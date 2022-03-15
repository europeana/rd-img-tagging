import fire
from pathlib import Path
import pandas as pd

def main(**kwargs):

    saving_path = kwargs.get('saving_path')
    chunks_path = kwargs.get('chunks_path')

    df = pd.DataFrame()
    for fpath in Path(chunks_path).iterdir():
        _df = pd.read_csv(fpath)
        df = df.append(_df)
    df.to_csv(saving_path,index = False)

if __name__ == "__main__":
    fire.Fire(main)