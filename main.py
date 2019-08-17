import sensor_data as IoT
import simplejson as json
import requests
import calendar;
import time;
import threading 
from threading import Thread

data={}
# the result is a Python dictionary:
server_data = []
f= open("logs.txt","w+")

with open('configuration.json') as f:
  data = json.load(f)


def collect_data():
    threading.Timer(1.0, collect_data).start()
    for (k, v) in data.items():
        if(k!="configuration"):
            if(v.get("DeviceType")=="Analog"):
                device_data = {}
                value = IoT.read_data_rs485_holding(data['configuration'],v)
                if v.get("Threshold")==value:
                    print("send alarm")
                else:
                    device_data['Gatewayname']=v.get("Gatewayname")
                    device_data['parameter']=k
                    device_data['timestamp']=str(calendar.timegm(time.gmtime()))
                    device_data['value']=value
                    server_data.append(device_data)
                    #f.write(device_data)

        if (v.get("DeviceType") == "Digital"):
                device_data = {}
                value = IoT.read_data_IO(v.get("PIN"),v.get("Mode"))
                if v.get("Threshold") == value:
                    print("send alarm")
                else:
                    device_data['Gatewayname'] = v.get("Gatewayname")
                    device_data['parameter'] = k
                    device_data['timestamp'] = str(calendar.timegm(time.gmtime()))
                    device_data['value'] = value
                    server_data.append(device_data)
                    #f.write(device_data)                    
    print(server_data)
    print(len(server_data))

def push_data():
    threading.Timer(30, push_data).start()
    print("-----------------------------------------------")
    print("pushing to server")
    print(server_data)
    print(len(server_data))
    f.write(convert(server_data)) 
    reset_list()
    print(len(server_data))

    

def reset_list():
    server_data.clear()

def convert(list):    
    # Converting integer list to string list 
    s = [str(i) for i in list]       
    # Join list items using join() 
    res = int("".join(s))       
    return(res) 

if __name__ == '__main__':
    Thread(target = collect_data).start()
    Thread(target = push_data).start()


#IoT.read_data_rs485(data['configuration'],data['Temperature_Temperature'])