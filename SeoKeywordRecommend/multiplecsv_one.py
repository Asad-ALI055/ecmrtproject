import pandas as pd

# df=pd.read_csv('keyword_data/Keyword Stats 2021-06-16 at 00_37_37.csv',)
df=pd.read_excel('keyword_data/all_seokeywords.xlsx')
# print(str(df['Keyword']).strip())

print(df)
df.to_csv('all_seo_keywords.csv')
