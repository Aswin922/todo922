from flask import Blueprint,g,session,url_for,jsonify
from flask import render_template, request, redirect
from flask_login import login_user,logout_user
from . import db
import datetime


bp = Blueprint("task", "task", url_prefix="/task")


@bp.route("/",methods=['GET','POST'])
def dashboard():
     today =datetime.datetime.today()
     user_id = session.get("user_id")
     datas=None
     conn=db.get_db()
     cursor=conn.cursor()
     
     cursor.execute("select o.taskname,o.duedate,o.overdue from task o where o.taskrec =%s order by o.duedate",(user_id,))
     datas=cursor.fetchone()
     
     if datas is not None:
        conn=db.get_db()
        cursor=conn.cursor()
        cursor.execute("select o.taskname,o.duedate,o.overdue from task o where o.taskrec =%s order by o.duedate",(user_id,))
        datas=cursor.fetchall()
        
        conn=db.get_db()
        cursor=conn.cursor()
        cursor.execute("select o.duedate from task o where o.taskrec =%s ",(user_id,))
        duedates=(x[0] for x in cursor.fetchall())
        for duedate in duedates:
          datetime_object = datetime.datetime.strptime(duedate,"%Y-%m-%d")
          if datetime_object< today:
            cursor.execute("update task set overdue=%s where taskrec=%s and duedate=%s",('y',user_id,duedate))
            conn.commit()
          else:
             cursor.execute("update task set overdue=%s where taskrec=%s and duedate=%s",('n',user_id,duedate))
             conn.commit()
        conn=db.get_db()
        cursor=conn.cursor()
     
        cursor.execute("select o.taskname,o.duedate,o.overdue,o.id from task o where o.taskrec =%s order by o.duedate",(user_id,))
        datas=cursor.fetchall()
        return render_template("task.html",datas=datas)  
     return render_template("task.html")    


     
@bp.route("/logout")
def logout():
   
    session.clear()
    return redirect(url_for('home'))


@bp.route("/add",methods=['GET','POST'])
def addtask():   
     user_id = session.get("user_id")
     
     if request.method == "POST":
       conn=db.get_db()
       cursor=conn.cursor()
       task=request.form.get('task')
       date=request.form.get('date')
       error=None
       if(not task or not date):
           error ="Enter Task and Due Date"

       if error is None:  
         cursor.execute("insert into task(taskname,duedate,taskrec) values(%s,%s,%s)",(task,date,user_id))
         conn.commit() 
     return redirect(url_for('task.dashboard'))


@bp.route("/delete/<id>",methods=['GET','POST'])
def delete(id):
  conn=db.get_db()
  cursor=conn.cursor()
  cursor.execute("delete from task where id=%s",(id,))
  conn.commit()
  return redirect(url_for('task.dashboard'))
