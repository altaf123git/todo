from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
   
class Register(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    mobile = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    
    
def __repr__(self) -> str:
        return f"{self.sno} {self.title}"

@app.route('/',methods=['GET', 'POST'])
def first():
    return render_template('first.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    data=request.form.uname
    print(data)
    users=Register.query.all()
    return render_template('login.html',users=users, xyz='abcd')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        name=request.form['uname']
        email=request.form['email']
        mobile=request.form['mobile']
        password=request.form['upass']
        todo = Register(name=name, email=email, mobile=mobile, password=password)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
       title=request.form['title']
       desc=request.form['desc']
       if len(title)==0 or len(desc)==0:
           return redirect('/home')
       else:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
       
    alltodo=Todo.query.all()
    return render_template('index.html', alltodo=alltodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/") 

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']
        todo= Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    todo= Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/c')
def create():
    db.create_all()
    return "created successfully"

if __name__=="__main__":
    app.run(debug=True , port=7000)
