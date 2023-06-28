from flask import Flask, Blueprint, render_template, url_for, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manager.db'
db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False, default='No First Name')
    last_name = db.Column(db.String(60), nullable=False, default='No Last Name')
    event_type = db.Column(db.String(80), nullable=False, default='No Event Type')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
        tasks = Client.query.order_by(Client.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/manager', methods=['POST', 'GET'])
def manager():
    if request.method == 'POST':
        clientpulled = request.form.get('clientDropdown')
        try:
            return redirect('/manager')
        except:
            return 'That didnt work.'
    else:
        tasks = Client.query.order_by(Client.date_created).all()
        return render_template('manager.html', tasks=tasks)

@app.route('/client', methods=['POST', 'GET'])
def client():
        tasks = Client.query.order_by(Client.date_created).all()
        return render_template('client.html', tasks=tasks)
    
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        eventtype = request.form['eventtypecontent']
        firstname = request.form['firstnamecontent']
        lastname = request.form['lastnamecontent']
        new_task = Client(event_type=eventtype, first_name=firstname, last_name=lastname)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/manager')
        except:
            return 'There was an issue submitting your information.'
    else:
        tasks = Client.query.order_by(Client.date_created).all()
        return render_template('register.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Client.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/manager')
    except:
        return 'There was an issue deleting the section.'
    
@app.route('/client/<int:id>', methods=['GET', 'POST'])
def chooseclient(id):
    task = Client.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['eventtypecontent']

        try:
            db.session.commit()
            return redirect('/client/<int:id>')
        except:
            return 'There was an issue updating the section.'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)