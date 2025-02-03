
# from crypt import methods
from unicodedata import name
from argon2 import hash_password
import bcrypt
from flask import render_template,request,session,redirect,url_for,flash
from flask_cors import CORS,cross_origin
from Buyandsell import db,app,bcrypt
from .forms import RegistrationForm, LoginForm
from flask import Flask
from .models import User
# from mysqlx import Column
import pandas as pd
import numpy as np
import pickle
import os


@app.route('/')
def homepage():
    return render_template('homepage.html')

#********************************************************************************************
model=pickle.load(open('LinearRegressionModel.pkl','rb'))
@app.route('/prediction',methods=['GET','POST'])
def index():
    app=Flask(__name__)
    cors=CORS(app)
    
    car=pd.read_csv('Cleaned_Car_data.csv')
    companies=sorted(car['company'].unique())
    car_models=sorted(car['name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()

    companies.insert(0,'Select Company')
    return render_template('index.html',companies=companies, car_models=car_models, years=year,fuel_types=fuel_type)


@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():

    company=request.form.get('company')

    car_model=request.form.get('car_models')
    year=request.form.get('year')
    fuel_type=request.form.get('fuel_type')
    driven=request.form.get('kilo_driven')

    prediction=model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                              data=np.array([car_model,company,year,driven,fuel_type]).reshape(1, 5)))
    print(prediction)

    return str(np.round(prediction[0],2))
#********************************************************************************************


#********************************************************************************************
@app.route('/loginpage', methods =['GET','POST'])
def login():
    form=LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email']= form.email.data
            flash(f'Welcome {form.email.data} You are logged in','success')
            return redirect(request.args.get('next') or url_for('message'))
        else:
            flash("Wrong password please try again")
    return render_template('loginpage.html',form=form)

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'please login first')
        return redirect(url_for('login'))
        
    return render_template('__index.html')


@app.route('/message')
def message():
    return render_template('__message.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password= bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome{form.name.data}!,Thanks for registering')
        return redirect(url_for('message'))
    return render_template('signinpage.html',form=form)

#********************************************************************************************

