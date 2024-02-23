import serial
import telebot
import time

chat_id='1937153612'
police_id='1104552069'
bot=telebot.TeleBot(token='6144658985:AAEgZNhMjE9nBObqcLA5Z5DD8bZ2AVdHzfo')

ser=serial.Serial('COM3',9600,timeout=0.5)
ser.close()
ser.open()

while True:
    if (ser.in_waiting>0):
        t=ser.readline()
        t=t.decode('utf-8')
        print(t)
        
        if(t.startswith('#')):
            print('Invoking Notification')
            bot.send_message(chat_id,"Vibrations Detected at your home")
            time.sleep(3)
            bot.send_message(police_id,"Theft Alert located at Lat: 15.7194586,, Long: 78.008111")
            time.sleep(3)