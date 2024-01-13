from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["TRACK_MODIFICATION"] = False
app.secret_key ="uiucuh8574t87582&Y$*&Y$&#"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=10)


db = SQLAlchemy(app)

class user(db.Model):
    __tablename__ = 'login_details'
    id = db.Column(db.Integer,primary_key = True)
    user_name = db.Column(db.String(25),nullable=False)
    email = db.Column(db.String(50),nullable = False)
    password = db.Column(db.String(50),nullable = False)

    def __init__(self,email,password,user_name):
        self.email = email
        self.password = password
        self.user_name = user_name

class todo(db.Model):
    __tablename__ = "todo_details"
    lin = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("login_details.id"),nullable=False)
    content = db.Column(db.String(200),nullable=False)
    completed_task = db.Column(db.Boolean ,default = False)

    def __init__(self,user_id,content):
        self.user_id = user_id
        self.content = content

@app.route("/",methods=["GET","POST"])
def login():
    if(not session):
        return render_template("login.html")
    else:
        return redirect(url_for("after_login"))

@app.route("/list")
def list_users():
    print(user.query.all())
    return "iucricviuri"

def check_already_exist(email_id):
    check_user = user.query.filter_by(email= email_id).first()
    if(check_user):
        return check_user
    else:
        return False

@app.route("/signUp",methods=["GET","POST"])
def signUp():
    if(session):
        return redirect(url_for("after_login"))

    if(request.method=="POST"):
        user_name = request.form.get("user-name")
        signup_email = request.form.get("signup-email")
        signup_password = request.form.get("signup-password")
        exist = check_already_exist(signup_email)
        if(exist):
            session["user_name"] = user_name
            session["email_id"] = signup_email
            session["password"] = signup_password
            session["id"] = exist.id
            return redirect(url_for("logged_in"))
        else:
            create_user = user(user_name= user_name,email=signup_email,password=signup_password)
            db.session.add(create_user)
            db.session.commit()
            session["user_name"] = user_name
            session["email_id"] = signup_email
            session["password"] = signup_password
            exist = check_already_exist(signup_email)
            session["id"] = exist.id
            return redirect(url_for("after_login"))
    else:
        return render_template("sign_up.html")


@app.route('/login',methods =["GET","POST"])
def logged_in():
    email = request.form.get("login-email")
    password = request.form.get("login-password")
    print(email)
    print(password)
    exist = check_already_exist(email)
    if(not exist):
        print(exist)
        return redirect(url_for("signUp"))
    else:
        session["user_name"] = exist.user_name
        session["email_id"] = exist.email
        session["password"] = exist.password
        session["id"] = exist.id
        print(exist.email)
        print(exist.password)
        return redirect(url_for("after_login"))

@app.route("/logged",methods=["GET","POST"])
def after_login():
    session.permanent =True
    if(request.method=="POST"):
        todo_content = request.form.get("todo-list")
        print("to do content" ,todo_content)
        add_details = todo(user_id = session["id"],content=todo_content)
        db.session.add(add_details)
        db.session.commit()
        return redirect(url_for("after_login"))

    else:
        if(session):
            # print(session["id"])
            list_items = todo.query.filter_by(user_id = session["id"]).order_by(todo.completed_task4).all()
            # list_items = [for item in list_items]
            print(list_items)
            for items in list_items:
                print(items.lin,items.user_id,items.completed_task)
            return render_template("after_login.html",listOfItems = list_items)
        else:
            return redirect(url_for('logged_in'))

@app.route("/delete_task",methods=["GET","POST"])
def deleteTask():
    if(session):
        task_id = request.form.get("delete_id")  # This gets the value of 'ele.id' from the form
        print(task_id,"delete id")
        todo.query.filter_by(lin=task_id).delete()
        db.session.commit()
        return redirect(url_for("after_login"))
    else:
        return redirect(url_for('logged_in'))

@app.route("/edit_task",methods=["GET","POST"])
def editTask():
    if(session):
        edit_id = request.form.get("edit_id")
        content = request.form.get("edit_content")
        finding_element = todo.query.filter_by(lin = edit_id).first()
        print(finding_element.content,"jref8erjifej8e")
        finding_element.content = content
        db.session.commit()
        return redirect(url_for("after_login"))
    else:
        return redirect(url_for('logged_in'))

@app.route("/logout")
def logout():
    if(session):
        print(session,"session data")
        session.clear()
        print(session,"after session pop")
    return redirect(url_for("login"))


@app.route("/completed_task",methods=["GET","POST"])
def completeTask():
    completed = request.form.get("todo-checkbox")
    print(completed,"complted task ",type(completed))
    id = request.form.get("checkbox-id")
    finding_id=todo.query.filter_by(lin=id).first()
    if(completed=="on"):
        finding_id.completed_task = True
    else:
        finding_id.completed_task = False
    db.session.commit()
    return redirect(url_for("after_login"))

if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
    app.run(debug= True)