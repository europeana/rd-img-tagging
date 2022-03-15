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

def request_properties(**kwargs):
  vocab_property = kwargs.get('vocab_property')
  entity = kwargs.get('entity')
  response = requests.get(f'https://www.wikidata.org/w/api.php?action=wbgetclaims&property={vocab_property}&entity={entity}&format=json').json()
  return response



def get_mapping(map_dict, wiki_id_list):
  vocab_property = map_dict['property']
  vocab_uri_list = []
  for wiki_id in wiki_id_list:
    try:
      response = request_properties(vocab_property = vocab_property, entity = wiki_id)
      vocab_id = None
      for k,v in response['claims'].items():
        vocab_id = v[0]['mainsnak']['datavalue']['value']
    except:
      vocab_id = None

    if vocab_id:
      vocab_uri = map_dict['uri'].replace('[placeholder]',vocab_id)
    else:
      vocab_uri = None
    vocab_uri_list.append(vocab_uri)
  return vocab_uri_list



def main(**kwargs):
    vocab_path = kwargs.get('vocab_path')
    saving_path = kwargs.get('saving_path')
    vocabulary_name = kwargs.get('vocabulary_name')
    saving_path = Path(saving_path)
    saving_path.mkdir(exist_ok = True, parents=True)

    fname = Path(vocab_path).name

    vocabulary_dict = {
        'aat':{'property':'P1014','uri':'http://vocab.getty.edu/page/aat/[placeholder]'},
        'iconclass':{'property':'P1256','uri':'http://www.iconclass.org/rkd/[placeholder]/'},
        # 'ulan':{'property':'P245','uri':'http://vocab.getty.edu/page/ulan/[placeholder]'},
        # 'tgn':{'property':'P1667','uri':'http://vocab.getty.edu/page/tgn/[placeholder]'},
        # 'mimo':{'property':'P3763','uri':'http://minim.ac.uk/index.php/explore/?instrument=[placeholder]/'},
        # 'viaf':{'property':'P214','uri':'https://viaf.org/viaf/[placeholder]/'},
        # 'geonames':{'property':'P1566','uri':'https://www.geonames.org/[placeholder]/'},
        # 'lcsh':{'property':'P244','uri':'http://id.loc.gov/authorities/subjects/[placeholder]'},
        # 'unesco':{'property':'P3916','uri':'http://vocabularies.unesco.org/thesaurus/[placeholder]'}, 
    }

    vocabulary_df = pd.read_csv(vocab_path)


    # print('getting wikidata uris...')
    # start = time()

    # wiki_uri_list = []
    # wiki_id_list = []
    # for firebase_id in vocabulary_df['LabelName'].values:

    #   wiki_uri,wiki_id = firebase_to_wikidata(firebase_id)
    #   wiki_uri_list.append(wiki_uri)
    #   wiki_id_list.append(wiki_id)

    # vocabulary_df['wikidata'] = wiki_uri_list

    # t = (time()-start)/60.0
    # print(f'it took {t} minutes')


    #wiki_uri_list = [parse_wikidata_uri(GKG.get(GK_id)) for GK_id in vocabulary_df['LabelName'].values]
    #wiki_id_list = [uri.split('/')[-1] if uri else uri for uri in wiki_uri_list]




    # #for vocabulary_name in vocabulary_dict.keys():

    vocabulary_df = vocabulary_df.where(pd.notnull(vocabulary_df), None)

    wiki_uri_list = vocabulary_df['wikidata'].values
    #print(wiki_uri_list)
    wiki_id_list = [uri.split('/')[-1] if uri else None for uri in wiki_uri_list]

    print(f'getting {vocabulary_name} uris...')
    start = time()
    uri_list = get_mapping(vocabulary_dict[vocabulary_name], wiki_id_list)
    t = (time()-start)/60.0
    print(f'it took {t} minutes')

    vocabulary_df[vocabulary_name] = uri_list

    vocabulary_df.to_csv(saving_path.joinpath(fname),index=False)


if __name__ == "__main__":
    fire.Fire(main)