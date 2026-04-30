import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename 
app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["ClassE8"]
collection_admission = db["admission"]
product_collection = db["products"]

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Home page (Read all data)
@app.route("/")
def index():
    data = list(collection_admission.find())
    return render_template("index.html", data=data)


# Add new user
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        data = {
            "name": request.form['name'],
            "email": request.form['email'],
            "age": request.form['age'],
            "gender": request.form['gender'],
            "course": request.form["course"],
        }
        collection_admission.insert_one(data)
        return redirect(url_for("index"))
    
    return render_template("add.html")


# Edit user
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    user = collection_admission.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        updated_data = {
            "name": request.form['name'],
            "email": request.form['email'],
            "age": request.form['age'],
            "gender": request.form['gender'],
            "course": request.form["course"],
        }

        collection_admission.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_data}
        )

        return redirect(url_for('index'))

    return render_template('edit.html', user=user)


# Delete user
@app.route("/delete/<id>")
def delete(id):
    collection_admission.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


@app.route('/products')
def products():
    data = list(product_collection.find())
    return render_template('products.html', data = data)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']
        image = request.files['image']

        filename = None

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data = {
            "name": name,
            "price": price,
            "image": filename
        }

        product_collection.insert_one(data)

        return redirect(url_for('products'))

    return render_template('add_product.html')



@app.route('/edit_product/<id>', methods=['GET', 'POST'])
def edit_product(id):
        
        product = product_collection.find_one({"_id": ObjectId(id)})
    
        if request.method == 'POST':
    
            name = request.form['name']
            price = request.form['price']
            image = request.files.get('image')  # ADD THIS
    
            update_data = {
                "name": name,
                "price": price
            }
    
            # IF NEW IMAGE UPLOADED
            if image and image.filename != "":
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                update_data["image"] = filename  # update image in DB
    
            product_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
    
            return redirect(url_for("products"))
        return render_template('edit_product.html' , product = product)
    
@app.route('/delete_product/<id>')
def delete_product(id):
    product_collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(debug=True)