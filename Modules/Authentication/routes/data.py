from flask import Blueprint , request , render_template, session ,redirect
import pandas as pd
from models import dataset_collection 
data_bp = Blueprint('data',__name__)

@data_bp.route('/data-ingestion', methods= ['GET','POST'])
def data_ingestion():
    # if session.get('role') == 'admin':
    #     return redirect('/')

    message = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                df = pd.read_csv(file)
                df.fillna("N/A", inplace = True)
                data = df.to_dict(orient= 'records')
                if data:
                    dataset_collection.insert_many(data)
                message = "Data uploads & saved succesfully"
            except Exception as e :
                message = f"Errors{str(e)}"
    return render_template('data_ingestion.html',message = message)


#----------------view data --------------------
@data_bp.route('/view-data', methods=['GET', 'POST'])
def view_data():
    # if session.get('role') == 'admin':
    #     return redirect('/')

    query = {}
    search = request.form.get('search')
    if search:
        query["name"] = {"$regex": search, "$options": "i"}

    data = list(dataset_collection.find(query))
    return render_template('view_data.html', data=data)

#----------------Data Clear krne k liye --------------------
@data_bp.route('/clear-data')
def clear_data():
    # if session.get('role') == 'admin':
    #     return redirect('/')

    dataset_collection.delete_many({})
    return redirect('/view-data')