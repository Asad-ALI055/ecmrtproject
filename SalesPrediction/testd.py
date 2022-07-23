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


# advertising = pd.DataFrame(pd.read_csv("advertising.csv"))
# advertising.head()
advertising=pd.read_csv('monthly_champagne_sales.csv')


advertising.info()
advertising.describe()

# Checking Null values
advertising.isnull().sum()*100/advertising.shape[0]
# There are no NULL values in the dataset, hence it is clean.

# Outlier Analysis
# fig, axs = plt.subplots(3, figsize = (5,5))
# plt1 = sns.boxplot(advertising['TV'], ax = axs[0])
# plt2 = sns.boxplot(advertising['Newspaper'], ax = axs[1])
# plt3 = sns.boxplot(advertising['Radio'], ax = axs[2])
# plt.tight_layout()

# Let's see how Sales are related with other variables using scatter plot.
advertising['Month']=[i for i in range(1,len(advertising['Month'])+1)]
sns.pairplot(advertising, x_vars=['Month'], y_vars='Sales', height=4, aspect=1, kind='scatter')
plt.show()


# Let's see the correlation between different variables.
# sns.heatmap(advertising.corr(), cmap="YlGnBu", annot = True)
# plt.show()


# X = advertising['TV']
# Y = advertising['Sales']
X=advertising['Month']
Y=advertising['Sales']


x=np.array(X).reshape(-1,1)
y=np.array(Y).reshape(-1,1)

X_train, X_test, y_train, y_test = train_test_split(x, y, train_size = 0.7, test_size = 0.3, random_state = 100)
# Let's now take a look at the train dataset


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


plt.scatter(X_train, y_train)
# plt.plot(X_train, 6.948 + 0.054*X_train, 'r')
plt.plot(X_train, model.intercept_ + model.coef_*X_train, 'r')
plt.show()

print(model.predict([[4.1]]))