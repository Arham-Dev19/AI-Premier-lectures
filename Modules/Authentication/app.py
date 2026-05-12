from flask import Flask
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.data import data_bp
# from routes.chart import chart_bp

app = Flask(__name__)
app.secret_key = "secret123"

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(data_bp)
#app.register_blueprint(chart_bp)

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, render_template, request, redirect, session
# from models import users_collection
# from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash
# app = Flask(__name__)
# app.secret_key = "seret123"

@app.route('/register' ,methods=['GET','POST'])
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

@app.route('/',methods=['GET','POST'])
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

# ------admin dashboard--------
@app.route("/admin")
def admin():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html', name=session['user'])
    return redirect('/')

# ------student dashboard--------
@app.route("/student")
def student():
    if 'role' in session and session['role'] == 'student':
        return render_template('user_dashboard.html', name=session['user'])
    return redirect('/')

# ------teacher dashboard--------
@app.route("/teacher")
def teacher():
    if 'role' in session and session['role'] == 'teacher':
        return render_template('teacher_dashboard.html', name=session['user'])
    return redirect('/')



# AUTHN CHECK
def admin_required():
    return 'role' in session and session['role'] == 'admin'


# VIEW USERS
@app.route('/manage-users')
def manage_users():
    if not admin_required():
        return redirect('/')

    users = list(users_collection.find())
    return render_template('manage_users.html', users=users)


# ADD USER
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if not admin_required():
        return redirect('/')

    if request.method == 'POST':
        users_collection.insert_one({
            "name": request.form['name'],
            "email": request.form['email'],
            "password": request.form['password'],
            "role": request.form['role']
        })
        return redirect('/manage-users')

    return render_template('add_user.html')


#----------------edit user ka route----------------
@app.route('/edit-user/<id>', methods = ['GET','POST'])
def edit_user(id):
    if not admin_required():
        return redirect('/')

    user = users_collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        users_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.form["name"],
                "email": request.form["email"],
                "role": request.form["role"]
            }}
        )
        return redirect("/manage-users")

    return render_template('edit_user.html', user=user)

#----------------DELETE USER----------------
@app.route('/delete-user/<id>')
def delete_user(id):
    if not admin_required():
        return redirect('/')

    users_collection.delete_one({"_id": ObjectId(id)})

    return redirect('/manage-users')

if __name__ == "__main__":
    app.run(debug=True)