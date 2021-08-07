from flask import Flask, render_template, request,session,url_for,redirect

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)

app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'charan'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        firstName =request.form['first_name']
        lastName = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers_3 VALUES (%s,%s,%s,%s,%s) ", (firstName, lastName ,email,password,confirm_password))
        mysql.connection.commit()
        assert isinstance(cur, object)
        cur.close()
        return 'success'

    return render_template('test.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM MyUsers_3 WHERE email = % s AND password = % s", (email, password,))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug=True
    app.run()
