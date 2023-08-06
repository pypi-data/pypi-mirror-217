import os
import platform
import subprocess
import time

def check_ip():    
    cmd = "nslookup"
    outputs = subprocess.check_output([cmd, "myip.opendns.com", "resolver1.opendns.com"]).decode("cp949")
    #print(outputs)
    '''
권한 없는 응답:
서버:    dns.opendns.com
Address:  208.67.222.222

이름:    myip.opendns.com
Address:  210.105.109.16        
    '''
    ip = None
    for output in outputs.split("\n")[1:]:
        output = output.strip()
        #print(output) #Address:  210.105.109.16
        if "Address:" in output:
            li = output.split(" ")
            #print(li) #['Address:', '', '210.105.109.16']
            ip = li[-1]
            #print(output)
    return ip 
