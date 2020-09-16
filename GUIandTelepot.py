import datetime
import telepot
from telepot.loop import MessageLoop
import RPi.GPIO as GPIO
from time import sleep
try:
	import tkinter as tk
except:
	import Tkinter as tk
from PIL import ImageTk, Image
import pyautogui

#userID = 1350550818 #idris
userID = 1175189504 #fiona
BOT_TOKEN = '1043973887:AAHSdZ_qXsdUna4t0QBoNiYc3_4xgK_qk-M'
motor_pin = 21

GPIO.setmode(GPIO.BCM) #board pin numbering
GPIO.setup(motor_pin, GPIO.OUT)


def spinMotor(time):
	GPIO.output(motor_pin, True)
	sleep(time)
	GPIO.output(motor_pin,False)

def wakeScreen():
	pyautogui.move(0,50)#wake screen
	pyautogui.move(0,-50)
	#pyautogui.click()
	
###############start telegram stuff#########
def handle(msg):
	content_type,chat_type,chat_id = telepot.glance(msg)
	chat_id = msg['chat']['id'] #recieve message
	#mType = msg['chat']['content_type']
	#print('Recieved: ')
	#print(chat_id)
	#userID = -chat_id
	
	#print(content_type)
	
	if content_type == 'photo':
		wakeScreen()
		text_box.delete('1.0',tk.END)
		text_box.config(spacing1=5)
		text_box.insert('1.0'," ","msg")   #to center photo
		bot.download_file(msg['photo'][1]['file_id'],'/home/pi/Desktop/pictures/sentpic.png')
		sleep(1)
		img = ImageTk.PhotoImage(Image.open('/home/pi/Desktop/pictures/sentpic.png'))
		text_box.image_create(tk.END,image=img)
		text_box.image = img
		spinMotor(1)
		return
		
	elif content_type =='text':
		
		command = msg['text']
		if command == '/test':
			bot.sendMessage(userID, str("The pi is running"))
		elif command == '/exit':
			 quit
		elif command =='/clear':
			text_box.delete('1.0',tk.END)
		elif command == '/help':
			bot.sendMessage(userID, str("Possible commands: \n/exit, /clear, /test\nOr no slash to send message"))
		else:
			wakeScreen() 
			text_box.delete('1.0',tk.END)
			text_box.config(spacing1=sHeight/2-fontSize)
			text_box.insert('1.0',msg['text'],"msg")
			text_box.update_idletasks()
			spinMotor(1)

			
		
bot = telepot.Bot(BOT_TOKEN)
#print(bot.getMe())
MessageLoop(bot,handle).run_as_thread()

##############end telegram stuff##############

##############start gui stuff################
fontSize = 50

#for onclick to clear
def callback(event):
	#print("clicked")
	sleep(2)
	text_box.delete('1.0',tk.END)
	bot.sendMessage(userID, str("Your message was seen"))

window = tk.Tk()
sHeight = window.winfo_screenheight()+5
sWidth = window.winfo_screenwidth()+5
window.geometry(str(sWidth)+'x'+str(sHeight)+'+'+str(-5)+'+'+str(-5))
frame = tk.Frame(window,width=sWidth,height=sHeight)
frame.pack()

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

text_box = tk.Text(frame,fg="white",bg = "black",font=("Courier",fontSize,"bold"),spacing1=sHeight/2-fontSize)
text_box.tag_configure("msg",justify='center')

text_box.place(x=0,y=0,height=sHeight,width=sWidth)
text_box.bind("<Button-1>",callback)

exitBtn = tk.Button(window,fg="#4B4747",bg="black",text="Exit",command=quit,borderwidth=0,highlightbackground="black"
)
exitBtn.place(x=sWidth-50,y=sHeight-50,width=50,height=50)
exitBtn.lift()

window.attributes("-fullscreen",True)
#window.attributes('-topmost', True)

message = "uwu"
text_box.insert('4.0',message,"msg")
##################end GUI stuff##############

window.mainloop()

while True:
	sleep(10)


