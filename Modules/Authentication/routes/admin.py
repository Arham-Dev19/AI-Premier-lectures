from flask import Flask,Blueprint, render_template, request,redirect , session
from models import users_collection
from bson.objectid import ObjectId
admin_bp = Blueprint('admin',__name__)

@admin_bp.route("/admin")
def admin():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html',name=session['user'])
    return redirect('/')

# AUTHN CHECK
def admin_required():
    return 'role' in session and session['role'] == 'admin'


# VIEW USERS
@admin_bp.route('/manage-users')
def manage_users():
    if not admin_required():
        return redirect('/')

    users = list(users_collection.find())
    return render_template('manage_users.html', users=users)


# ADD USER
@admin_bp.route('/add-user', methods=['GET', 'POST'])
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
@admin_bp.route('/edit-user/<id>', methods = ['GET','POST'])
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
@admin_bp.route('/delete-user/<id>')
def delete_user(id):
    if not admin_required():
        return redirect('/')

    users_collection.delete_one({"_id": ObjectId(id)})

    return redirect('/manage-users')


# ------logout--------
@admin_bp.route("/logout")
def logout():
        session.clear()
        return redirect('/')