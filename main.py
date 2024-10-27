import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types
import string
from datetime import datetime
import fake_useragent

def parsing(numberday, message, city):
    global soup

    bot.send_message(message.chat.id, f"🚩 {city}")  

    try:  
        day = soup.find_all("div", class_ = "forecast-briefly__name")[numberday].text
        time = soup.find_all("time", class_ = "time forecast-briefly__date")[numberday].text
        WeatherTemperatureDay = soup.find_all("div", class_ = "temp forecast-briefly__temp forecast-briefly__temp_day")[numberday].text
        WeatherTemperatureDay = str(WeatherTemperatureDay.replace("днём", " "))
        WeatherTemperatureDay = WeatherTemperatureDay.strip(string.whitespace)

        WeatherTemperaturenight = soup.find_all("div", class_ = "temp forecast-briefly__temp forecast-briefly__temp_night")[numberday].text
        WeatherTemperaturenight = str(WeatherTemperaturenight.replace("ночью", " "))
        WeatherTemperaturenight = WeatherTemperaturenight.strip(string.whitespace)

        condition = soup.find_all("div", class_ = "forecast-briefly__condition")[numberday].text     
        WeatherToday = f"{day} ({time})\nднём {WeatherTemperatureDay} \nночью {WeatherTemperaturenight} \n{condition}" 
        return WeatherToday

    except:
        error(message)   

def IP():
    global LINKIP

    try:
        lip = requests.get(LINKIP).text
        ip = lip.strip(string.whitespace)
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        city = response.get('city')

        return city

    except:
        print("Ошибка IP")  

def Weekday(numberweekday):
    match(numberweekday):
        case 0:
            numberweekday = "ПОГОДА В ПОНЕДЕЛЬНИК"
        case 1:
            numberweekday = "ПОГОДА ВО ВТОРНИК"
        case 2:
            numberweekday = "ПОГОДА В СРЕДУ"
        case 3:
            numberweekday = "ПОГОДА В ЧЕТВЕРГ"
        case 4:
            numberweekday = "ПОГОДА В ПЯТНИЦУ"
        case 5:
            numberweekday = "ПОГОДА В СУББОТУ"
        case 6:
            numberweekday = "ПОГОДА В ВОСКРЕСЕНИЕ"  
    return numberweekday        

def Weather(numberday):
    global soup 

    try:
        condition = soup.find_all("div", class_ = "forecast-briefly__condition")[numberday].text

        return condition

    except:
        print("Ошибка")      

def error(message):
    print("Ошибка")
    bot.send_message(message.chat.id, "Произошла ошибка подключения😢! \nНе переживайте наша команда уже трудиться")

LINKIP = "https://icanhazip.com/"
TOKEN = "7193616764:AAHFlbGKhwoMH_N0IHvBFmkjrHv3ai6SJ_g"

bot = telebot.TeleBot(TOKEN)

print("Бот запущен")

try:
    city = IP()
    city = city.lower()
    city = city.replace(" ", "-") 
    LINKWEATHER = f"https://yandex.ru/pogoda/{city}"

    user = fake_useragent.UserAgent().random
    header = {'user-agent': user }
    src = requests.get(LINKWEATHER)   
    r = src.text 
    soup = BeautifulSoup(r, "html") 

except:
    print("Ошибка подключения")


WeatherBy = {
    1 : " ",
    2 : " ",
    3 : " ",
    4 : " ",
    5 : " "
}

for i in range(1, 6):
    Weather1 = str(Weather(i))
    
    Weather2 = Weather1.lower()
    print(Weather2)

    if Weather2.find("дождь") >= 0:  
        WeatherBy[i]="🌨"
    elif Weather2.find("ясно") >= 0:  
        WeatherBy[i]="☀"
    elif Weather2.find("облачно") >= 0:  
        WeatherBy[i]="☁"   
    elif Weather2.find("пасмурно") >= 0:
        WeatherBy[i]="☁"    
    else:
        WeatherBy[i] = "?" 


print(WeatherBy)             

#keyboard 
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnToday = types.KeyboardButton(f"({WeatherBy[1]})ПОГОДА СЕГОДНЯ")
btnInformation = types.KeyboardButton("📃Информация")
btnYesteday = types.KeyboardButton(f"({WeatherBy[2]})ПОГОДА ЗАВТРА")

#Дни недели
year = int(datetime.now().strftime('%Y'))
month = int(datetime.now().strftime('%m'))

day1 = datetime(year, month, int(datetime.now().strftime('%d'))+2)
day2 = datetime(year, month, int(datetime.now().strftime('%d'))+3)
day3 = datetime(year, month, int(datetime.now().strftime('%d'))+4)

markup.add(btnToday, btnYesteday, btnInformation)        

for i in range(2, 5):
    daytoday = int(datetime.now().strftime('%d'))+i
    day = datetime(year, month, daytoday)
    day = day.weekday()

    btn = types.KeyboardButton(f"({WeatherBy[i+1]}){Weekday(day)}")       
    markup.add(btn) 

@bot.message_handler(commands=['start'])
def Hello(message):
    bot.send_message(message.chat.id, "Привет, {0.first_name}🤪. Меня зовут {1.first_name}. Если хочешь узнать погоду нажми кнопку ПОГОДА, выбрав день".
                     format(message.from_user, bot.get_me()), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def Weather(message):
    if message.text == f"({WeatherBy[1]})ПОГОДА СЕГОДНЯ":
        try:
            city = IP()
            bot.send_message(message.chat.id, parsing(1, message, city))
        except:
            error(message)
        
    elif message.text == f"({WeatherBy[2]})ПОГОДА ЗАВТРА":
        try:
            city = IP()
            bot.send_message(message.chat.id, parsing(2, message, city)) 
        except:
            error(message)
    elif message.text == f"({WeatherBy[3]}){Weekday(day1.weekday())}":
        try:
            city = IP()
            bot.send_message(message.chat.id, parsing(3, message, city)) 
        except:
            error(message)

    elif message.text == f"({WeatherBy[4]}){Weekday(day2.weekday())}":
        try:
            city = IP()
            bot.send_message(message.chat.id, parsing(4, message, city)) 
        except:
            error(message)
    elif message.text == f"({WeatherBy[5]}){Weekday(day3.weekday())}":        
        try:
            city = IP()
            bot.send_message(message.chat.id, parsing(5, message, city)) 
        except:
            error(message)

    elif message.text == "📃Информация":
        city = IP()
        city = city.strip(string.whitespace)
        city = city.replace(" ", "-")
        city = city.lower()
        bot.send_message(message.chat.id, "Bot создан в развлекательных целях. Вся информация берется с сайта " + 
                         f"https://yandex.ru/pogoda/{city} . Телеграмм бот с открытым исходным кодом. Ссылка на GitHub " + 
                         f"https://github.com/Mike-Belov/TelegramWeather")  

    else:
        bot.send_message(message.chat.id, "Не понял вас😩. Повторите")  

bot.polling(True)     