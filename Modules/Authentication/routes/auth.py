from flask import Flask,Blueprint, render_template, request,redirect , session
from models import users_collection
auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/register' ,methods=['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        users_collection.insert_one({
            "name":name,
            "email":email,
            "password":password,
            "role":role
        })
        
        return redirect('/')
    return render_template('register.html')

@auth_bp.route('/',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        user = users_collection.find_one({"email":email, "password":password})
        
        if user:
            session['user'] = user['name']
            session['role'] = user['role']
            
            if user['role'] == 'admin':
                return redirect("/admin")
            elif user ['role'] == 'teacher':
                return redirect("/teacher")
            else:
                return redirect("/student")
        else:
            return "Invalid credentials"
    return render_template("login.html")