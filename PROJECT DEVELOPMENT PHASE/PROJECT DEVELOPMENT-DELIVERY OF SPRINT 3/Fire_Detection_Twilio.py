import cv2        
import threading   
import playsound  
from twilio.rest import Client
  

fire_cascade = cv2.CascadeClassifier('fire_detection.xml') 

vid = cv2.VideoCapture(0) 
runOnce = False 

def play_alarm_sound_function():
    playsound.playsound('FOM.mp3',True) 
    print("Fire alarm end") 

def send_Twilio_function(): 
    
    SID = 'AC9e15eae056ba54ebe61e3ed93d4f2658'

    Auth_Token = 'a049c8a7500762182c3fa47a9fa239f7'

    cl = Client(SID, Auth_Token)

    cl.messages.create(body="Forest Fire Go To Saved Places", from_= '+18563865770',to='+919965265228')

    
		
while(True):
    Alarm_Status = False
    ret, Forest = vid.read() 
    gray = cv2.cvtColor(Forest, cv2.COLOR_BGR2GRAY) 
    fire = fire_cascade.detectMultiScale(Forest, 1.2, 5) 

    
    for (x,y,w,h) in fire:
        cv2.rectangle(Forest,(x-20,y-20),(x+w+20,y+h+20),(0,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = Forest[y:y+h, x:x+w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread

        if runOnce == False:
            print("Twilio send initiated")
            threading.Thread(target=send_Twilio_function).start() # To call Twilio thread
            runOnce = True
        if runOnce == True:
            print("Twilio is already sent once")
            runOnce = True

    cv2.imshow('Forest', Forest)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release
cv2.destroyAllWindows    