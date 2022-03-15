import fire
from pathlib import Path
import pandas as pd

import pyeuropeana.utils as utils

def download_images(df,saving_dir,n_images = 10):
  for i,row in df.iterrows():
    if i > n_images:
      break
    try:
      img = utils.url2img(row['image_url'])
    except:
      img = None
    if not img:
      continue
    fname = row['europeana_id'].replace('/','[ph]')+'.jpg'
    img.save(saving_dir.joinpath(fname))


def main(**kwargs):
    saving_dir = kwargs.get('saving_dir')
    input = kwargs.get('input')

    df = pd.read_csv(input)
    download_images(df,Path(saving_dir),n_images = 1e6)

if __name__ == '__main__':
    fire.Fire(main)