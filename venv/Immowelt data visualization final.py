import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
import numpy as np

# read csv file with ; as delimiter
df = pd.read_csv('c:\\Temp\\houselist_df.csv', delimiter=";")

# descriptive statistics
print('Data-count')
print(df.count())
print('Price min, mean, max')
print(df['Price'].min())
print(df['Price'].mean(0))
print(df['Price'].max(0))

print('Livingspace min, mean, max')
print(df['Livingspace'].min())
print(df['Livingspace'].mean(0))
print(df['Livingspace'].max(0))

print('Rooms min, mean, max')
print(df['Room'].min())
print(df['Room'].mean(0))
print(df['Room'].max(0))

print('Plotsize min, mean, max')
print(df['Plotsize'].min())
print(df['Plotsize'].mean(0))
print(df['Plotsize'].max(0))

print('Distance min, mean, max')
print(df['Distance'].min())
print(df['Distance'].mean(0))
print(df['Distance'].max(0))

# clean data: Livingspace less or equal to 300 m², less than 21 rooms, plotsize smaller than 5001
df_clean = df.loc[(df['Livingspace'] <= 300) & (df['Room'] <= 20) & (df['Plotsize'] <= 5000)]

# validate data
print('Data-count')
print(df_clean.count())
print('Price min, mean, max')
print(df_clean['Price'].min())
print(df_clean['Price'].mean(0))
print(df_clean['Price'].max(0))

print('Livingspace min, mean, max')
print(df_clean['Livingspace'].min())
print(df_clean['Livingspace'].mean(0))
print(df_clean['Livingspace'].max(0))

print('Rooms min, mean, max')
print(df_clean['Room'].min())
print(df_clean['Room'].mean(0))
print(df_clean['Room'].max(0))

print('Plotsize min, mean, max')
print(df_clean['Plotsize'].min())
print(df_clean['Plotsize'].mean(0))
print(df_clean['Plotsize'].max(0))

print('Distance min, mean, max')
print(df_clean['Distance'].min())
print(df_clean['Distance'].mean(0))
print(df_clean['Distance'].max(0))

# Price to k to get a better scale
df_clean['Price'] = df_clean['Price'].div(1000)

# regression plot to extrapolate
fig = sns.regplot(x="Distance", y="Price", data=df_clean)
fig.set(xlabel='Distance (KM)', ylabel='Price in thousands (€)')
plt.title("Regression Distance and Price")
plt.savefig('c:\\temp\\regression price Distance.png')
plt.show()

# clustering with kmeans
kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=300, n_init=10, random_state=0).fit(df_clean)
centroids = kmeans.cluster_centers_
labels = kmeans.fit(df_clean)
print('labels')
print(labels.labels_)
print('centroids')
print(centroids)
colors = np.array(["Red", "Green", "Blue"])
plt.scatter(x=df_clean["Price"], y=df_clean["Livingspace"], c=colors[kmeans.labels_], s=50, alpha=0.5)
plt.xlabel("Livingspace (m²)")
plt.ylabel("Price in thousands (€)")
plt.title("K means Classification")
plt.savefig('c:\\temp\\K means Classification1.png')
plt.show()

plt.scatter(df_clean['Price'], df_clean['Livingspace'], c=kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='blue', s=50)
plt.legend(kmeans.labels_)
plt.xlabel("Livingspace (m²)")
plt.ylabel("Price in thousands (€)")
plt.title("K means Classification")
plt.savefig('c:\\temp\\K means Classification2.png')
plt.show()

# calculate the correlation matrix
corr = df_clean.corr()
sns.heatmap(corr, cmap="Blues", annot=True)
plt.savefig('c:\\temp\\heatmap correlation1.png')
plt.show()

# plot the heatmap in red
sns.heatmap(corr,
            xticklabels=corr.columns,
            yticklabels=corr.columns, annot=True)
plt.savefig('c:\\temp\\heatmap correlation2.png')
plt.show()

# regression plot to extrapolate
sns.regplot(x="Price",
            y="Livingspace",
            data=df_clean)
plt.ylabel("Livingspace (m²)")
plt.xlabel("Price in thousands (€)")
plt.title("Regression Price & Living-space")
plt.savefig('c:\\temp\\regression price liviginspace.png')
plt.show()

# plot livingspace and price
df_clean.plot(x='Livingspace', y='Price', style='o')
plt.xlabel("Livingspace (m²)")
plt.ylabel("Price in thousands (€)")
plt.title("Price & Living-space")
plt.savefig('c:\\temp\\plot price livingspace.png')
plt.show()

# scatterplot livingspace and price
sns.scatterplot(x="Livingspace", y="Price", data=df_clean)
plt.savefig('c:\\temp\\scatterplot price livingspace.png')
plt.xlabel("Livingspace (m²)")
plt.ylabel("Price in thousands (€)")
plt.title("Scatterplot Price & Living-space")
plt.show()

# show relations
sns.relplot(x="Livingspace", y="Plotsize", size="Price", sizes=(0, 300), data=df_clean)
plt.xlabel("Livingspace (m²)")
plt.ylabel("Plotsize (m²)")
plt.title("Relations Price & Living-space & Plotsize")
plt.savefig('c:\\temp\\relations Plotsize livingspace Price.png')
plt.show()

# show relations
sns.relplot(x="Distance", y="Livingspace", size="Price", sizes=(0, 300), data=df_clean)
plt.xlabel("Distance (KM)")
plt.ylabel("Living-space (m²)")
plt.title("Relations Price & Living-space & Distance")
plt.savefig('c:\\temp\\relations Distance Price livingspace.png')
plt.show()

# show relations
sns.relplot(x="Distance", y="Livingspace", size="Plotsize", sizes=(0, 300), data=df_clean)
plt.xlabel("Distance (KM)")
plt.ylabel("Living-space (m²)")
plt.title("Relations Plotsize & Living-space & Distance")
plt.savefig('c:\\temp\\relations Distance Price Plotsize.png')
plt.show()
