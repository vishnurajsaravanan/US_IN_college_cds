import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
        'storageBucket': 'us-datasets-3f68b.appspot.com'
})


def store_in_firestore(college_name, data):
    db = firestore.client()
    college_name = college_name.replace(' ','_')
    doc_ref = db.collection('colleges').document(college_name)
    doc_ref.set({'college name': college_name, 'data': data})
    print(f'Data for {college_name} stored in Firestore')


# Upload file to Firebase Storage
def upload_file(file_path):
    # firebase storage
    bucket = storage.bucket()
    blob = bucket.blob(f'/US College CDS/{file_path}')
    # Open the file in read mode
    with open(f'{file_path}', 'rb') as my_file:
        blob.upload_from_file(my_file)
    print(f'File uploaded {file_path} to Firebase Storage')

