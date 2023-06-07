from google.cloud import storage
from datetime import datetime, timedelta
import os


def upload_file(file_path, user_id):
    # Get bucket
    client = storage.Client()
    bucket = client.bucket("daily-cloud-user-predicted-images")

    # Get date (for filename)
    date = datetime.now().strftime("%Y-%m-%d")

    # Destination path
    destination_path = f"{user_id}/{date}.jpg"

    # Upload file
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(file_path)
    print(f"File {file_path} uploaded to bucket daily-cloud-user-predicted-images.")

    # Get authenticated URL which expires in 7 days
    expiration = datetime.now() + timedelta(days=7)
    authenticated_url = blob.generate_signed_url(expiration=expiration)

    return authenticated_url


url = upload_file(os.path.abspath("cat_predict.jpg"), "uQqLNwNlaNXqey7e165HCRjzSvF3")
print(url)
