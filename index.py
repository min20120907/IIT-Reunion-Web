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

def getUUID(email):
    sql = "SELECT UUID FROM Photos WHERE Email='"+str(email+"'")
    cur = mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data[0]

def getPic1(UUID):
    sql = "SELECT PIC_1 FROM Photos WHERE UUID="+str(UUID)
    cur =mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data[0]

def getPic2(UUID):
    sql = "SELECT PIC_2 FROM Photos WHERE UUID="+str(UUID)
    cur =mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data[0]
    

def update(UUID,img1, img2):
    sql = "UPDATE Photos SET PIC_1=%s, PIC_2=%s WHERE UUID=%s"
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
            img1 = request.files['img1']
            img2 = request.files['img2']
            uuid_usr = request.values['UUID']
            # Check whether the data is existed
            query_r = query(email)
            if query == None:
                # Save image1
                if img1 and allowed_file(img1.filename):
                    filename = secure_filename(str(uuid.uuid5())+"."+img1.filename.rsplit('.', 1)[1])
                    print(filename)
                    img1.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                       filename))
                # Save image2
                if img2 and allowed_file():
                    filename = secure_filename(str(uuid.uuid5())+"."+img2.filename.rsplit('.', 1)[1])
                    print(filename)
                    img2.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                       filename))
                insert((str(uuid.uuid5()),email,img1,img2))
            elif uuid_usr == getUUID(email):
                # Save image1
                if img1 and allowed_file(img1.filename):
                    filename = secure_filename(getPic1(uuid_usr)+"."+img1.filename.rsplit('.', 1)[1])
                    print(filename)
                    img1.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                       filename))
                # Save image2
                if img2 and allowed_file():
                    filename = secure_filename(getPic2(uuid_usr)+"."+img2.filename.rsplit('.', 1)[1])
                    print(filename)
                    img2.save(os.path.join(app.config['UPLOAD_FOLDER'],
                update(uuid_usr, img1, img2) 
    return render_template("form.html")

if __name__ == '__main__':
    app.run()

