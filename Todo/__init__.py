import functools
import os
import psycopg2
from flask import Flask, render_template,request,url_for,jsonify
from flask_login import LoginManager,login_user
from flask import Blueprint,flash,session,redirect,g


def create_app():
   app = Flask("Todo")
   
   app.config.from_mapping(
    DATABASE="list",  
    SECRET_KEY="uni" )
    
   from . import task 
   app.register_blueprint(task.bp)
   
   from . import db
   db.init_app(app)
   
   
   def login_required(view):
    """Redirecting to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('home'))

        return view(**kwargs)

    return wrapped_view
    
 
   
   @app.route("/")
   def home():
    return render_template("index.html")
   
   @app.route("/login",methods=["GET","POST"])
   def login():
     if request.method == "POST":
       username=request.form.get('username')
       password=request.form.get('password')
       conn = db.get_db()
       error = None
       cursor= conn.cursor()
       cursor.execute("select username,password,id from people where username=%s",(username))
       data = cursor.fetchone()
       received_username=data[1]
       received_password=data[0]
      
       if (received_username is not None and received_password==password):
          session.clear()
          session["user_id"] = data[2]
          return redirect(url_for('task.dashboard'))
       else:
         error="Invalid username or Password"
     return render_template("index.html", error=error)
     """
       
       cursor= conn.cursor()
       cursor.execute("select o.username,o.password from people o where o.username=%s",(username))
       data = cursor.fetchone()
       received_username=data[0]
       received_password=data[1]
       error_message = "Invalid username or Password"
      
       login_user(email)
       return redirect(url_for('bp.dashboard'))"""
     
     
      
     
   @app.route("/register",methods=["GET", "POST"])
   def signup():
     if request.method == "POST":
       conn=db.get_db()
       cursor=conn.cursor()
       email=request.form.get('email')
       username=request.form.get('username')
       password=request.form.get('password')
       error=None
       if(not email or not username or not password):
           error ="Fields cannot be left empty."

       if error is None:  
         cursor.execute("insert into user(username,password) values(%s,%s)",(username,password))
         conn.commit()
         conn.close()
         return redirect(url_for('login'))

       flash(error)
       return render_template("index.html")
   return app  

