# coding=utf-8
import json, glob, os
import numpy as np
from sklearn.ensemble import RandomForestClassifier

apistats_dir = './data'
select_number = 120

apis = []
fs = glob.glob(os.path.join(apistats_dir, '*.json'))
for f in fs:
    with open(f, 'r') as jsonfile:
        data = json.load(jsonfile)
        capis = data['apistats']
        for api in capis.keys():
            if api not in apis:
                apis.append(api)

n_samples = len(fs)
n_features = len(apis)
loc = {}
for i in range(n_features):
    loc[apis[i]] = i

x = np.zeros((n_samples, n_features))
y = np.zeros((n_samples, ))
for i in range(n_samples):
    with open(fs[i], 'r') as jsonfile:
        data = json.load(jsonfile)
        capis = data['apistats']
        cls = data['class']
        if cls == 'malware':
            y[i] = 1
        for api in capis.keys():
            x[i, loc[api]] = 1

feat_labels = apis   #特征列名
forest = RandomForestClassifier(n_estimators=2000, random_state=0, n_jobs=-1)  #2000棵树,并行工作数是运行服务器决定
forest.fit(x, y)
importances = forest.feature_importances_   #feature_importances_特征列重要性占比
indices = np.argsort(importances)[::-1]     #对参数从小到大排序的索引序号取逆,即最重要特征索引——>最不重要特征索引

standard = []
for f in range(x.shape[1]):
    print("%2d) %-*s %f" % (f + 1, 30, feat_labels[indices[f]], importances[indices[f]]))
    standard.append(feat_labels[indices[f]])
import pandas as pd
standard_pd = pd.DataFrame(standard[:select_number])
standard_pd.to_csv("standard.txt", index=None, header=None)
# remain indices columns
x = x[:, indices[:select_number]]
xmal = x[np.where(y==1)]
ymal = y[np.where(y==1)]
xben = x[np.where(y==0)]
yben = y[np.where(y==0)]


np.savez('data120.npz', xmal=xmal, ymal=ymal, xben=xben, yben=yben)