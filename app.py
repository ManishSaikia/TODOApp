from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'{self.sno} - {self.title}'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTODO = Todo.query.all()
    return render_template('index.html', allTODO=allTODO)

@app.route('/update/<int:num>', methods=['GET', 'POSt'])
def update(num):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=num).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    todo = Todo.query.filter_by(sno=num).first()
    return render_template('update.html', todo=todo)
    

@app.route('/delete/<int:num>')
def delete(num):
    todo = Todo.query.filter_by(sno=num).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False, port=8000)