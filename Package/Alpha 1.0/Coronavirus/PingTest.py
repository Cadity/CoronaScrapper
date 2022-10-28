import os

def check_ping():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        pingstatus = 1
    else:
        pingstatus = 0
    
    return pingstatus