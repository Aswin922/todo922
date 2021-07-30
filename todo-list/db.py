import psycopg2
import click 
from flask import current_app, g
from flask.cli import with_appcontext
import urllib.parse as urlparse




def get_db():
    if 'db' not in g:
        url = urlparse.urlparse('postgres://xzazucmbfvomqo:a0b4236392644438b0eed7f8756cc537ea582f7f062a2d95052009dc36e49293@ec2-54-211-160-34.compute-1.amazonaws.com:5432/dd5lqk4v8arqlg')
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        g.db= psycopg2.connect(
           dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            
            )
    return g.db



def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()



def init_db():
    db = get_db()
    f = current_app.open_resource("todo.sql")
    sql_code = f.read().decode("ascii")
    cur = db.cursor()
    cur.execute(sql_code)
    cur.close()
    db.commit()
    close_db()



@click.command('initdb', help="initialise the database") 
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Database initialised.') 



def init_app(app):
    
    app.cli.add_command(init_db_command)
    
