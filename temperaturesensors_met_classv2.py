import time
import datetime
import os
import glob
import PySimpleGUI as sg
from ISStreamer.Streamer import Streamer
import threading
from threading import Thread
import concurrent.futures
import smtplib, ssl

port = 465  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "nlyusufcetin@gmail.com"
receiver_email = "nlyusufnitec@gmail.com"

password = 'okgm hqtw tjbz booh'


streamer = Streamer(bucket_name="Temperature Stream-1",bucket_key="piot_temp_stream031815", access_key = "ist_A1_NZy3vwBVJs2Tw-3QfZCzWF5Udc7g0")

#Send warning mail
def snd_mail(msg):
    message = msg
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    except:
        print("there is problem")
        pass



os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# prepare sensors for reading, write the adress of sensor's folders
base_dir = '/sys/bus/w1/devices/'

# "try-pass "if power pin not connected then bypass for reading temp, continue to work.
try:
    device_folder1 = glob.glob(base_dir + '28-01215c857889')[0]
except:
    pass

try:
    device_folder2 = glob.glob(base_dir + '28-01215c98f77b')[0]
except:
    pass

try:
    device_folder3 = glob.glob(base_dir + '28-01215c8401da')[0]
except:
    pass

device_file1 = device_folder1 + '/w1_slave'
device_file2 = device_folder2 + '/w1_slave'
device_file3 = device_folder3 + '/w1_slave'

#Reading sensors

class Read_temp(object):
    
    def __init__(self,device_file):
        self.device_file = device_file
            
    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        line = f.readlines()
        f.close()
        return line
        
    def __str__(self):
        try:
            lines = self.read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self.read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos + 2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 +32.0
                return str(temp_c)
        except:
            return '300' # if cant read the temp from the read pin, return this value (sensors can read max 125 C)
            pass



# Create a layout for the GUI, three columns for three sensors
sg.theme('DarkTeal6')
col_1 =[
    [sg.VPush()],[sg.VPush()],[sg.VPush()],[sg.VPush()],
    [sg.Text(size=(10,3), key='temp1',font=("Helvetica", 20), text_color='white',justification='center')],
    [sg.Text(size=(10,3),key='wtext_1')],
    [sg.Input(key='input_1',size=(10,10)),sg.Button(button_text = 'Change warning temp', key='button_1')]
    ]
 
col_2 =[
    [sg.VPush()],[sg.VPush()],[sg.VPush()],[sg.VPush()],
    [sg.Text(size=(10, 3), key='temp2',font=("Helvetica", 20), text_color='white',justification='center')],
    [sg.Text(size=(10,3),key='wtext_2')],
    [sg.Input(key='input_2',size=(10,10)),sg.Button(button_text = 'Change warning temp',key='button_2')]
    ]
 
col_3 =[
    [sg.VPush()],[sg.VPush()],[sg.VPush()],[sg.VPush()],
    [sg.Text(size=(10, 3), key='temp3',font=("Helvetica", 20), text_color='white',justification='center')],
    [sg.Text(size=(10,3),key='wtext_3')],
    [sg.Input(key='input_3',size=(10,10)),sg.Button(button_text = 'Change warning temp',key='button_3')]

     ]

layout =[[sg.Text('Temperature Sensors Dashboard', font=("Helvetica", 20), text_color='white')],
        [sg.Frame(layout=col_1,title='Temperature Sensor -1-',visible=True, key='frame_1'),
         sg.Frame(layout=col_2,title='Temperature Sensor -2-',visible=True, key='frame_2'),
         sg.Frame(layout=col_3,title='Temperature Sensor -3-',visible=True, key='frame_3')],
        [sg.Exit()],
        [sg.Text(size=(10,3),key='try')]
        ]

# Create the window
window = sg.Window('Temperature Sensors Dashboard', layout,default_element_size=(30, 2),auto_size_text=False,auto_size_buttons=False)

#Default sensor's max. warning values
warning_1 ='23'
warning_2 ='23'
warning_3 ='23'
tmt1 = 0
tmt2 = 0
tmt3 = 0

# Main program 
while True:
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    n = datetime.datetime.now() #to take minute from time

    tmp1 = str(Read_temp(device_file1)) 
    tmp2 = str(Read_temp(device_file2)) 
    tmp3 = str(Read_temp(device_file3))
#Warning text on secreen
    if float(tmp1)>float(warning_1):
        window[f'wtext_1'].update('WARNING!')
        if(n.minute - tmt1 > 1):
            #snd_mail("Warning ! On temperature sensor 1, the temperature reached the maximum value!")
            print("send mail!")
            tmt1 = n.minute
    else:
        window[f'wtext_1'].update('')

    if float(tmp2)>float(warning_2):
        window[f'wtext_2'].update('WARNING!')
        if(n.minute - tmt2 > 1):
            #snd_mail("Warning ! On temperature sensor 2, the temperature reached the maximum value!")
            print("send mail!")
            tmt2 = n.minute
    else:
        window[f'wtext_2'].update('')
     
    if float(tmp3)>float(warning_3):
        window[f'wtext_3'].update('WARNING!')
        if(n.minute - tmt3 > 1):
            #snd_mail("Warning ! On temperature sensor 3, the temperature reached the maximum value!")
            print("send mail!")
            tmt3 = n.minute
    else:
        window[f'wtext_3'].update('')


#Warning Buttons
    if event == 'button_1':
        warning_1 =values['input_1']

    if event == 'button_2':
        warning_2 =values['input_2']

    if event == 'button_3':
        warning_3 =values['input_3']

#Checking if temp sensor plug in. If not, make column invisible. Controlling both power pin and read pin value
    if tmp1 !='300' and str(tmp1) !='85.0': #"85" is if power pin not connected, can read 85 only
        window['frame_1'].update(visible=True)
        window[f'temp1'].update(tmp1)
    else:
        window['frame_1'].update(visible=False)

    if tmp2 != '300' and str(tmp2) !='85.0':
        window['frame_2'].update(visible=True)
        window[f'temp2'].update(tmp2)
    else:
        window['frame_2'].update(visible=False)
     
    if tmp3 !='300'and str(tmp3) !='85.0':
        window['frame_3'].update(visible=True)
        window[f'temp3'].update(tmp3)
    else:
        window['frame_3'].update(visible=False)
    
time.sleep(1)   
window.close()

