from flask import Flask, render_template, request, redirect,session
from models import users_collection
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash

# Start flask
app = Flask(__name__)

# Involve secret key
app.secret_key = "secret123"

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": password,
            "role": role
        })

        return redirect('/login')

    return render_template("register.html")
        
        
# login ka route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({"email":email, "password":password})

        # ab role base screens change hogi user ki
        if user:
            session['user'] = user['name']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect("/admin")
            elif user['role'] == 'teacher':
                return redirect("/teacher")
            else:
                return redirect('/student')
        else:
            return "Invalid credentials😞"

    return render_template("login.html")


#-------------admin dashboard-------------
@app.route("/admin")
def admin():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html', name=session['user'])
    return redirect('/')

#-------------student dashboard-------------
@app.route("/student")
def student():
    if 'role' in session and session['role'] == 'student':
        return render_template('user_dashboard.html', name=session['user'])
    return redirect('/')

#-------------teacher dashboard-------------
@app.route("/teacher")
def teacher():
    if 'role' in session and session['role'] == 'teacher':
        return render_template('teacher_dashboard.html', name=session['user'])
    return redirect('/')

#-------------logout-------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#-------------admin check------------------
def admin_required():
    return 'role' in session and session['role'] == 'admin'


#-------------view users-------------------
@app.route('/manage-users')
def manage_users():

    if not admin_required():
        return redirect('/')

    users = list(users_collection.find())

    return render_template('manage_user.html', users=users)


#-------------add user ka route-------------
@app.route('/add-user', methods=['GET', 'POST'])
def add_users():

    if not admin_required():
        return redirect('/')

    if request.method == 'POST':

        users_collection.insert_one({

            "name": request.form['name'],
            "email": request.form['email'],
            "password": request.form['password'],
            "role": request.form['role'],
        })

        return redirect("/manage-users")

    return render_template('add_user.html')



if __name__ == "__main__":
    app.run(debug=True)

