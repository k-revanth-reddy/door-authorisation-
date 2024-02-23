import serial
import time
import cv2
import os
import boto3
import telebot

chat_id='1937153612'
bot=telebot.TeleBot(token='6144658985:AAEgZNhMjE9nBObqcLA5Z5DD8bZ2AVdHzfo')

@bot.message_handler(commands=['open'])
def open_door(message):
 if (message.chat.id==1937153612):
  bot.reply_to(message,"Your door will be opened soon")
  print('Waiting for Door to open')
  ser.close()
  ser.open()
  time.sleep(2)
  ser.write('open'.encode('utf-8'))
  time.sleep(10)
  print('Door should open')
  bot.stop_polling()
 else:
  bot.reply_to(message,"Sorry, you can't do that")
  bot.stop_polling()

@bot.message_handler(commands=['close'])
def close_door(message):
 if (message.chat.id==1937153612):
  bot.reply_to(message,"Your door will not be opened")
  bot.stop_polling()
 else:
  bot.reply_to(message,"Sorry, you can't do that")
  bot.stop_polling()

ser=serial.Serial('COM3',9600,timeout=0.5)
ser.close()
ser.open()

cam=cv2.VideoCapture(0) # index of camera
family=os.listdir('family/')
client=boto3.client('rekognition')

def callingCamera():
    try:
     if cam.isOpened():
        status,frame=cam.read()
        cv2.imwrite('test.jpg',frame)
        cv2.waitKey(1)
        flag=0
        for i in family:
            imageSource=open('test.jpg','rb')
            imageTarget=open('family/'+i,'rb')
            response=client.compare_faces(
                SimilarityThreshold=70,
                SourceImage={'Bytes':imageSource.read()},
                TargetImage={'Bytes':imageTarget.read()}
            )
            if response['FaceMatches']:
                result=i.split('.')[0]
                flag=1
                print('Face Matched with '+result)
                return(1)
        if(flag==0):
            print('You are a Stranger')
            bot.send_document(chat_id=chat_id,document=open('test.jpg','rb'))
            return(0)
    except:
     print('No person')

while True:
    if (ser.in_waiting>0):
        t=ser.readline()
        t=t.decode('utf-8')
        print(t)
        
        if(t.startswith('#Alert')):
            print('Invoking Camera')
            response1=callingCamera()
            if(response1==1):
                ser.close()
                ser.open()
                ser.write('open'.encode('utf-8'))
                time.sleep(2)
            elif(response1==0):
                print('Invoking Telegram')
                bot.polling()
