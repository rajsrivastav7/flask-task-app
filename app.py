import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2305@localhost/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Home Route
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        try:
            title = request.form['title']
            desc = request.form['desc']
            new_task = Task(title=title, desc=desc)
            db.session.add(new_task)
            db.session.commit()
        except Exception as e:
            print(f"Error adding task: {e}")
    allTask = Task.query.all()
    return render_template('index.html', allTask=allTask)

# Show Route
@app.route("/show")
def prods():
    allTask = Task.query.all()
    return "<p>Prods!</p>"

# Update Route
@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    task = Task.query.filter_by(sno=sno).first()
    if not task:
        return "Task not found", 404
    if request.method == 'POST':
        try:
            title = request.form['title']
            desc = request.form['desc']
            task.title = title
            task.desc = desc
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error updating task: {e}")
    return render_template('update.html', task=task)

# Delete Route
@app.route("/delete/<int:sno>")
def delete(sno):
    task_to_delete = Task.query.filter_by(sno=sno).first()
    if task_to_delete:
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
        except Exception as e:
            print(f"Error deleting task: {e}")
    return redirect("/")

# All Route (Placeholder)
@app.route("/all")
def all():
    return "<p>All!</p>"

# Code to create database tables when running the script
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database created successfully!")
    app.run(debug=True)
