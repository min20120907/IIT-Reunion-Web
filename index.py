import os
from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import uuid
import glob
import smtplib, ssl

smtp_server = "localhost"
port = 25  # For starttls
sender_email = "reunion@alumni.iit.tku.edu.tw"

# Create a secure SSL context
message = """\
Subject: Verify Email

Please enter the following UUID for the next uploads.
UUID: """

# Some format and sizes limits
UPLOAD_FOLDER = '/imgs/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
MAX_CONTENT_LENGTH = 10*1024*1024   # 10MB

# Actual initialization of web interface
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd() + UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "reunion"
app.config["MYSQL_PASSWORD"] = "password"
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
    return data

def getPic1(UUID):
    sql = "SELECT PIC_1 FROM Photos WHERE UUID='"+str(UUID)+"'"
    cur =mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data[0][0]

def getPic2(UUID):
    sql = "SELECT PIC_2 FROM Photos WHERE UUID='"+str(UUID)+"'"
    cur =mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data[0][0]
    

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
        if request.values['send']=='submit':
            email = request.values['email']
            img1 = request.files['img1']
            img2 = request.files['img2']
            img1_p = ""
            img2_p = ""
            uuid_usr = request.values['UUID']
            # print(uuid_usr)
            # print(getUUID(email))
            # Check whether the data is existed
            query_r = query(email)
            if query_r == ():
                print("no uuid")
                # Save image1
                if img1 and allowed_file(img1.filename):
                    filename = secure_filename(str(uuid.uuid4())+"."+img1.filename.rsplit('.', 1)[1])
                    img1_p = filename
                    img1.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                       filename))
                # Save image2
                if img2 and allowed_file(img2.filename):
                    filename = secure_filename(str(uuid.uuid4())+"."+img2.filename.rsplit('.', 1)[1])
                    img2.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                       filename))
                    img2_p = filename
                insert((str(uuid.uuid4()),email,img1_p,img2_p)) 
                try:
                    server = smtplib.SMTP(smtp_server,port)
                    server.ehlo() # Can be omitted
                    server.sendmail(sender_email, email, message+str(uuid.uuid4()))
                    # TODO: Send email here
                except Exception as e:
                    # Print any error messages to stdout
                    print(e)
                finally:
                    server.quit() 
            elif uuid_usr == getUUID(email)[0][0]:
                print("enter UUID")
                print(img1)
                print(img2)
                # Save image1
                
                if img1 and allowed_file(img1.filename):
                    print("removing img1")
                    os.remove(app.config['UPLOAD_FOLDER']+str(getPic1(uuid_usr)))
                    print(app.config['UPLOAD_FOLDER']+str(getPic1(uuid_usr)))
                    filename = secure_filename(str(getPic1(uuid_usr)).rsplit('.',1)[0]+"."+img1.filename.rsplit('.', 1)[1])
                    img1.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                       filename))
                    img1_p=filename
                # Save image2
                if img2 and allowed_file(img2.filename):
                    print("removing img2")
                    os.remove(app.config['UPLOAD_FOLDER']+str(getPic2(uuid_usr)))
                    print(app.config['UPLOAD_FOLDER']+str(getPic2(uuid_usr)))
                    filename = secure_filename(str(getPic2(uuid_usr)).rsplit('.',1)[0]+"."+img2.filename.rsplit('.', 1)[1])
                    img2.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                       filename))
                    img2_p=filename
                update(uuid_usr, img1_p, img2_p)
                
    return render_template("form.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=("/etc/letsencrypt/live/alumni.iit.tku.edu.tw/fullchain.pem","/etc/letsencrypt/live/alumni.iit.tku.edu.tw/privkey.pem"), port=443)

