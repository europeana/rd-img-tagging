import fire
from pathlib import Path
from google.cloud import storage


def main(**kwargs):

    images_dir = kwargs.get('images_dir')

    def upload_blob(bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

    bucket_name = 'vision-project-bucket'

    for source_file_name in Path(images_dir).iterdir():
        destination_blob_name = Path(source_file_name).name
        #print(source_file_name, destination_blob_name)
        upload_blob(bucket_name, source_file_name, destination_blob_name)
 

if __name__ == '__main__':
    fire.Fire(main)