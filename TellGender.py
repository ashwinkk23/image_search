import requests
import json
from bs4 import BeautifulSoup as bs
import os
def gender(imgURL):
    while (True):
        try:
            send = {"api_key":"d45fd466-51e2-4701-8da8-04351c872236",
            "api_secret":"171e8465-f548-401d-b63b-caf0dc28df5f",
            "detection_flags":"gender",
            "image_url":imgURL,
            "original_filename":"Trial"}
            url = "http://www.betafaceapi.com/service.svc/UploadNewImage_Url"
            r = requests.post(url, data=send)
            soup = bs(r.text,'lxml')
            aa = soup.find_all('img_uid')[0].text
            trial2 = {
            "api_key":"d45fd466-51e2-4701-8da8-04351c872236",
            "api_secret":"171e8465-f548-401d-b63b-caf0dc28df5f",
            "img_uid":aa
            }
            url2 = "http://www.betafaceapi.com/service_json.svc/GetImageInfo"
            s = requests.post(url2,data = trial2)

            a = json.loads(s.text)
            if (r.status_code == 200) and (s.status_code == 200):
                break
        except:
            print("Bad connection...")
            continue
    try:
        #return a['faces'][0]['tags'][3]['value']
        return a
    except:
        return None
    

