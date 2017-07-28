from pithy import *
from flask import Flask, redirect, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the DSLR interface.<br/><br/>View the camera summary <a href="http://127.0.0.1:5000/summary">here</a>.<br/>View the current configuration <a href="http://127.0.0.1:5000/getConfig">here</a>.<br/><br/>To change the configuration, go <a href="http://127.0.0.1:5000/setConfig">here</a>.'

@app.route('/summary')
def summary():
    text=subprocess.Popen(["gphoto2","--summary"],stdout=subprocess.PIPE)
    output = text.stdout.read()
    return output

@app.route('/setConfig')
def setConfig():
    return render_template('my-form.html')

@app.route('/getConfig')
def getConfig():
    
    bar=subprocess.Popen(["gphoto2","--get-config=/main/imgsettings/iso"],stdout=subprocess.PIPE)
    getiso = (bar.stdout.read().split('\n'))[2][9:]

    bar=subprocess.Popen(["gphoto2","--get-config=/main/imgsettings/whitebalance"],stdout=subprocess.PIPE)
    getwhite = (bar.stdout.read().split('\n'))[2][9:]
    
    bar=subprocess.Popen(["gphoto2","--get-config=/main/capturesettings/f-number"],stdout=subprocess.PIPE)
    getaperture = (bar.stdout.read().split('\n'))[2][9:]
    
    bar=subprocess.Popen(["gphoto2","--get-config=/main/capturesettings/shutterspeed"],stdout=subprocess.PIPE)
    getshutter = (bar.stdout.read().split('\n'))[2][9:]
    
    return 'ISO: ' + getiso + '<br/>' + 'White Balance: ' + getwhite + '<br/>' + 'Aperture: ' + getaperture + '<br/>' + 'Shutter Speed: ' + getshutter + '<br/><br/>Click <a href="http://127.0.0.1:5000/">here</a> to go back home or <a href="http://127.0.0.1:5000/setConfig">here</a> to change the configuration.'

@app.route('/changeConfig', methods = ['POST'])
def changeConfig():
    iso = request.form['ISO']
    subprocess.call("gphoto2 --set-config=/main/imgsettings/iso="+iso, shell=True)
    
    white = request.form['WhiteBalance']
    subprocess.call("gphoto2 --set-config=/main/imgsettings/whitebalance="+white, shell=True)

    aperture = request.form['F-Number']
    subprocess.call("gphoto2 --set-config=/main/capturesettings/f-number="+aperture, shell=True)

    shutter = request.form['Shutter Speed']
    subprocess.call("gphoto2 --set-config=/main/capturesettings/shutterspeed="+shutter, shell=True)
    
    return redirect('/getConfig')
