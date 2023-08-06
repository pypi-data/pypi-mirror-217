import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def Analysis_Visualization():
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']
    data = pd.read_csv('transformdata.csv')
    k = 4
    iteration = 1000
    kmodel = KMeans(n_clusters=k, max_iter=iteration)
    kmodel.fit(data)
    r1 = pd.Series(kmodel.labels_).value_counts()
    r2 = pd.DataFrame(kmodel.cluster_centers_)
    r = pd.concat([r1, r2], axis=1)
    r.columns = [u'ClusterNum'] + list(data.columns)
    print(r)
    r3 = pd.Series(kmodel.labels_, index=data.index)
    r = pd.concat([data, r3], axis=1)
    r.columns = list(data.columns) + [u'ClusterCategory']
    r.to_csv('04data_type.csv')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    for i in range(k):
        cls = data[r[u'ClusterCategory'] == i]
        cls.plot(kind='kde', linewidth=2, subplots=True, sharex=False)
        plt.suptitle('Prevention_Control=%d;ClusterNum=%d' % (i, r1[i]))
        plt.subplots_adjust(wspace=0, hspace=0.5)
    plt.legend()
    return plt.show()
Analysis_Visualization()