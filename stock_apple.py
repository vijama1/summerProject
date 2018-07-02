import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('Apple.csv')

train_data = df[['Open','High','Low','Adj Close','Volume']]
train_target = df[['Close']]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(train_data,train_target)

# Make predictions using the testing set-------2d required
#y_pred = regr.predict(df[['Open','High','Low','Adj Close','Volume']])
y_pred = regr.predict([[187.74, 190.37,187.65, 189.31, 27989300]])
print(round(y_pred[0][0],3))
print('Coefficients: \n', regr.coef_)
conv_var =0
conv_var = round(y_pred[0][0],3)
print(conv_var)
# 187.74	190.37	187.65	189.31	27,989,300

'''
print("Mean squared error: %.2f"
      % mean_squared_error(df[['Close']], y_pred))

plt.plot(df['Date'],df['Close'])
plt.plot(df['Date'],y_pred,color='r')
plt.xticks(())
plt.yticks(())

plt.show()
'''
'''
Low : 184.03
High	187.28
Open	185.23
vol      25,037,500
adj close 184.16
'''
