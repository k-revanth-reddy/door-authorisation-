import cv2
import boto3
import os

family=os.listdir('family/')
client=boto3.client('rekognition')
cam=cv2.VideoCapture(0) # index of camera

k=input('Enter what you want me to do: ')
if k.lower()=='open':
    print('Calling Face Recognition Service')
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
        if(flag==0):
            print('You are a Stranger')
        
else:
    print('Invalid Command,Try again')