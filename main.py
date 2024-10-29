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
    if numberweekday == 0:
        day = "ПОГОДА В ПОНЕДЕЛЬНИК"
    elif numberweekday == 1:
        day = "ПОГОДА ВО ВТОРНИК"
    elif numberweekday == 2:
        day = "ПОГОДА В СРЕДУ"
    elif numberweekday == 3:
        day = "ПОГОДА В ЧЕТВЕРГ"
    elif numberweekday == 4:
        day = "ПОГОДА В ПЯТНИЦУ"
    elif numberweekday == 5:
        day = "ПОГОДА В СУББОТУ" 
    elif numberweekday == 6:
        day = "ПОГОДА В ВОСКРЕСЕНЬЕ"    
    else:
        print("Не удалось получить информацию (смотреть день недели)")                       
       
    return day        

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
    src = requests.get(LINKWEATHER, headers=header)   
    r = src.text 
    soup = BeautifulSoup(r, "html.parser") 

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
        WeatherBy[i]="☁🌨"    
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

endmonth = 5
newmoth = 0

try:
    yesteday = datetime(year, month, int(datetime.now().strftime('%d'))+1)
except:
    newmoth += 1
try:
    day1 = datetime(year, month, int(datetime.now().strftime('%d'))+2)
except:
    endmonth = endmonth-1
    newmoth += 1
try:
    day2 = datetime(year, month, int(datetime.now().strftime('%d'))+3)
except:
    endmonth = endmonth-1 
    newmoth += 1 
try:
    day3 = datetime(year, month, int(datetime.now().strftime('%d'))+4)
except:
    endmonth = endmonth-1  
    newmoth += 1

markup.add(btnToday, btnYesteday, btnInformation)        

for i in range(2, endmonth):
    try:
        daytoday = int(datetime.now().strftime('%d'))+i
        day = datetime(year, month, daytoday)
        day = day.weekday()
    
        btn = types.KeyboardButton(f"({WeatherBy[i+1]}){Weekday(day)}")       
        markup.add(btn) 
    except:
        print("Погода будет известна через несколько дней")    

if month+1 > 12:  
    nextmonth = 1
    year = int(datetime.now().strftime('%Y'))+1
else:
    nextmonth = month+1

if newmoth > 0:
    if newmoth == 4:
        day1 = datetime(year, nextmonth, 2)
        day2 = datetime(year, nextmonth, 3)
        day3 = datetime(year, nextmonth, 4)
     
        for i in range(1, 4):
            try:
               daytoday = i+1
               day = datetime(year, nextmonth, daytoday)
               day = day.weekday()

               weatherspeed = 3
            
               btn = types.KeyboardButton(f"({WeatherBy[weatherspeed]}){Weekday(day)}")     
               weatherspeed +=1  
               markup.add(btn) 
            except:
               print("Погода будет известна через несколько дней") 
    elif newmoth == 3:
        day1 = datetime(year, nextmonth+1, 1)
        day2 = datetime(year, nextmonth+1, 2)
        day3 = datetime(year, nextmonth+1, 3)

        for i in range(1, 4):
            try:
               daytoday = i
               day = datetime(year, nextmonth, daytoday)
               day = day.weekday()

               weatherspeed = 3
            
               btn = types.KeyboardButton(f"({WeatherBy[weatherspeed]}){Weekday(day)}")     
               weatherspeed += 1  
               markup.add(btn) 
            except:
               print("Погода будет известна через несколько дней") 
    elif newmoth == 2:
        day2 = datetime(year, nextmonth, 1)
        day3 = datetime(year, nextmonth, 2)

        for i in range(1, 3):
            try:
               daytoday = i
               day = datetime(year, nextmonth, daytoday)
               day = day.weekday()

               weatherspeed = 4
            
               btn = types.KeyboardButton(f"({WeatherBy[weatherspeed]}){Weekday(day)}")  
               weatherspeed +=1     
               markup.add(btn) 
            except:
               print("Погода будет известна через несколько дней") 
    elif newmoth == 1:
        day3 = datetime(year, nextmonth, 1) 
        try:
           daytoday = 1
           day = datetime(year, nextmonth, daytoday)
           day = day.weekday()
        
           btn = types.KeyboardButton(f"({WeatherBy[5]}){Weekday(day)}")       
           markup.add(btn) 
        except:
           print("Погода будет известна через несколько дней")         


@bot.message_handler(commands=['start'])
def Hello(message):
    bot.send_message(message.chat.id, "Привет, {0.first_name}🤪. Меня зовут {1.first_name}. Если хочешь узнать погоду нажми кнопку ПОГОДА, выбрав день".
                     format(message.from_user, bot.get_me()), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def Weather(message):
    try:
        if message.text == f"({WeatherBy[1]})ПОГОДА СЕГОДНЯ":
            try:
                city = IP()
                bot.send_message(message.chat.id, parsing(1, message, city))
            except:
                error(message)
    
        elif message.text == "📃Информация":
            city = IP()
            city = city.strip(string.whitespace)
            city = city.replace(" ", "-")
            city = city.lower()
            bot.send_message(message.chat.id, "Bot создан в развлекательных целях. Вся информация берется с сайта " + 
                             f"https://yandex.ru/pogoda/{city} . Телеграмм  bot с открытым исходным кодом. Ссылка на GitHub " + 
                             f"https://github.com/Mike-Belov/TelegramWeather")         
            
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
    
        else:
            bot.send_message(message.chat.id, "Не понял вас😩. Повторите") 
    except:
        bot.send_message(message.chat.id, "Не понял вас😩. Повторите")              

while 1:
    try:
        bot.polling(none_stop=True,timeout=5)
    except Exception as e:
        print(e)