import fire
from time import time
import requests
import pandas as pd
from pathlib import Path

class GoogleKG():
  def __init__(self,key):
    self.key = key
  def get(self,id):
    return requests.get('https://kgsearch.googleapis.com/v1/entities:search', params = {'ids':id,'key':self.key}).json()  

def request_Wikipedia(**kwargs):
  concept_name = kwargs.get('concept_name')
  return requests.get(f'https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&titles={concept_name}&format=json').json()

def parse_wikidata_uri(GK_response):
  try:
    concept_name = GK_response['itemListElement'][0]['result']['name']
    Wikipedia_response = request_Wikipedia(concept_name = concept_name)
    for k,v in Wikipedia_response['query']['pages'].items():
      wikibase_id = v['pageprops']['wikibase_item']
      wikidata_uri = f'https://www.wikidata.org/entity/{wikibase_id}'
  except:
    wikidata_uri = None
  return wikidata_uri

def firebase_to_wikidata(firebase_id):

  query = '''
  SELECT ?item 
  WHERE 
  {
    ?item wdt:P646 "[placeholder]". 
  }
  '''
  query = query.replace('[placeholder]',firebase_id)
  wikidata_uri = None
  wikidata_id = None
  try:
    data = requests.get('https://query.wikidata.org/sparql', params = {'format': 'json', 'query': query}).json()
    wikidata_uri = data['results']['bindings'][0]['item']['value']
    wikidata_id = wikidata_uri.split('/')[-1]
  except:
    wikidata_uri = None
    wikidata_id = None
  return wikidata_uri,wikidata_id

def main(**kwargs):
    vocab_path = kwargs.get('vocab_path')
    saving_path = kwargs.get('saving_path')
    saving_path = Path(saving_path)
    saving_path.mkdir(exist_ok = True, parents=True)

    vocab_fname = Path(vocab_path).name

    vocabulary_df = pd.read_csv(vocab_path)

    GKG = GoogleKG('AIzaSyBhX8-XYxRkJCav4V9_1cRLaTDN30Owcfo')

    print('getting wikidata uris GKG...')
    start = time()
    wiki_uri_list = [parse_wikidata_uri(GKG.get(GK_id)) for GK_id in vocabulary_df['LabelName'].values]

    # vocabulary_df['wikidata_GKG'] = wiki_uri_list

    # print('getting wikidata uris...')
    # start = time()

    # wiki_uri_list = []
    # wiki_id_list = []
    # for firebase_id in vocabulary_df['LabelName'].values:
    #     wiki_uri,wiki_id = firebase_to_wikidata(firebase_id)
    #     wiki_uri_list.append(wiki_uri)
    #     wiki_id_list.append(wiki_id)

    vocabulary_df['wikidata'] = wiki_uri_list

    t = (time()-start)/60.0
    print(f'it took {t} minutes')

    vocabulary_df.to_csv(saving_path.joinpath(vocab_fname),index=False)


     

if __name__ == "__main__":
    fire.Fire(main)