from flask import Flask, render_template, request, redirect, url_for, flash
from firebase_admin import credentials, firestore, initialize_app

# initializations
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
db_ref = db.collection('database')

# settings
app.secret_key = "mysecretkey"

def get_data():
    all_data = db_ref.stream()
    data=[]
    for doc in all_data:
        data.append(doc.to_dict())
    return data

# routes
@app.route('/')
def Index():
    return render_template('index.html', contacts = get_data())


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        document_id=str(len(db_ref.get()))
        values = {key:value for key,value in request.form.items()}
        values['ID']=document_id
        db_ref.document(document_id).set(values)
        flash('Contact Added successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    return render_template('edit-contact.html', contact = db_ref.document(id).get().to_dict())


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        values = {key:value for key,value in request.form.items()}
        values['ID']=id
        db_ref.document(id).set(values)
        return redirect(url_for('Index'))


@app.route('/delete/<id>', methods = ['POST','GET'])
def delete_contact(id):
    db_ref.document(id).delete()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
