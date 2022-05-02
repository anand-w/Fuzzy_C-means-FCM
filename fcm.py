import pandas as pd
import numpy as np
import random
import operator
import math

# Reading the Input Data

df_full = pd.read_csv("C:\sparkCourse\Fuzzy-C-Means\Data.csv")
columns = list(df_full.columns)
features = columns[:len(columns)-1]
class_labels = list(df_full[columns[-1]])
df = df_full[features]


# Number of Attributes
num_attr = len(df.columns) - 1

# Number of Clusters to make
k = 2

# Maximum number of iterations
MAX_ITER = 100

# Number of data points
n = len(df)

# Fuzzy parameter
m = 2.00

# Step 1 : Initializing the Membership Matrix with Random Values

# initializing the membership matrix with random values

def initializeMembershipMatrix():
    membership_mat = list()
    for i in range(n):
        random_num_list = [random.random() for i in range(k)]
        summation = sum(random_num_list)
        temp_list = [x/summation for x in random_num_list]
        membership_mat.append(temp_list)
    return membership_mat


# Step 2 : Calculating the Cluster Center

def calculateClusterCenter(membership_mat):
    cluster_mem_val = list(zip(*membership_mat))
    cluster_centers = list()
    for j in range(k):
        x = list(cluster_mem_val[j])
        xraised = [e ** m for e in x]
        denominator = sum(xraised)
        temp_num = list()
        for i in range(n):
            data_point = list(df.iloc[i])
            prod = [xraised[i] * val for val in data_point]
            temp_num.append(prod)
        numerator = list(map(sum, list(zip(*temp_num))))
        center = [z/denominator for z in numerator]
        cluster_centers.append(center)
    return cluster_centers

#Step 3 : Updating Membership Values using Cluster Centers from Step 2

# updating the membership values using the cluster centers

def updateMembershipValue(membership_mat, cluster_centers):
    p = float(2/(m-1))
    for i in range(n):
        x = list(df.iloc[i])
        distances = [np.linalg.norm(list(map(operator.sub, x, cluster_centers[j]))) for j in range(k)]
        for j in range(k):
            den = sum([math.pow(float(distances[j]/distances[c]), p) for c in range(k)])
            membership_mat[i][j] = float(1/den)       
    return membership_mat


# Function defined which returns the Clusters from the Membership Matrix

def getClusters(membership_mat):
    cluster_labels = list()
    for i in range(n):
        max_val, idx = max((val, idx) for (idx, val) in enumerate(membership_mat[i]))
        cluster_labels.append(idx)
    return cluster_labels


# Calling fcm function which runs for MAX_ITER number of times and returns the Result

# the final fcm function, 

def fuzzyCMeansClustering():
    # Membership Matrix
    membership_mat = initializeMembershipMatrix()
    curr = 0
    while curr <= MAX_ITER:
        cluster_centers = calculateClusterCenter(membership_mat)
        membership_mat = updateMembershipValue(membership_mat, cluster_centers)
        cluster_labels = getClusters(membership_mat)
        curr += 1
    
    print(membership_mat)
    return cluster_labels, cluster_centers


# Displaying the Results
#Outputting Cluster Labels and Cluster Centers

# calling the main function and storing the final results in labels, centers

print("printing the final membership matrix")

labels, centers = fuzzyCMeansClustering()

print("printing cluster centers")
print(centers)

# Utility Function for Evaluating the Result

# accuracy function for measuring the accuracy of our result

def accuracy(cluster_labels, class_labels):
    county = [0,0]
    countn = [0,0]
    tp = [0, 0]
    tn = [0, 0]
    fp = [0, 0]
    fn = [0, 0]
    
    for i in range(len(df)):
        # Yes = 1, No = 0
        if cluster_labels[i] == 1 and class_labels[i] == 'Yes':
            tp[0] = tp[0] + 1
        if cluster_labels[i] == 0 and class_labels[i] == 'No':
            tn[0] = tn[0] + 1
        if cluster_labels[i] == 1 and class_labels[i] == 'No':
            fp[0] = fp[0] + 1
        if cluster_labels[i] == 0 and class_labels[i] == 'Yes':
            fn[0] = fn[0] + 1
    
    for i in range(len(df)):
        # Yes = 0, No = 1
        if cluster_labels[i] == 0 and class_labels[i] == 'Yes':
            tp[1] = tp[1] + 1
        if cluster_labels[i] == 1 and class_labels[i] == 'No':
            tn[1] = tn[1] + 1
        if cluster_labels[i] == 0 and class_labels[i] == 'No':
            fp[1] = fp[1] + 1
        if cluster_labels[i] == 1 and class_labels[i] == 'Yes':
            fn[1] = fn[1] + 1
    
    a0 = float((tp[0] + tn[0]))/(tp[0] + tn[0] + fn[0] + fp[0])
    a1 = float((tp[1] + tn[1]))/(tp[1] + tn[1] + fn[1] + fp[1])
    p0 = float(tp[0])/(tp[0] + fp[0])
    p1 = float(tp[1])/(tp[1] + fp[1])
    r0 = float(tp[0])/(tp[0] + fn[0])
    r1 = float(tp[1])/(tp[1] + fn[1])
    
    accuracy = [a0*100,a1*100]
    precision = [p0*100,p1*100]
    recall = [r0*100,r1*100]
    
    return accuracy, precision, recall


# Outputting the accuracy achieved

# measuring the accuracy of the result

a,p,r = accuracy(labels, class_labels)

print("Accuracy = " + str(a))
print("Precision = " + str(p))
print("Recall = " + str(r))




