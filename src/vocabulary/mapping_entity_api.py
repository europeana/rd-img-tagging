import fire
import json
import requests
import pandas as pd
from tqdm import tqdm

class Entity:
  def __init__(self,key):
    self.key = key
  def __call__(self,**kwargs):
    uri = kwargs.get('uri')
    return requests.get(f'https://api.europeana.eu/entity/resolve?wskey={self.key}&uri={uri}').json()

def main(**kwargs):

    vocab_path = kwargs.get('vocab_path')
    saving_path = kwargs.get('saving_path')

    entity_api = Entity('api2demo')
    df = pd.read_csv(vocab_path)
    df = df.where(pd.notnull(df), None)

    entity_list = []
    for uri in tqdm(df['wikidata'].values[:]):
        if not uri:
            entity = None
        else:
            entity = None
            response = entity_api(uri = uri.replace('https','http'))
            if 'id' in response.keys():
                entity = response['id']

        entity_list.append(entity)
            
    df['entity_collection'] = entity_list
    df.to_csv(saving_path,index=False)
        
if __name__ == '__main__':
    fire.Fire(main)



