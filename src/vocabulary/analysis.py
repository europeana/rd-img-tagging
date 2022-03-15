import fire
import pandas as pd

def main(**kwargs):
    vocab_path = kwargs.get('vocab_path')
    df = pd.read_csv(vocab_path)

    print(len(df['LabelName'].unique()))

    vocab_list = [col for col in df.columns if col not in ['LabelName','DisplayName']]
    
    result_list = []
    for vocab_name in vocab_list:
        n_matches = df.loc[~df[vocab_name].isnull()].shape[0]
        result_list.append(f'{vocab_name}: {n_matches}')
    
    res = '\n'.join(result_list)
    print(res)

if __name__ == "__main__":
    fire.Fire(main)