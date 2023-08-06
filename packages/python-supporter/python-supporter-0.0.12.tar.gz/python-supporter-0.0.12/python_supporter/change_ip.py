import os
import platform
import subprocess
import time

class ChangeIp:
    def __init__(self, base_directory):
        super().__init__()
        self.base_directory = base_directory
        self.device = None
        self.ip = None

    def connect_to_device(self):    
        if not os.path.exists(f"{self.base_directory}/platform-tools"):
            import zipfile
            if platform.system() == 'Darwin': #맥
                from_zip = f"{self.base_directory}/platform-tools_r34.0.3-darwin.zip"
            elif platform.system() == 'Windows': #윈도우
                from_zip = f"{self.base_directory}/platform-tools_r34.0.3-windows.zip"
            elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
                from_zip = f"{self.base_directory}/platform-tools_r34.0.3-linux.zip"
            zip_file = zipfile.ZipFile(from_zip)
            zip_file.extractall(self.base_directory)
            zip_file.close()

        cmd = f"{self.base_directory}/platform-tools/adb"
        outputs = subprocess.check_output([cmd, "devices"]).decode('utf-8')
        device = None
        for output in outputs.split("\n")[1:]:
            output = output.strip()
            #print(output) #R95RB00QRCY     device
            if output:
                output = output.split("\t")[0]
                device = output
                break
        self.device = device
        return device
    
    def data_disable(self):
        cmd = f"{self.base_directory}/platform-tools/adb -s {self.device} shell svc data disable"
        os.system(cmd)

    def data_enable(self):
        cmd = f"{self.base_directory}/platform-tools/adb -s {self.device} shell svc data enable"
        os.system(cmd)

    def check_ip(self):    
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
        self.ip = ip
        return ip 
