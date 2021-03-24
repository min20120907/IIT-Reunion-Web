import os
from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import uuid

# Some format and sizes limits
UPLOAD_FOLDER = 'imgs/'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])
MAX_CONTENT_LENGTH = 10*1024*1024   # 10MB

# Actual initialization of web interface
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

#MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "jefflin123"
app.config["MYSQL_DB"] = "IIT"
mysql = MySQL(app)

# Check validity of the file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def query(email):
    sql = "SELECT PIC_1, PIC_2 FROM Photos WHERE Email='"+str(email+"'")
    cur = mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data

def update(UUID,img1, img2):
    sql = "UPDATE Photos SET PIC_1=%s, PIC_2=%s WHERE UUID=%s";
    cur = mysql.connection.cursor()
    cur.execute(sql, (img1,img2,UUID))
    mysql.connection.commit()

def insert(datas):
    sql = 'INSERT INTO Photos (UUID,Email,PIC_1, PIC_2) VALUES (%s, %s, %s, %s)'
    cur = mysql.connection.cursor()
    cur.execute(sql, datas)
    mysql.connection.commit()


@app.route('/', methods=["POST","GET"])
def index():
    if request.method == 'POST':
        if request.values['send']=='送出':
            email = request.values['email']
            print(query(email))
            img1 = request.files['img1']
            img2 = request.files['img2']
            # Save image1
            if img1 and allowed_file(img1.filename):
                filename = secure_filename(img1.filename)
                print(filename)
                img1.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                   filename))
            # Save image2
            if img2 and allowed_file(img2.filename):
                filename = secure_filename(img2.filename)
                print(filename)
                img2.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))

            uuid = request.values['UUID']
            insert(("ssfdsdfsdsdfsfd",email,img1,img2))

    return render_template("form.html")

if __name__ == '__main__':
    app.run()

