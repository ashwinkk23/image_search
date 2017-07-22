import os
import pandas as pd
import csv
import json
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import requests
import io
import PIL
import base64
from bs4 import BeautifulSoup as bs
import TellGender
raw = pd.read_csv('data.csv')
df = pd.read_csv('processed.csv')
root = os.getcwd()

X = np.array(df.ix[:,0:244])
Y = np.array(df['ID'])
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X,Y.ravel())


def plot_corr(df,size):
    fig, ax=plt.subplots(figsize=(10,10))
    corr = df.corr()
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)),corr.columns)
    plt.yticks(range(len(corr.columns)),corr.columns)
    plt.show()

def data_from_url(url):
    da = TellGender.gender(url)
    da = da['faces'][0]['points']
    da = pd.DataFrame(da)
    del da['name']
    del da['type']
    DA = np.concatenate((np.array(da['x']).reshape(1,122),np.array(da['y'].reshape(1,122))),axis=0).reshape(1,244)
    return DA
    
def name_from_url(url):
    da = TellGender.gender(url)
    da = da['faces'][0]['points']
    da = pd.DataFrame(da)
    del da['name']
    del da['type']
    DA = np.concatenate((np.array(da['x']).reshape(1,122),np.array(da['y'].reshape(1,122))),axis=0).reshape(1,244)
    prediction = knn.predict(DA)
    name = raw['Name'][raw['USN']==prediction[0]][raw['Name'][raw['USN']==prediction[0]]].index[0]
    return name,prediction[0]

def name_from_image(img):
    with open(img, "rb") as i_file:
        encoded_string = base64.b64encode(i_file.read())
    url1 = 'http://www.betafaceapi.com/service.svc/UploadNewImage_File'
    url2 = "http://www.betafaceapi.com/service_json.svc/GetImageInfo"
    to_send= {
	"api_key":"d45fd466-51e2-4701-8da8-04351c872236",
	"api_secret":"171e8465-f548-401d-b63b-caf0dc28df5f",
	"detection_flags":"gender",
	"imagefile_data":encoded_string,
	"original_filename":"trial"
    }
    while True:
        r = requests.post(url1, data=to_send)
        soup = bs(r.text,'lxml')
        uid = soup.find_all('img_uid')[0].text
        to_send_again = {
        "api_key":"d45fd466-51e2-4701-8da8-04351c872236",
        "api_secret":"171e8465-f548-401d-b63b-caf0dc28df5f",
        "img_uid":uid
        }
        s = requests.post(url2,data=to_send_again)
        a = json.loads(s.text)
        a = a['faces'][0]['points']
        a = pd.DataFrame(a)
        del a['name']
        del a['type']
        DA = np.concatenate((np.array(a['x']).reshape(1,122),np.array(a['y'].reshape(1,122))),axis=0).reshape(1,244)
        p = knn.predict(DA)
        del DA
        if(r.status_code == 200 and s.status_code == 200):
            break
    return raw['Name'][raw['USN']==p[0]][raw['Name'][raw['USN']==p[0]]].index[0],p[0]
    
