import requests

#https://www.myip.com/api-docs/
#https://api.myip.com/
def check_ip():    
    try:
        response = requests.get("https://api.myip.com")
        print(response.json()) #{"ip":"180.92.96.163","country":"Korea, Republic of","cc":"KR"}
        return response.json()["ip"]
    except:
        return None
