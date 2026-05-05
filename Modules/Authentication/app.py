from flask import Flask, render_template, request, redirect,session
from models import users_collection

# start flask
app = flask(__name__)

# Involve secret key
app.secret_key = "secret123"

# Register Routes

@app.route('/register' ,Method=['GET','POST'])
def register():
    if request.method == 'POST':
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
        
        return redirect
        
        
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

if __name__ == "__main__":
    app.run(debug=True)