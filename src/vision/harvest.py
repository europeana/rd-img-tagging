import fire
import pandas as pd
from pathlib import Path

import pyeuropeana.apis as apis
import pyeuropeana.utils as utils

def get_facet_fields(response):
  return response['facets'][0]['fields']

def count_providers_aggregator(aggregator,limit = 100):
  response = apis.search(
      query = f'(PROVIDER:"{aggregator}") AND NOT dc_subject:* AND NOT dc_format:* AND NOT dcterms_medium:*',
      profile = 'facets',
      facet = f'DATA_PROVIDER&f.DATA_PROVIDER.facet.limit={limit}',
      rows = 1
  )
  print(response.keys())
  facets = get_facet_fields(response)
  return pd.DataFrame(facets).rename(columns={"label": "provider"})

def count_provider_aggregator_list(aggregators_list,providers_per_aggregator = 20, counter_fn = count_providers_aggregator):
  df = pd.DataFrame()
  for aggregator in aggregators_list:
    provider_df = counter_fn(aggregator,limit = providers_per_aggregator)
    provider_df = provider_df.sort_values(by='count',ascending = False)
    provider_df['aggregator'] = aggregator
    df = df.append(provider_df)
  df = df.reset_index()
  del df['index']
  cols = df.columns.tolist()
  cols = [cols[0],cols[-1],cols[1]]
  df = df[cols]
  return df


def main(**kwargs):

    providers_per_aggregator = kwargs.get('providers_per_aggregator',50)
    objects_per_provider = kwargs.get('objects_per_provider',50)
    saving_path = kwargs.get('saving_path')

    saving_path = Path(saving_path)

    aggregators_list = [
    'OpenUp!',
    'Digitale Collectie',
    'Hispana',
    'Kulturpool',
    'Greek Aggregator SearchCulture.gr | National Documentation Centre (EKT)',
    'Formula Aggregation Service of the National Library of Finland',
    'European Fashion Heritage Association',
    'German Digital Library',
    'Swedish Open Cultural Heritage | K-samsök',
    'Slovenian National E-content Aggregator',
    'MIMO - Musical Instrument Museums Online',
    'PHOTOCONSORTIUM',
    'LT-Aggregator Service National Library of Lithuania',
    'Museu',
    'Judaica Europeana/Jewish Heritage Network',
    'Europeana FashionEuropeana Fashion',
    'Archives Portal Europe',
    'Heritage plus.be',
    'National Library of France',
    'Czech digital library/Česká digitální knihovna',
    'INP - National Heritage Institute, Bucharest',
    'Forum Hungaricum Non-profit Ltd.',
    'CulturaItalia',
    'Digital Libraries Federation',
    'CARARE',
    'EFG - The European Film Gateway',
    'EuropeanaLocal Austria',
    'RNOD-Portugal',
    'EuropeanaPhotography',
    ]

    df = count_provider_aggregator_list(aggregators_list,providers_per_aggregator = providers_per_aggregator,counter_fn = count_providers_aggregator)
    #df.to_csv(saving_path,index=False)

    print(df.shape)

    #count_df = pd.DataFrame()
    eval_df = pd.DataFrame()
    for i,row in df.iterrows():
      aggregator = row['aggregator']
      provider = row['provider']

      response = apis.search(
          query = f'DATA_PROVIDER:"{provider}" AND NOT dc_subject:* AND NOT dc_format:* AND NOT dcterms_medium:*',
          qf = 'MIME_TYPE:image/jpeg',
          rows = objects_per_provider
      )

      # count_df = count_df.append(pd.DataFrame([{
      #   'provider':provider,
      #   'aggregator':aggregator,
      #   'counts':response['totalResults'],
      #   'url': response['url']
      # }]))
      
      if 'items' in response.keys() and response['items']:
        CHO_df = utils.search2df(response)
        CHO_list = response['items']
        CHO_df['aggregator'] = aggregator
        CHO_df['provider'] = provider
        eval_df = eval_df.append(CHO_df)
        # if CHO_list:
        #   CHO = utils.process_CHO_search(CHO_list[0])
        #   del CHO['raw_metadata']
        #   CHO_df = pd.DataFrame([CHO])

          


    eval_df.to_csv(saving_path,index=False)

    print(eval_df.shape)

if __name__ == '__main__':
    fire.Fire(main)



