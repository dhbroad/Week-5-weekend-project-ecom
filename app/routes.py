from app import app
from flask import render_template, redirect, url_for

@app.route('/')
def home():
    return redirect(url_for('ecom.posts'))

    
    # return render_template('index.html', my_list=names)



@app.route('/about')
def iCanNameThisAnything():
    return render_template('about.html')
