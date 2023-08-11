from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)


conn=mysql.connector.connect(user='root' ,host='localhost',database='coding',password='')#, password=''
cursor=conn.cursor()

@app.route('/')
def login():
    if 'password_required' in session:
        return render_template("login_with_password.html")
    return render_template("login.html")



    # return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template("home.html")
    else:
        return redirect('/')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    pasword=request.form.get('password')
    
    cursor.execute("""SELECT *FROM `users` WHERE `email` LIKE '{}' AND `password`LIKE '{}'""".format(email,pasword))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect("home")
    else:
        return redirect('/')



@app.route('/add_user', methods =['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    
    query = "INSERT INTO `USERS` (`name`, `email`, `password`) VALUES ('{}', '{}', '{}')".format(name, email, password)
    cursor.execute(query)
    conn.commit()  # You forgot the parentheses here to call the commit method
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')



if __name__== "__main__":
    app.run(debug=True)
    
    
    
