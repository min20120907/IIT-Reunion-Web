from flask import Flask, redirect, url_for, render_template,request
app = Flask(__name__)


@app.route('/', methods=["POST","GET"])
def index():
    return render_template("form.html")

if __name__ == '__main__':
    app.run()

