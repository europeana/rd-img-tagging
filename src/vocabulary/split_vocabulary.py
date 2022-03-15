import fire
from pathlib import Path
import pandas as pd
import numpy as np

def main(**kwargs):
    vocab_path = kwargs.get('vocab_path')
    saving_path = kwargs.get('saving_path')
    n_chunks = kwargs.get('n_chunks')

    saving_path = Path(saving_path)
    saving_path.mkdir(exist_ok = True,parents = True)

    vocabulary_df = pd.read_csv(vocab_path)
    df_list = np.array_split(vocabulary_df, n_chunks)

    for i,df in enumerate(df_list):
        df.to_csv(saving_path.joinpath(f'vocabulary_{i}.csv'),index = False)

if __name__ == "__main__":
    fire.Fire(main)