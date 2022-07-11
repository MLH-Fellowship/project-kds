import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)


isKayla = True

@app.route('/')
def kaitlyn_index():
    return render_template('kaitlyn_index.html', url=os.getenv("URL"))

@app.route('/kaitlyn_about')
def kaitlyn_about():
    return render_template('kaitlyn_about.html', url=os.getenv("URL"))

@app.route('/kaitlyn_experience')
def kaitlyn_experience():
    return render_template('kaitlyn_experience.html', url=os.getenv("URL"))

@app.route('/kaitlyn_education')
def kaitlyn_education():
    return render_template('kaitlyn_education.html', url=os.getenv("URL"))

@app.route('/kaitlyn_hobbies')
def kaitlyn_hobbies():
    return render_template('kaitlyn_hobbies.html', url=os.getenv("URL"))

@app.route('/kaitlyn_places')
def kaitlyn_places():
    return render_template('kaitlyn_places.html', url=os.getenv("URL"))

# app = Flask(__name__)
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
        mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST"),
            port=3306
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    if "name" not in request.form:
        return "Invalid name", 400
    else:
        name = request.form['name']
        if name == "":
            return "Invalid name", 400
    email = request.form['email']
    if "email" not in request.form:
        return "Invalid email", 400
    else:
        email = request.form['email']
        if email == "" or "@" not in email:
            return "Invalid email", 400
    content = request.form['content']
    if content == "":
        return "Invalid content", 400
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    posts = {

        'timeline_posts': [
            model_to_dict(p)
            for p in
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
    return posts

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():

    posts = {

        'timeline_posts': [
            model_to_dict(p)
            for p in
TimelinePost.select()
        ]
    }    
    the_id = posts['timeline_posts'][0]["id"]
    TimelinePost.delete_by_id(the_id)
    return "Successfully deleted " + str(the_id) + "\n"

@app.route('/timeline')
def timeline():
    
    return render_template('timeline.html', title="Timeline")