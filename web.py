import flask
from flask import render_template, request
from app import app
#import plotly as Plotly

import dbhommat as dbh

@app.route("/")
def index():
    return render_template("index.html")

#@app.route("/plot")
#def plotterpage():
#    return render_template("plotter.html")

@app.route("/chartly")
def chartlypage():
    return render_template("chartly.html")

@app.route("/search")
def searchpage():
    return render_template("search.html")

@app.route("/result", methods=["POST"])
def  result():
    print(request.form["county"])
    return render_template("result.html")





#validaatiota tuolle partial match stringille!!!!!