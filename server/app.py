from flask import Flask, render_template, send_file
from flask import request
from bs4 import BeautifulSoup
import requests
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import pytz
import os

app=Flask(__name__)


config = {
    "apiKey": "AIzaSyC-6dvMzUmmHBlzVmqpNBst-JHibiJgoNA",
    "authDomain": "myestilo-aa9fb.firebaseapp.com" ,
    "databaseURL": "https://myestilo-aa9fb-default-rtdb.firebaseio.com",
    "projectId": "myestilo-aa9fb",
    "storageBucket": "myestilo-aa9fb.appspot.com",
    "messagingSenderId": "348650249197",
    "appId": "1:348650249197:web:73b7e4bb5bd57e923b65e4",
    "measurementId": "G-VX9CD26SSC"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

tz = pytz.timezone('Asia/Singapore')
time = datetime.now(tz).strftime('%d-%m-%Y %H:%M:%S')

cred = credentials.Certificate("myestilo-aa9fb-firebase-adminsdk-aw4hb-b18671d80e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


#for duck-Traditional
url1='https://www.getducked.com/ready-to-wear/limited-edition?category=5068'
req=requests.get(url1)
bsObject=BeautifulSoup(req.text,"html.parser")

# testing for duck
nameT = bsObject.find_all('h2', 'fs-lg-6 flex-fill m-0 plpProductName')
sellpriceT = bsObject.find_all('div', 'fs--1 fw-normal price-adjustment')

nameLoopT = [ namesTraditional.text for namesTraditional in nameT]
sellpriceLoopT = [sellTraditional.text for sellTraditional in sellpriceT]

datawebsite1 = {
    'item_Name' : nameLoopT,
    'item_Price' : sellpriceLoopT
}

lenNameT = len(nameLoopT)
lenPriceT = len(sellpriceLoopT)


#for duck-comfort
url2='https://www.getducked.com/ready-to-wear/tops'
req=requests.get(url2)
bs=BeautifulSoup(req.text,"html.parser")

nameC = bs.find_all('h2', 'fs-lg-6 flex-fill m-0 plpProductName')
sellpriceC = bs.find_all('div', 'fs--1 fw-normal price-adjustment')

nameLoopC = [names.text for names in nameC]
sellpriceLoopC = [sell.text for sell in sellpriceC]

datawebsite2 = {
    'item_Name' : nameLoopC,
    'item_Price' : sellpriceLoopC
}

lenNameC = len(nameLoopC)
lenPriceC = len(sellpriceLoopC)

#for duck-evening
url3='https://www.getducked.com/ready-to-wear/dresses'
req=requests.get(url3)
obj=BeautifulSoup(req.text,"html.parser")

nameE = obj.find_all('h2', 'fs-lg-6 flex-fill m-0 plpProductName')
sellpriceE = obj.find_all('div', 'fs--1 fw-normal price-adjustment')

nameLoopE = [names.text for names in nameE]
sellpriceLoopE = [sell.text for sell in sellpriceE]

datawebsite3 = {
    'item_Name' : nameLoopE,
    'item_Price' : sellpriceLoopE
}

lenNameE = len(nameLoopE)
lenPriceE = len(sellpriceLoopE)


#for lilit-comfort
url4='https://www.lilitstore.com/apparel/tops?category=5415%2C5388'
req=requests.get(url4)
bsO=BeautifulSoup(req.text,"html.parser")

# testing for lilit
nameCC = bsO.find_all('h2', 'fs-lg-6 flex-fill fw-lighter m-0 plpProductName')
priceC = bsO.find_all('div', 'fs--1 fw-normal')

nameLoopCC = [names.text for names in nameCC]
priceLoopC = [sell.text for sell in priceC]

datawebsite4 = {
    'item_Name' : nameLoopCC,
    'item_Price' : priceLoopC
}

lenNameCC = len(nameLoopCC)
lenPriceCC = len(priceLoopC)


#for lilit-Traditional
url5='https://www.lilitstore.com/collections?category=4844'
req=requests.get(url5)
bsOb=BeautifulSoup(req.text,"html.parser")
nameTT = bsOb.find_all('h2', 'fs-lg-6 flex-fill fw-lighter m-0 plpProductName')
priceT = bsOb.find_all('div', 'fs--1 fw-normal')

nameLoopTT = [names.text for names in nameTT]
priceLoopT = [sell.text for sell in priceT]

datawebsite5 = {
    'item_Name' : nameLoopTT,
    'item_Price' : priceLoopT
}

lenNameTT = len(nameLoopTT)
lenPriceTT = len(priceLoopT)

#for LIIT-evening
url6='https://www.lilitstore.com/apparel/dresses?category=5376'
req=requests.get(url6)
bObj=BeautifulSoup(req.text,"html.parser")

nameEE = bObj.find_all('h2', 'fs-lg-6 flex-fill fw-lighter m-0 plpProductName')
priceE = bObj.find_all('div', 'fs--1 fw-normal')

nameLoopEE = [names.text for names in nameEE]
priceLoopE = [sell.text for sell in priceE]

datawebsite6 = {
    'item_Name' : nameLoopEE,
    'item_Price' : priceLoopE
}

lenNameEE = len(nameLoopEE)
lenPriceEE = len(priceLoopE)


#for naelofar
url7='https://my.naelofar.com/clothing/kaftan'
req=requests.get(url7)
bsObj=BeautifulSoup(req.text,"html.parser")

nameN = bsObj.find_all('a', 'product-item-link')
priceN = bsObj.find_all('span', 'price')

nameLoopN = [names.text for names in nameN]
priceLoopN = [sell.text for sell in priceN]

datawebsite7 = {
    'item_Name' : nameLoopN,
    'item_Price' : priceLoopN
}

lenNameN = len(nameLoopN)
lenPriceN = len(priceLoopN)

def format_server_time():
    server_time = time.localtime()
    return time.strftime("%I : %M :%S %p", server_time)

# function for login
@app.route('/', methods=['GET', 'POST'])
def index():
	unsuccessful = 'Please check your credentials'
	successful = 'Login successful'
	if request.method == 'POST':
		email = request.form['user_email']
		password = request.form['user_password']
		try:
			auth.sign_in_with_email_and_password(email, password)
			return render_template('home.html', s=successful)
		except:
			return render_template('main.html', us=unsuccessful)
	return render_template('main.html')

# function for logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	return render_template('main.html')   


@app.route('/home' )    
def home():
	return render_template('home.html')

@app.route('/download_file')
def download_file():
    path = "MyEstilo.apk"
    return send_file(path, as_attachment=True)    

# function for display result for ducked.com
@app.route('/resultT1', methods=['GET', 'POST'])
def resultTraditional():
    def saveBottom(collection_id, document_id, datawebsite1):
        db.collection(collection_id).document(document_id).set(datawebsite1)
    saveBottom(
        collection_id = "Traditional",
        document_id = f"{time}",
        datawebsite1=datawebsite1
    )
    return render_template('resultTraditional.html', lenNameT=lenNameT, lenPriceT=lenPriceT, nameLoopT=nameLoopT, sellpriceLoopT=sellpriceLoopT)

@app.route('/resultC1', methods=['GET', 'POST'])
def resultComfort():
    def saveTop(collection_id, document_id, datawebsite2):
        db.collection(collection_id).document(document_id).set(datawebsite2)
    saveTop(
        collection_id = "Comfort",
        document_id = f"{time}",
        datawebsite2=datawebsite2
    )
    return render_template('resultComfort.html', lenNameC=lenNameC,lenPriceC=lenPriceC, nameLoopC=nameLoopC, sellpriceLoopC=sellpriceLoopC)


@app.route('/resultE1', methods=['GET', 'POST'])
def resultEvening():
    def saveTop(collection_id, document_id, datawebsite3):
        db.collection(collection_id).document(document_id).set(datawebsite3)
    saveTop(
        collection_id = "Evening",
        document_id = f"{time}",
        datawebsite3=datawebsite3
    )
    return render_template('resultEvening.html', lenNameE=lenNameE,lenPriceE=lenPriceE, nameLoopE=nameLoopE, sellpriceLoopE=sellpriceLoopE)

# function for display result for lilit.com
@app.route('/resultC2', methods=['GET', 'POST'])
def resultComfortLilit():
    def saveTop(collection_id, document_id, datawebsite4):
        db.collection(collection_id).document(document_id).set(datawebsite4)
    saveTop(
        collection_id = "Comfort",
        document_id = f"{time}",
        datawebsite4=datawebsite4
    )
    return render_template('resultLilitC.html', lenNameCC=lenNameCC,lenPriceCC=lenPriceCC, nameLoopCC=nameLoopCC, priceLoopC= priceLoopC)

@app.route('/resultT2', methods=['GET', 'POST'])
def resultTraditionalLilit():
    def saveBottom(collection_id, document_id, datawebsite5):
        db.collection(collection_id).document(document_id).set(datawebsite5)
    saveBottom(
        collection_id = "Traditional",
        document_id = f"{time}",
        datawebsite5=datawebsite5
    )
    return render_template('resultLilitT.html', lenNameTT=lenNameTT, lenPriceTT=lenPriceTT, nameLoopTT=nameLoopTT, priceLoopT=priceLoopT)


@app.route('/resultE2', methods=['GET', 'POST'])
def resultEveningLilit():
    def saveTop(collection_id, document_id, datawebsite6):
        db.collection(collection_id).document(document_id).set(datawebsite6)
    saveTop(
        collection_id = "Evening",
        document_id = f"{time}",
        datawebsite6=datawebsite6
    )
    return render_template('resultLilitE.html', lenNameEE=lenNameEE,lenPriceEE=lenPriceEE, nameLoopEE=nameLoopEE,priceLoopE=priceLoopE)

# function for display result for naelofar
@app.route('/resultT3', methods=['GET', 'POST'])
def resultNaelofar():
    def saveTop(collection_id, document_id, datawebsite):
        db.collection(collection_id).document(document_id).set(datawebsite)
    saveTop(
        collection_id = "Traditional",
        document_id = f"{time}",
        datawebsite=datawebsite7
    )
    return render_template('resultNaelofar.html', lenNameN=lenNameN,lenPriceN=lenPriceN, nameLoopN=nameLoopN,priceLoopN=priceLoopN)


if __name__ == '__main__':
	app.run(debug=True)
    

