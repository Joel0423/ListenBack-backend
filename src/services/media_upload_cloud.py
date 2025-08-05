from firebase_admin import storage

def upload_media_to_firebase(file_path, dest_blob_name):
    bucket = storage.bucket()
    blob = bucket.blob(dest_blob_name)
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url