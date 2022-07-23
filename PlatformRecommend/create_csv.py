import pandas as pd
import os


def multiple_one_csv(path):
    print(os.listdir(path))
    filenames=os.listdir(path)
    df = pd.concat(map(pd.read_csv, [path+'/'+i for i in filenames]))

    df=df.dropna()

    df.to_csv('groups_alldata.csv',index=False)

multiple_one_csv('input_dataset')