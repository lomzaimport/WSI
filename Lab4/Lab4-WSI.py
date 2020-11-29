import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, plot_roc_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
from matplotlib import pyplot as plt

X_test = pd.read_csv('adult.test')
X_train = pd.read_csv('adult.data')

le = LabelEncoder()
X_train = X_train[X_train.columns[:]].apply(le.fit_transform)
X_test = X_test[X_test.columns[:]].apply(le.fit_transform)
print(X_test)

X_test = X_test.drop(['education'], axis=1)
X_train = X_train.drop(['education'], axis=1)

y_train = X_train['salary']
y_test = X_test['salary']

X_train = X_train.drop(['salary'],axis=1)
X_test = X_test.drop(['salary'],axis=1)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

score = accuracy_score(y_test, y_pred)
print(score)

plot = plot_roc_curve(clf, X_test, y_test)
plt.show()


