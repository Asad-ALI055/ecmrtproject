import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn import linear_model

# Super store

# df=pd.read_excel('Sample - Superstore.xls')
# # print(df.head())
# # print(df.to_string)
#
# print(df.info())
# print(df.corr())
#
# df['Order Date']=pd.to_datetime(df['Order Date'])
#
# df['year']=df['Order Date'].dt.year
# print(df['Order Date'].dt.year)
# print(df['year'].unique())
# # sn.heatmap(df.corr(),annot=True)
# plt.bar(sorted(df['year'].unique()),sorted(df.groupby(df['year']).sum()['Sales']))
# plt.show()
#
#

def linear_prediction(path,target_column,x_column):
    dict_predict={}

    # read file
    advertising_df = pd.read_csv(path)

    # print(advertising_df.info())
    # print(advertising_df.describe())

    # Checking Null values
    print(advertising_df.isnull().sum()*100/advertising_df.shape[0])

    # Remove Null values
    advertising_df=advertising_df.dropna()

    # There are no NULL values in the dataset, hence it is clean.

    # Outlier Analysis
    # fig, axs = plt.subplots(3, figsize = (5,5))
    # plt1 = sns.boxplot(advertising['TV'], ax = axs[0])
    # plt2 = sns.boxplot(advertising['Newspaper'], ax = axs[1])
    # plt3 = sns.boxplot(advertising['Radio'], ax = axs[2])
    # plt.tight_layout()


    dict_predict['orignal_x']=list(advertising_df[x_column])
    dict_predict['orignal_y']=list(advertising_df[target_column])
    # print(dict_predict['orignal_x'])

    # Let's see how Sales are related with other variables using scatter plot.
    # sns.pairplot(advertising, x_vars=['TV', 'Newspaper', 'Radio'], y_vars='Sales', height=4, aspect=1, kind='scatter')
    # plt.show()


    # Let's see the correlation between different variables.
    # sns.heatmap(advertising.corr(), cmap="YlGnBu", annot = True)
    # plt.show()


    X = advertising_df[x_column]
    Y = advertising_df[target_column]
    # X=advertising['YearsExperience']
    # Y=advertising['Salary']


    x=np.array(X).reshape(-1,1)
    y=np.array(Y).reshape(-1,1)

    # split data into training & testing
    X_train, X_test, y_train, y_test = train_test_split(x, y, train_size = 0.7, test_size = 0.3, random_state = 100)

    #or
    # # Add a constant to get an intercept
    # X_train_sm = sm.add_constant(X_train)
    #
    # # Fit the resgression line using 'OLS'
    # lr = sm.OLS(y_train, X_train_sm).fit()

    #or
    model=linear_model.LinearRegression()
    model.fit(X_train,y_train)


    print(f"Coeficient : {model.coef_}")     #coeficient
    print(f"Intercept : {model.intercept_}")  #intercept
    accuracy=model.score(X_test,y_test)
    print(f"Accuracy : {round(accuracy*100,2)}")

    dict_predict['x_train']=[float(i) for i in X_train]
    dict_predict['y_train']=[float(i) for i in y_train]
    predicted_values=model.intercept_ + model.coef_*X_train
    dict_predict['predict_values']=[round(float(i),1) for i in predicted_values]

    # print(dict_predict['predict_values'])

    # plt.scatter(X_train, y_train)
    ## plt.plot(X_train, 6.948 + 0.054*X_train, 'r')
    # plt.plot(X_train, predicted_values, 'r')
    # plt.show()

    # print(model.predict([[4.1]]))
    dict_predict['intercept_value']=model.intercept_
    dict_predict['coef_value']=model.coef_
    return dict_predict


# linear_prediction('advertising.csv','Sales','TV')