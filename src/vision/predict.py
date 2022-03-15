import fire
from pathlib import Path
import pandas as pd
from google.cloud import storage
from google.cloud import vision


def main(**kwargs):

    data_path = kwargs.get('data_path')
    saving_path = kwargs.get('saving_path')
    vocab = kwargs.get('vocab')

    vocab_df = pd.read_csv(vocab)

    test_set_df = pd.read_csv(data_path)

    bucket_name = 'vision-project-bucket'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    all_blobs = list(storage_client.list_blobs(bucket))

    df = pd.DataFrame()

    client = vision.ImageAnnotatorClient()
    image = vision.Image()

    for j,blob in enumerate(all_blobs):
        image_uri = f'gs://vision-project-bucket/{blob.name}'

        europeana_id = blob.name.replace('[ph]','/').replace('.jpg','')

        image_data = test_set_df[['europeana_id','uri','image_url','aggregator','provider']].loc[test_set_df['europeana_id'] == europeana_id]

        image.source.image_uri = image_uri
        response = client.label_detection(image=image)
        
        for i,label in enumerate(response.label_annotations):
            firebase_id = label.mid
            wiki_df = vocab_df['wikidata'].loc[vocab_df['LabelName'] == firebase_id]
            wikidata_uri = None
            if not wiki_df.empty:
                wikidata_uri = wiki_df.values[0]

            image_data[f'pred_name_{i}'] = label.description
            image_data[f'pred_wiki_{i}'] = wikidata_uri
            image_data[f'conf_{i}'] = label.score*100.


        df = df.append(image_data)

    df.to_csv(saving_path,index = False)


if __name__ == "__main__":
    fire.Fire(main)