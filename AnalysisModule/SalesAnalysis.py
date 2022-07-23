import os
import pandas as pd
import matplotlib.pyplot as plt

# #### Read in updated dataframe       1
# In[4]:   (use)length of all rows
def preprocess(path):
    dic1={}
    all_data = pd.read_csv(path)
    print("Total Number Of Transactions: ",len(all_data['Product']))
    dic1['total_trans']=len(all_data['Product'])


    # In[5]:   (not use)
    # info1=all_data.info()
    # print(info1)


    # ##### Drop rows of NAN              2
    # In[6]:  (use) length of null rows

    # Find NAN
    nan_df = all_data[all_data.isna().any(axis=1)]
    # nul=nan_df.to_string()
    # print(nan_df.head())
    print("Empty/Faulty Transactions: ",len(nan_df))
    #
    all_data = all_data.dropna(how='all')
    print(all_data.head())




    # # ##### Get rid of text in order date column
    #
    # # In[7]:  (use)
    #
    #
    al = all_data[all_data['Order Date'].str[0:2]=='Or'].count()
    print(len(al))
    print("Empty/Faulty Transactions: ",len(nan_df)+len(al))
    dic1['empty_trans']=len(nan_df)+len(al)

    all_data=all_data[all_data['Order Date'].str[0:2]!='Or']
    print("Number of Transactions after cleaning:",len(all_data))
    dic1['actual_trans']=len(all_data)

    #
    #
    # # #### Make columns correct type
    #
    # # In[8]:
    #
    #
    all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
    all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
    #
    #
    # # ### Augment data with additional columns
    #
    # # #### Add month column

    all_data['Month'] = pd.to_datetime(all_data['Order Date']).dt.month
    print(all_data)
    #
    #
    # # #### Add city column
    #
    # # In[11]:
    #
    #
    def get_city(address):
        return address.split(",")[1].strip(" ")
    #
    def get_state(address):
        return address.split(",")[2].split(" ")[1]
    #
    all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)}  ({get_state(x)})")
    all_data.head()
    return all_data,dic1    #dict 3 value about transactions

def myanalysis(path):
    all_data,dict1=preprocess(path)

    #
    # # ## Data Exploration!
    # # #### Question 1: What was the best month for sales? How much was earned that month?
    # # In[26]:

    all_data['Sales'] = all_data['Quantity Ordered'].astype('int') * all_data['Price Each'].astype('float')

    # # In[27]:

    # all_data.groupby(['Month']).sum()

    # # In[28]:

    months = range(1,13)
    print("Best Month for sales")
    print(list(months))
    print(list(all_data.groupby(['Month']).sum()['Sales']))
    dict1['month1']=list(months)
    dict1['sales1']=list(all_data.groupby(['Month']).sum()['Sales'])

    # plt.bar(months,all_data.groupby(['Month']).sum()['Sales'])
    # plt.xticks(months)
    # plt.ylabel('Sales in USD ($)')
    # plt.xlabel('Month number')
    # plt.show()


    # # #### Question 2: What city sold the most product?
    # # In[29]:

    all_data.groupby(['City']).sum()

    # # In[30]:

    keys = [city for city, df in all_data.groupby(['City'])]
    print("Best City sales wise")
    print(keys)
    print(list(all_data.groupby(['City']).sum()['Sales']))
    dict1['city2']=list(keys)
    dict1['sales2']=list(all_data.groupby(['City']).sum()['Sales'])

    # plt.bar(keys,all_data.groupby(['City']).sum()['Sales'])
    # plt.ylabel('Sales in USD ($)')
    # plt.xlabel('Month number')
    # plt.xticks(keys, rotation='vertical', size=8)
    # plt.show()


    # #### Question 3: What time should we display advertisements to maximize likelihood of customer's buying product?
    # In[31]:

    # # Add hour column
    all_data['Hour'] = pd.to_datetime(all_data['Order Date']).dt.hour
    all_data['Minute'] = pd.to_datetime(all_data['Order Date']).dt.minute
    all_data['Count'] = 1
    print(all_data.head())

    # # In[32]:

    keys = [pair for pair, df in all_data.groupby(['Hour'])]
    print("Best Hour for sales/peak sales hour or best hour for advertisement ")
    print(keys)
    print(list(all_data.groupby(['Hour']).count()['Count']))
    dict1['hour3']=list(keys)
    dict1['trans3']=list(all_data.groupby(['Hour']).count()['Count'])


#  Day Wise Sales
    all_data['Weekday']=pd.to_datetime(all_data['Order Date']).dt.weekday
    days=[pair for pair, df in all_data.groupby(['Weekday'])]
    print(days)
    print(list(all_data.groupby(['Weekday']).count()['Count']))
    print(list(all_data.groupby(['Weekday']).sum()['Sales']))
    # plt.plot(keys, all_data.groupby(['Hour']).count()['Count'])
    # plt.xticks(keys)
    # plt.grid()
    # plt.show()

    # # My recommendation is slightly before 11am or 7pm


    # # #### Question 4: What products are most often sold together?
    # # In[48]:

    # # https://stackoverflow.com/questions/43348194/pandas-select-rows-if-id-appear-several-time
    df = all_data[all_data['Order ID'].duplicated(keep=False)]

    # # Referenced: https://stackoverflow.com/questions/27298178/concatenate-strings-from-several-rows-using-pandas-groupby
    df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
    df2 = df[['Order ID', 'Grouped']].drop_duplicates()

    # # In[47]:

    # # Referenced: https://stackoverflow.com/questions/52195887/counting-unique-pairs-of-numbers-into-a-python-dictionary
    from itertools import combinations
    from collections import Counter

    count = Counter()
    #
    for row in df2['Grouped']:
        row_list = row.split(',')
        count.update(Counter(combinations(row_list, 2)))

    for key,value in count.most_common(10):
        print(key, value)


    # #### What product sold the most? Why do you think it sold the most?

    # In[76]:


    product_group = all_data.groupby('Product')
    quantity_ordered = product_group.sum()['Quantity Ordered']

    keys = [pair for pair, df in product_group]
    print(keys)
    print(list(quantity_ordered))
    dict1['product4']=list(keys)
    dict1['quantity4']=list(quantity_ordered)

    # plt.bar(keys, quantity_ordered)
    # plt.xticks(keys, rotation='vertical', size=8)
    # plt.show()

    # # In[75]:

    # # Referenced: https://stackoverflow.com/questions/14762181/adding-a-y-axis-label-to-secondary-y-axis-in-matplotlib
    prices = all_data.groupby('Product').mean()['Price Each']
    #
    # fig, ax1 = plt.subplots()
    #
    print("sold product and their prices")
    print(list(keys))
    print(list(quantity_ordered))
    print(list(prices))
    dict1['price5']=list(prices)
    #
    # # ax2 = ax1.twinx()
    # # ax1.bar(keys, quantity_ordered, color='g')
    # # ax2.plot(keys, prices, color='b')
    # #
    # # ax1.set_xlabel('Product Name')
    # # ax1.set_ylabel('Quantity Ordered', color='g')
    # # ax2.set_ylabel('Price ($)', color='b')
    # # ax1.set_xticklabels(keys, rotation='vertical', size=8)
    #
    # # fig.show()

    return dict1