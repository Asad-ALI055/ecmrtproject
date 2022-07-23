import pandas as pd

def seokeyword(name,path):
    df = pd.read_csv(path+'all_seo_keywords.csv')
    # df = pd.read_csv('all_seo_keywords.csv')

    df = df.dropna()

    seo_dict={}

    n1=[]
    for i in df['Keyword']:
        if name in str(i).lower():
            n1.append(str(i))

    print(df.loc[df['Keyword'].isin(n1)])
    d1=df.loc[df['Keyword'].isin(n1)]

    seo_dict['keyword']=n1
    seo_dict['avg_search']=list(d1['Avg monthly searches'])
    seo_dict['competition']=list(d1['Competition'])
    seo_dict['competition_index']=list(d1['Competition index'])

    print(len(n1))
    print(seo_dict['avg_search'])

    return seo_dict


# seokeyword('tv')
