import pandas as pd

def Platform_Recommendation(name,path):
    df = pd.read_csv(path + 'groups_alldata.csv')
    # df = pd.read_csv('groups_alldata.csv')

    df = df.dropna()
    group_dict={}

    n1=[]
    for i in df['page_title']:
        if name in str(i).lower():
            n1.append(str(i))

    # print(df.loc[df['page_title'].isin(n1)])
    d1=df.loc[df['page_title'].isin(n1)]

    # print(d1)
    group_dict['page_title']=n1
    group_dict['img_link']=list(d1['img_link'])
    group_dict['page_url']=list(d1['page_url'])
    group_dict['aduiance']=list(d1['aduiance'])

    group_dict['type'] = [str(i).split('\xa0')[0] for i in group_dict['aduiance']]
    group_dict['aduiance']=[str(i).split('\xa0')[2][3:] for i in group_dict['aduiance']]
    # print(n1)
    # print(len(group_dict['aduiance']))
    # print(len(group_dict['type']))

    return group_dict

# Platform_Recommendation('toaster',' ')