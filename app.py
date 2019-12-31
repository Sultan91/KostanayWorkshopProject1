from flask import Flask, render_template, redirect, request, send_from_directory
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from ImageProcessingModule.test import genGrayScale
from ImageProcessingModule.MeanFilter import mean_filter
from ImageProcessingModule.HistogramEqualizer import color_correction
import cv2
import os
import random
import string


def randomString(stringLength=3):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
'''
Idea of the project :
Онлайн калкулятор вложений, кредита
- create flask app: templates, backend (routes)
- module: will do some logic
'''


app = Flask(__name__, static_url_path="", static_folder="static")
# Config for mysql goes here
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1'
app.config['MYSQL_DB'] = 'myFlaskApp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['work_image'] = 'work_image.jpg'
app.config['UPLOAD_FOLDER'] = 'static'
# Initilize mysql
mysql = MySQL()

app.debug=True # To make auto rerun server


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload-image', methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            app.config['work_image'] =  str(randomString())+secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], app.config['work_image'] ))
    return render_template('home.html')


@app.route('/convert2gray', methods=["GET"])
def convert2gray():
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], app.config['work_image']))
    gray = genGrayScale(img)
    gray_name = 'grayScaled'+app.config['work_image']
    cv2.imwrite('static/'+gray_name, gray)
    app.config['work_image'] = gray_name
    return render_template('home.html', output_img=gray_name)


@app.route('/smoothed', methods=["GET"])
def smoothed():
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], app.config['work_image']))
    smooth_img = mean_filter(img)
    smooth_name = 'smooth_'+app.config['work_image']
    cv2.imwrite('static/'+smooth_name, smooth_img)
    return render_template('home.html', output_img=smooth_name)


@app.route('/hist_stabilization', methods=["GET"])
def hist_stabilization():
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], app.config['work_image']))
    trans_img = color_correction(img)
    name = os.path.join('static', 'stabilized'+app.config['work_image'])
    print(name)
    cv2.imwrite(name, trans_img)
    return render_template('home.html', output_img='stabilized'+app.config['work_image'])


if __name__=='__main__':
    app.run()