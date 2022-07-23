# DFSA (DarazFlashSaleAnalysis)

# %%%%%%%%%  Import Libraries  %%%%%%%%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import statistics
import os
import numpy as np


from datetime import timedelta     # module use to add days in date


# &&&&&&&&&&   Functions for Preprocessing    &&&&&&&&&&&&

# %%%%%%%%%   Function for Cleaning    %%%%%%%%%%
def clean(df):
    dup_values=df.duplicated().sum()   # how many duplicate values
    df=df.drop_duplicates()            # drop duplicate values

    null_values=df.isna().sum()        # how many null values
    df=df.dropna()                     # drop null values

    return df

# %%%%%%%%%   Function for Transformation    %%%%%%%%%%
def transformation(df):
    # it only store date
    df['Date'] = pd.to_datetime(df['Date'])
    # df['Date']=df['Date'].dt.date

    # generate sales & Product Name(first 4 word of title) column
    df['Sales'] = df['Price'] * df['Sold Products']

    def name_fuc(x):
        x = str(x)
        x = ' '.join(x.split()[:4])
        return x
    df['Name'] = df['Product Title'].map(name_fuc)

    return df

# %%%%%%%%%   Function For Percentile(To find Distribution of product w.r.t revenue)   %%%%%%%%%
def percentiles(df,daraz_dict):
    # print("Percentail 50 of not zero sale products :",np.percentile(df['Sales'][df['Sold Products']!=0],50))
    # print("Percentail 70 of not zero sale products :",np.percentile(df['Sales'][df['Sold Products']!=0],70))
    # print("Percentail 95 of not zero sale products :",np.percentile(df['Sales'][df['Sold Products']!=0],95))
    # print("Percentail 50 all :",np.percentile(df['Sales'],50))
    # print("Percentail 70 all :",np.percentile(df['Sales'],70))
    # print("Percentail 95 all :",np.percentile(df['Sales'],95))

    # percentile50 = np.percentile(df['Sales'][df['Sold Products'] != 0], 50)
    # percentile70=np.percentile(df['Sales'][df['Sold Products']!=0],70)
    percentile95 = np.percentile(df['Sales'], 95)

    # find 95 percentaile how much percent of total revenue
    values_95 = df['Sales'][df['Sales'] <= percentile95].sum()
    values_5 = df['Sales'][df['Sales'] > percentile95].sum()
    values_total = df['Sales'].sum()

    # print(round((values_95 / values_total) * 100, 0), "%")
    # print(round((values_5 / values_total) * 100, 0), "%")

    # 95 percent of all products only gets 22% of Daraz Flash sale Revenue
    # 83 (5%) product have market sahre 78%
    # 5 percent of all products gets 78% of Daraz Flash sale Revenue
    # print('Market share product in term of sales', len(df[df['Sales'] <= percentile95]))
    # print('Market share product in term of sales', len(df[df['Sales'] > percentile95]))

    # Product percentage from all products
    daraz_dict['percentail_percent1']=round((len(df[df['Sales'] <= percentile95])/len(df))*100)
    daraz_dict['percentail_percent2']=round((len(df[df['Sales'] > percentile95])/len(df))*100)

    # Revenue share in percent from all Revenue
    daraz_dict['percentail_revenue_share1']=round((values_95 / values_total) * 100)
    daraz_dict['percentail_revenue_share2'] =round((values_5 / values_total) * 100)

    # Product percentage to Amount of products
    daraz_dict['percentail_amount1']=len(df[df['Sales'] <= percentile95])
    daraz_dict['percentail_amount2']=len(df[df['Sales'] > percentile95])

    # pie chart values
    a=round((len(df[df['Sales'] <= percentile95])/len(df))*100)
    a=str(a)+'% ('+str(len(df[df['Sales'] <= percentile95]))+') Products Share'
    a1=round((len(df[df['Sales'] > percentile95])/len(df))*100)
    a1=str(a1)+'% ('+str(len(df[df['Sales'] > percentile95]))+') Products Share'
    daraz_dict['mrk_lable']=[a,a1]
    daraz_dict['mrk_y']=[round((values_95 / values_total) * 100),round((values_5 / values_total) * 100)]

    # all product details that have revenue share higher
    mrk_share=df[df['Sales'] > percentile95]

    def conver(x):
        x=str(x).split()[0]
        return x

    daraz_dict['mrk_name'] = list(mrk_share['Name'])
    daraz_dict['mrk_date'] = list(mrk_share['Date'].apply(conver))
    daraz_dict['mrk_amount'] = list(mrk_share['Sold Products'])
    daraz_dict['mrk_sales'] = list(mrk_share['Sales'])
    return daraz_dict

# %%%%%%%%%   Function to Find Repeated Products   %%%%%%%%
def repeated(df,daraz_dict):
    name_ls,repeat_ls,sale_ls,sold_ls=[],[],[],[]
    df=df[df['Sales']>42500]
    for i in df.groupby(df['Name']):
        if len(i[1]) > 1:
            # print(len(i[1]))
            repeat_ls.append(len(i[1]))
            name_ls.append(i[1]['Name'].drop_duplicates().iloc[0])
            sale_ls.append(i[1]['Sales'].sum())
            sold_ls.append(i[1]['Sold Products'].sum())
            # print(i[1]['Name'].drop_duplicates())
            # print(i[1]['Price'])
            # print(i[1]['Sold Products'].sum())
            # print(i[1]['Sales'].sum())

    daraz_dict['mrk5_name']=name_ls
    daraz_dict['mrk5_repeat']=repeat_ls
    daraz_dict['mrk5_sold']=sold_ls
    daraz_dict['mrk5_sales']=sale_ls

    return daraz_dict

# %%%%%%%%%     Function for find most repeated products
def most_repeated(df,daraz_dict):
    df['Count'] = 1
    rep_prod,n1,r1,a1,s1 = [],[],[],[],[]
    # for not repeat products
    n_n1, n_r1, n_a1, n_s1 = [], [], [], []
    rep_df=pd.DataFrame()
    nrep_df=pd.DataFrame()
    for i in df.groupby(df['Name']):
        if len(i[1])>1:
            # print(len(i[1]))
            # print(i[1]['Name'].drop_duplicates().iloc[0])
            # print(i[1]['Sales'].sum())
            # print(i[1]['Sold Products'].sum())
            # print()
            n1.append(i[1]['Name'].drop_duplicates().iloc[0])
            r1.append(len(i[1]))
            a1.append(i[1]['Sold Products'].sum())
            s1.append(i[1]['Sales'].sum())

            rep_prod.append(len(i[1]))
        else:
            n_n1.append(i[1]['Name'].drop_duplicates().iloc[0])
            n_r1.append(len(i[1]))
            n_a1.append(i[1]['Sold Products'].sum())
            n_s1.append(i[1]['Sales'].sum())

    rep_df['Name']=n1
    rep_df['Repeat']=r1
    rep_df['Sold Products']=a1
    rep_df['Sales']=s1

# for not repeated products
    nrep_df['Name']=n_n1
    nrep_df['Repeat']=n_r1
    nrep_df['Sold Products']=n_a1
    nrep_df['Sales']=n_s1


    # sales trend reeated vs not repeated products
    # sales repeat
    daraz_dict['rep_sale_trend']=list(rep_df['Sales'])
    daraz_dict['rep_sale_trend_len']=[i for i in range(1,len(s1))]
    daraz_dict['rep_net_sale']=rep_df['Sales'].sum()
    daraz_dict['rep_max_sale'] = rep_df['Sales'].max()
    daraz_dict['rep_avg_sale'] = round(rep_df['Sales'].mean())

    # sold repeat
    daraz_dict['rep_sold_trend']=list(rep_df['Sold Products'])
    daraz_dict['rep_sold_trend_len'] = [i for i in range(1, len(a1))]
    daraz_dict['rep_net_sold'] = rep_df['Sold Products'].sum()
    daraz_dict['rep_max_sold'] = rep_df['Sold Products'].max()
    daraz_dict['rep_avg_sold'] = round(rep_df['Sold Products'].mean())

    # sales not repeat
    daraz_dict['not_rep_sale_trend']=list(nrep_df['Sales'])
    daraz_dict['not_rep_sale_trend_len']=[i for i in range(1,len(n_s1))]
    daraz_dict['not_rep_net_sale']=nrep_df['Sales'].sum()
    daraz_dict['not_rep_max_sale'] = nrep_df['Sales'].max()
    daraz_dict['not_rep_avg_sale'] = round(nrep_df['Sales'].mean())

    # sold not repeat
    daraz_dict['not_rep_sold_trend']=list(nrep_df['Sold Products'])
    daraz_dict['not_rep_sold_trend_len'] = [i for i in range(1, len(n_a1))]
    daraz_dict['not_rep_net_sold'] = nrep_df['Sold Products'].sum()
    daraz_dict['not_rep_max_sold'] = nrep_df['Sold Products'].max()
    daraz_dict['not_rep_avg_sold'] = round(nrep_df['Sold Products'].mean())

    # chart for repeat products on base of repeat,sold & sales
    rep_df=rep_df.sort_values(by=['Repeat'],ascending=False)
    daraz_dict['top15_repeat_name']=list(rep_df['Name'].head(15))
    daraz_dict['top15_repeat_rep']=list(rep_df['Repeat'].head(15))

    rep_df = rep_df.sort_values(by=['Sold Products'], ascending=False)
    daraz_dict['top15_repeat_name1'] = list(rep_df['Name'].head(15))
    daraz_dict['top15_repeat_rep1']=list(rep_df['Repeat'].head(15))
    daraz_dict['top15_repeat_sold1']=list(rep_df['Sold Products'].head(15))
    daraz_dict['top15_repeat_sales1']=list(rep_df['Sales'].head(15))


    rep_df = rep_df.sort_values(by=['Sales'], ascending=False)
    daraz_dict['top15_repeat_name2'] = list(rep_df['Name'].head(15))
    daraz_dict['top15_repeat_rep2'] = list(rep_df['Repeat'].head(15))
    daraz_dict['top15_repeat_sales2']=list(rep_df['Sales'].head(15))
    daraz_dict['top15_repeat_sold2'] = list(rep_df['Sold Products'].head(15))

    print(daraz_dict['top15_repeat_name'])


    return daraz_dict

# %%%%%%%%%    Function for sales trend reeated vs not repeated products
def repeat_vs_notrepeat(df,daraz_dict):
    pass


def daraz_analysis_function(path):
    df = pd.read_csv(path+'Daraz_alldata.csv')
    daraz_dict={}
    # Data Preprocessing
    df=clean(df)             # data cleaning
    df2=transformation(df)    # data Transformation


    #### print('')
    # Total Item Items Sold on store
    # print('Total Products Sold Till Now :',df['Sold Products'].sum())
    daraz_dict['total_item_sold']=df['Sold Products'].sum()

    # Total Revenue Earn
    # print('Rs.',df['Sales'].sum())
    daraz_dict['total_revenue']=df['Sales'].sum()

    # Average Sales Amount
    ds=df.copy()
    ds['Date'] = df['Date'].dt.date
    ds=ds.groupby(ds['Date'])          # sales amount on specific Date
    month_sales=[i[1]['Sales'].sum() for i in ds]
    # print('Average Sales Rs.',statistics.mean(month_sales))
    daraz_dict['avg_sale']=statistics.mean(month_sales)

    #### print('')
    # 1 Most Sales Date with amount
    date1=[(i[1]['Sales'].sum(),i[0]) for i in ds]
    max_sale_data=max(date1)
    # print('Top Sales Day :',max_sale_data[1])
    # print('Revenue :',max_sale_data[0])
    daraz_dict['most_sales_day1']=max_sale_data[1]
    daraz_dict['most_sales_revenue1']=max_sale_data[0]

    # Sales Vs Date line chart
    daraz_dict['s_date'] = [str(i[1]) for i in date1]
    daraz_dict['s_sale'] = [i[0] for i in date1]


    #### print('')
    # 1 Least Sales Date with amount
    min_sale_data=min(date1)
    # print('Least Sales Day :',min_sale_data[1])
    # print('Revenue :',min_sale_data[0])
    daraz_dict['least_sales_day2']=min_sale_data[1]
    daraz_dict['least_sales_revenue2']=min_sale_data[0]

    daraz_dict['graph_ml_sale_date']=[str(max_sale_data[1]),str(min_sale_data[1])]
    daraz_dict['graph_ml_sale_revenue'] = [max_sale_data[0], min_sale_data[0]]

    #### print('')
    # most sold item
    most_sold_item=df[df['Sold Products']==df['Sold Products'].max()]
    # print('Date :',str(most_sold_item['Date']).split()[1])
    # print('Sold Product Amount :',int(most_sold_item['Sold Products']))
    # print('Sale Amount :',int(most_sold_item['Sales']))
    # print('Product name :',most_sold_item['Name'].iloc[0])
    ## print(most_sold_item['Date']+timedelta(days=2))   # method to add days in date
    daraz_dict['most_sold_item_name3']=most_sold_item['Name'].iloc[0]
    daraz_dict['most_sold_item_date3']=str(most_sold_item['Date']).split()[1]
    daraz_dict['most_sold_item_amount3']=int(most_sold_item['Sold Products'])
    daraz_dict['most_sold_item_revenue3']=int(most_sold_item['Sales'])


    #### print('')
    # 2 Least sold item
    least_sold_item=df[df['Sold Products']==df['Sold Products'].min()]
    # print('Date :',str(least_sold_item['Date']).split()[1])
    # print('Sold Product Amount :',least_sold_item['Sold Products'].iloc[0])
    # print('Sale Amount :',least_sold_item['Sales'].iloc[0])
    # print('Product name :',least_sold_item['Name'].iloc[0])
    daraz_dict['least_sold_item_name4']=least_sold_item['Name'].iloc[0]
    daraz_dict['least_sold_item_date4']=str(least_sold_item['Date']).split()[1]
    daraz_dict['least_sold_item_amount4']=int(least_sold_item['Sold Products'].iloc[0])
    daraz_dict['least_sold_item_revenue4']=int(least_sold_item['Sales'].iloc[0])

    daraz_dict['graph_ml_sold_name'] = [most_sold_item['Name'].iloc[0],least_sold_item['Name'].iloc[0]]
    daraz_dict['graph_ml_sold_amount'] = [int(most_sold_item['Sold Products']), int(least_sold_item['Sold Products'].iloc[0])]

    # 4 All products Detail
    def conver(x):
        return str(x)

    #### print('')
    # 5 Most Revenue Collecting Product
    most_revenue_item=df[df['Sales']==df['Sales'].max()]
    # print('Name (Most Revenue Collecting Product) :',most_revenue_item['Name'].iloc[0])
    # print('Sales :',most_revenue_item['Sales'].iloc[0])
    daraz_dict['most_revenue_product_name5']=most_revenue_item['Name'].iloc[0]
    daraz_dict['most_revenue_product_sale5']=most_revenue_item['Sales'].iloc[0]

    def setvalue(x):
        if len(x)>26:
            x = str(x)
            x = ' '.join(x.split()[:3])
        return x

    # all product details in term of sales
    top10_sale_product=df.sort_values(by='Sales', ascending=False)
    # print(list(top10_sale_product['Sales'].head(10)), list(top10_sale_product['Name'].head(10)))
    daraz_dict['top15_sale_product_name'] = list(top10_sale_product['Name'].apply(setvalue).head(15))
    daraz_dict['top15_sale_product_amount'] = list(top10_sale_product['Sales'].head(15))
    top10_sale_product['Date']=top10_sale_product['Date'].dt.date

    daraz_dict['all_product_sale_detail_date']=list(top10_sale_product['Date'].apply(conver))
    daraz_dict['all_product_sale_detail_title'] = list(top10_sale_product['Product Title'])
    daraz_dict['all_product_sale_detail_amount'] = list(top10_sale_product['Sold Products'])
    daraz_dict['all_product_sale_detail_sales'] = list(top10_sale_product['Sales'])





    #### print('')
    # 3 top 10/15 most sold items
    top10_sold_product=df.sort_values(by='Sold Products', ascending=False)
    # print(list(top10_sold_product['Sold Products'].head(10)),list(top10_sold_product['Name'].head(10)))
    daraz_dict['top15_sold_product_name']=list(top10_sold_product['Name'].apply(setvalue).head(15))
    daraz_dict['top15_sold_product_amount']=list(top10_sold_product['Sold Products'].head(15))
    top10_sold_product['Date']=top10_sold_product['Date'].dt.date


    daraz_dict['all_product_detail_date']=list(top10_sold_product['Date'].apply(conver))
    daraz_dict['all_product_detail_title'] = list(top10_sold_product['Product Title'])
    daraz_dict['all_product_detail_amount'] = list(top10_sold_product['Sold Products'])
    daraz_dict['all_product_detail_sales'] = list(top10_sold_product['Sales'])

    # Sold vs Not Sold Products Percentages
    zero_amount = len(df['Sold Products'][df['Sold Products'] == 0])
    non_zero_amount = len(df['Sold Products'][df['Sold Products'] != 0])
    # print("Not Sold Products :{}%".format(round(zero_amount / len(df) * 100, 1)))
    # print("Sold Products :{}%".format(round(non_zero_amount / len(df) * 100, 1)))
    daraz_dict['sold_product_percent']=round(zero_amount / len(df) * 100,1)
    daraz_dict['notsold_product_percent']=round(non_zero_amount / len(df) * 100, 1)


    # Distribution of data Using Percentail
    daraz_dict=percentiles(df,daraz_dict)

    # Repeated Products Details
    daraz_dict=repeated(df,daraz_dict)

    # Top15 most repeated Products
    daraz_dict=most_repeated(df,daraz_dict)

    # Raw
    print("Number of Products :",len(df))
    print("How many Product Not Sold Sngle Product :",len(df['Sold Products'][df['Sold Products']==0]))
    print("How many Product Sold one or more Product :",len(df['Sold Products'][df['Sold Products'] != 0]))
    print("Average Sales :",statistics.mean(df['Sold Products'][df['Sold Products'] != 0]))
    zz=df[df['Sold Products']!=0]





    # plt.scatter(zz['Price'],zz['Sold Products'])

    # zz = df[df['Sold Products'] == 0]
    # plt.scatter(zz['Price'], zz['Sold Products'])
    # plt.scatter(zz['Price'],zz['Sales'])


    # plt.plot()
    # plt.show()

    # print('')
    # # Information about dataset
    # print(df.info())
    # print(df.describe())


    print(len(df[df['Product Title'].duplicated()]))
    print(df['Name'].duplicated().sum())



    # # sn.heatmap(df.corr(),annot=True)
    # # plt.show()
    # # img=sn.heatmap(df.corr(),annot=True)
    # # img=img.get_figure()
    # # img.savefig('heatmap.png')
    # # sn.histplot(df['Price'])
    # # plt.show()
    # # plt.hist(df['Sold Products'],10)
    # # plt.show()
    #
    # # overall best date of store sold items
    #
    # solddata = df.groupby(df['Date'])
    # for k, j in solddata:
    #     # j=pd.DataFrame(j)
    #     print(k)
    #     # print(j['Sold Products'].sum())
    #     n = j['Name'].head(30)
    #     s = j['Sold Products'].head(30)
    #     # p=j['Price'].head(30)
    #     plt.barh(n, s)
    #     # plt.plot(p,n)
    #     plt.tight_layout()
    #     plt.show()
    #     j = j.sort_values(by=['Sold Products'], ascending=False)
    #     print(list(j['Name']))
    #     print(list(j['Sold Products']))
    #     c1 = plt.barh(j['Name'].head(20), j['Sold Products'].head(20))
    #     c1 = plt.plot(j['Price'].head(20), j['Name'].head(20), color='red')
    #     plt.tight_layout()
    #     plt.show()
    #
    # dates = [str(k) for k, j in solddata]
    # solditems = [j['Sold Products'].sum() for k, j in solddata]
    #
    # print(dates, solditems)
    #
    # sn.barplot(dates, solditems)
    # plt.show()
    #
    # # sales amount wises best date
    # sale = [j['Sales'].sum() for k, j in solddata]
    # print(sale)
    # plt.bar(dates, sale)
    #
    # plt.show()
    return daraz_dict


# daraz_analysis_function('C:\Users\Muhammad Umair\PycharmProjects\ProductHunt\producthuntproject\media\darazdata')
# print(os.getcwd())