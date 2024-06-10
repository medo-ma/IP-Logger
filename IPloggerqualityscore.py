#imported modules:[time, requests, winotify]
import time
import tkinter
import requests
import re
from winotify import Notification, audio
from pathlib import Path
import os
#ip counter defulte value
call_counter = 0
Notifyrepeat = 0
api_Qscore=[]
apiNum= 0
VersionN="v1.1"
xd=0

#create new config
#set the config before app getting start.
def configFile():
    try:
            filename = Path('config.txt')
            filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
            file = open(filename,'r')
            x0content=file.readlines() 
            return x0content
    except Exception as e:
        print(f"Error loading config: {e}")

#configuration:
def ConfigN():
    try:
        #global_varibales
        global Notify
        global DurN
        global Notifyrepeat
        global api_Qscore
        global apiNum
        global api_Qx
        config_file = configFile()
        

#check if there's a need for resetting the config    
        if len(config_file) == 0:

            #api entering step
            api_Qx = int(input("how many APIs do want to add?\n"))
            for _ in range(api_Qx):
                    api_Q=input("what's your APIs?\n")
                    api_Qscore.append(api_Q)

            apiNum=int(input("which one do u want use first?, ex:'1' \n"))    
            Notify = input('1-notify for duplicate ip\nchoose y or n:\n ').lower().strip()

            if Notify == "y" or Notify=='yes':
                Notify = True
            else:
                Notify = False

            if Notify:
                DurN = int(input('2-notify for duplicate ip\nchoose delay time in sec: ((only numbers))\n ').strip())
                Notifyrepeat = int(input('3-number of repeatation for duplicate ip:((only numbers))\n ').strip())

            if Notify:    
                with open('config.txt', 'w') as config_file:
                    config_file.write(f"#set up yor prefered configuration from here:\n")
                    
                    config_file.write(f"-notify for duplicate ip:'{Notify}'\n")
                    config_file.write(f"-delay time:'{DurN}'\n")    
                    config_file.write(f"-number of repeatation:'{Notifyrepeat}'\n")    
                    config_file.write(f"-u are useing api number:'{apiNum}'\n")
                    config_file.write(f"-write your API:'{api_Qscore}'\n")
                    config_file.write(f"\n__'ip-logger' By MedoMa, version:{VersionN}__\n")
            else:
                DurN = 0
                Notifyrepeat = 0
                with open('config.txt', 'w') as config_file:
                    config_file.write(f"#set up yor prefered configuration from here:\n")
                    config_file.write(f"-notify for duplicate ip:'{Notify}'\n")
                    config_file.write(f"-delay time:'{DurN}'\n")    
                    config_file.write(f"-number of repeatation:'{Notifyrepeat}'\n") 
                    config_file.write(f"-u are useing api number:'{apiNum}'\n")
                    config_file.write(f"-write your API:'{api_Qscore}'\n")
                    config_file.write(f"\n__'ip-logger' By MedoMa, version:{VersionN}__\n")

            #recorrection for apiNum        
            apiNum -= 1        
        else:   
            #read the pre-set settings     
            with open('config.txt', 'r') as config_file:
                lines=config_file.readlines()
                Notify=lines[1].strip().split(":'")[1].rstrip("'").capitalize()
                #print(Notify)
                DurN=int(lines[2].strip().split(":'")[1].rstrip("'"))
                Notifyrepeat=int(lines[3].strip().split(":'")[1].rstrip("'"))
                apiNum=int(lines[4].strip().split(":'")[1].rstrip("'")) 
                apiNum -= 1 #recorrection for apiNum 
                api_Qscore1=lines[5].strip()
                #new one(api_Qscore):
                api_Qscore=re.findall(r'https?://[A-z]+\.[A-z]+/[A-z]+/[A-z]+/[A-z]+/[A-z0-9]+/\?[A-z]+=[A-z0-9]+&[A-z0-9]+=[A-z0-9]',api_Qscore1)
                #old one(api_Qscore):
                # urls_part = api_Qscore1.split(":'['")[1].rstrip("']")
                # api_Qscore = urls_part.split("', '")
                #print(lines)
                return apiNum,api_Qscore,Notifyrepeat,DurN,Notify
        return apiNum,api_Qscore,Notifyrepeat,DurN,Notify

    except Exception as e:
        print(f"Error in configuration: {e}")
#func to get the ip using requests
def get_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json().get('ip')
    except requests.RequestException as e:
        #print(f"Error getting public IP: {e}")
        return None

#load ip from ip_log and creat it if it ain't exist
def load_ip_log():
    try:
            filename = Path('ip_log.txt')
            filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
            log_file = open(filename)
            lines = log_file.readlines()
            #print(lines)
            clear()
            return [ip.strip().split('-')[-1].strip() for ip in lines]
            
    except Exception as e:
        print(f"Error loading IP log: {e}")
        return []

def check_internet_connection():
    try:
        time.sleep(10)
        requests.get('https://www.google.com', timeout=5).raise_for_status()
        return True
    except requests.RequestException:
        #print("Internet connection lost.")
        return False

def log_ip(ip):
    try:
        global call_counter
        call_counter += 1
        #pick and prepare the api
        ApiReq = api_Qscore[apiNum].split('/')
        ApiReq.insert(7 , f"{ip}")
        ApiReq="/".join(ApiReq)

        # Second POST request
        response2 = requests.get(f"{ApiReq}")


        # Check if the second response is not null
        if response2:
            result= process_second_response(response2, ip)          
        else:
                    print("Second response is null.")


        if ip:
            with open('ip_log.txt', 'a+') as log_file:
                    log_file.write(f"{time.strftime('%Y-%m-%d %I:%M:%S:%p')} - {ip} \n{result}\n")
                    #cmd result decoration
                    print(f"_" * 100)
                    print(f"{f'-{call_counter}-':^90}")
                    print(f"{'^^^':^90}")
                    print(f"1-Public IP logged: {ip}")
                    print(f"2-{result}")
                    print(f'{"_" * 20:^90}')
                    print(f"{f"Time:{time.strftime('%I:%M:%S:%p')}":^90}")
                    print(f"_" * 100)
                    print(f"\n" * 2)
        else:
            print("Error: New IP is None. Skipping logging and requests.")
    except Exception as e:
        print(f"Error logging IP: {e}")

def process_second_response(response, ip):
    try:
        json_response = response.json()
        fraud_score = json_response.get("fraud_score", "N/A")
        ISP = json_response.get("ISP", "N/A")
        vpn = json_response.get("vpn", "N/A")
        proxy = json_response.get("proxy", "N/A")

        # Show the extracted information from the second response in a notification
        send_notification(f"IP Quality Score for IP {ip}:\n Fraud Score={fraud_score},\n ISP={ISP}, VPN={vpn}, Proxy={proxy}")
        
        
        return f"IP Quality Score for IP {ip}:ISP={ISP} ,Fraud Score={fraud_score}, VPN={vpn}, Proxy={proxy}"
    except ValueError as ve:
        print(f"Error decoding JSON response: {ve}")
        send_notification("Error decoding IP Quality Score JSON response")

def check_and_notify_duplicate(new_ip, logged_ips):
    try:
        if (Notify == 'True') or (Notify == True) :
            if new_ip in logged_ips:
                xd=0
                while xd != Notifyrepeat:
                    nowip = get_public_ip()
                    if nowip == new_ip:
                        send_notification(f"Warning: New IP ({new_ip}) matches a previously logged IP.")
                        time.sleep(DurN)
                        xd += 1
                    else:                            
                        xd = Notifyrepeat     
                return True         
        else:
            send_notification(f"New IP detected: {new_ip}")
            return False   
    except Exception as e:
        print(f"Error checking duplicate IP: {e}")
        return False

def send_notification(message):
    try:
        app_id = "ip monitor -ma"  # Replace with your unique app_id
        toast = Notification(
            app_id,
            title="IP Monitor",
            msg=message,
            duration='long',
            icon=r"C:\Users\medo_ma\Desktop\New folder\1.ico"
        )
        toast.set_audio(audio.Mail, loop=False)
        # toast.add_actions(label="Button text", 
        #             launch="url")
        toast.show()
        time.sleep(5)
        
    except Exception as e:
        print(f"Error sending notification: {e}")

def is_script_working_correct(logged_ips):
    try:
        if len(logged_ips) > 0:
            last_logged_ip = logged_ips[-1]
            send_notification(f"Script is working correctly.\nLast logged IP: {last_logged_ip}.\nthanks for using the 'IP Logger' by medo_ma")
            return True
        else:
            #print("No IPs logged yet. Script may not be functioning correctly.")
            return False
    except Exception as e:
        print(f"Error checking script status: {e}")
        return False

def main():
    logged_ips = load_ip_log()
    current_ip = None
    #print(logged_ips)
    while True:
        time.sleep(2)

        # Check internet connection
        if not check_internet_connection():
            continue

        # Internet connection restored
        new_ip = get_public_ip()
        
        if new_ip is not None and new_ip != current_ip:
            # Check for duplicate and notify
            if not check_and_notify_duplicate(new_ip, logged_ips):
                # Log the new IP
                log_ip(new_ip)
                logged_ips.append(new_ip)

                current_ip = new_ip

                # Check script status after an event
                is_script_working_correct(logged_ips)
def clear():
    os.system('clear||cls')
def start():
    while True:
        ConfigN()
        main()

if __name__ == "__main__":
    start()
    # ConfigN()
    # main(Notify)