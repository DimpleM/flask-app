from typing import List, Dict
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import json
import re

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'users'
}
app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))
  
@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user_detail WHERE name = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account[0]
            return redirect(url_for('home'))
        else:
            return redirect(url_for('register'))
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
#    session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user_detail WHERE name = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Username already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user_detail VALUES ( %s, %s, %s)', (username, password, email,))
            connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/home')
def home():
    if 'loggedin' in session:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user_detail where name != %s',(session['username'],))
        accounts = cursor.fetchall()
        if accounts:
            return render_template('home.html', username=session['username'], accounts=accounts)
        else:
            return render_template('home.html', username=session['username'], accounts='')

    return redirect(url_for('login'))

@app.route('/delete', methods=['POST'])
def delete_entry():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        username = request.form['username']
        cursor.execute('delete from  user_detail where name = %s',(username,))
        connection.commit()
        result = { 'status':1, 'message': "Post Deleted" }
    except Exception as e:
        result = { 'status':0, 'message': repr(e) }
    return json.dumps(result) 
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


