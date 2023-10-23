from utils import collection_creation, fetch_records, data_info
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score


# Connect to the Stackoverflow collection in Mongodb
stackoverflow_scraped_data = collection_creation('Stackoverflow_Scraped')

# Save data in a dataframe
records = [record for record in fetch_records(stackoverflow_scraped_data)]
raw_data_df = pd.DataFrame(records)
raw_data_df = raw_data_df.set_index('_id')

# Convert badge_count dictionary column into new separate columns
raw_data_df = pd.concat([raw_data_df.drop(['badge_counts'], axis = 1), raw_data_df['badge_counts'].apply(pd.Series)], axis = 1)

# Method called from data_information.py
data_info(raw_data_df)

# Function to calculate and return the columns having a correlation coefficient greater than a specified threshold
def correlation(dataset, correlation_threshold):
    col_corr = set()
    
    # Select only numeric columns for correlation calculation
    numeric_columns = dataset.select_dtypes(include = ['int64', 'float', 'int', 'int32'])
    
    corr_matrix = numeric_columns.corr()
    for x in range(len(corr_matrix.columns)):
        for y in range(x):
            if corr_matrix.iloc[x, y] > correlation_threshold:
                col_name = corr_matrix.columns[x]
                col_corr.add(col_name)
    return col_corr

# Dropping highly correlated features
corr_features = correlation(raw_data_df, 0.8)
filtered_data_df = raw_data_df.drop(corr_features,axis=1)

# Feature selection for model
#check this line -------------------
features_selected = filtered_data_df.select_dtypes(include = ['int64', 'float', 'int','int32'])

# Feature scaling using standardization
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features_selected)

# # Check optimal number of clusters using the Elbow Method
# inertia_values = []

# for i in range(1, 11):
#     kmeans = KMeans(n_clusters = i, init = "k-means++", n_init = 10, max_iter = 300, random_state = 47)
#     kmeans.fit(scaled_features)
#     inertia_values.append(kmeans.inertia_)

# # Plot the Elbow Method
# plt.figure(figsize = (8, 6))
# plt.plot(range(1, 11), inertia_values, marker='o', linestyle='--')
# plt.xlabel('Number of Clusters')
# plt.ylabel('Inertia Values')
# plt.title('Elbow Method to find optimal number of clusters for KMeans')
# plt.show()

# Running KMeans algorithm
kmeans = KMeans(n_clusters = 2, init = "k-means++", n_init = 10, max_iter = 300, random_state = 11)

kmeans.fit(scaled_features)

# Appending newly created 'selected' column to the DataFrame.
raw_data_df['selected'] = [True if label == 1 else False for label in kmeans.labels_]

# Printing count of selected and not selected candidates
print(raw_data_df['selected'].value_counts())

# Defining prediction variable and features
x = scaled_features
y = raw_data_df['selected']

# Splitting data in train and test
train_x, testing_x, train_y, testing_y = train_test_split(x, y, test_size = 0.3)

# Splitting test data into test and validation
test_x, val_x, test_y, val_y = train_test_split(testing_x, testing_y)

# Create model
model = LogisticRegression(solver='liblinear')

# Model fitting
model.fit(train_x, train_y)
# Model score on train data
score = model.score(train_x, train_y)
print("The model score is ",score)

# Confusion matrix on test data
matrix_1 = confusion_matrix(test_y, model.predict(test_x))
print(matrix_1)
# Confusion matrix output format:
# [True Positive, False Negative]
# [False Positive, True Negative]

# matrix_2 = confusion_matrix(val_y, model.predict(val_x))
# print(matrix_2)

# Accuracy on test data
accuracy = accuracy_score(test_y, model.predict(test_x))
print("Accuracy:", accuracy,"%")