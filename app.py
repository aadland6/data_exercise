# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 11:14:11 2016

@author: aadlandma
"""
from flask import Flask,render_template 
import os
import os.path
app = Flask(__name__)

@app.route("/females")
def females():
    return render_template("females2.html")
   
@app.route("/males")
def males():
    return render_template("males.html")
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)