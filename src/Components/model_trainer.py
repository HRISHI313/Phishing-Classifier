import pandas as pd
import numpy as np
from src.logger import logging
from src.utils import read_mongodb

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns


# Step 2 read the files
legitimate_df = pd.read_csv("artifacts/structured_data_legitimate.csv")
phishing_df = pd.read_csv("artifacts/structured_data_phishing.csv")
logging.info('Importing data')

# Step 3 combine legitimate and phishing dataframes, and shuffle
logging.info("initiated combining legitimate and phishing dataframes, and shuffle")
df = pd.concat([legitimate_df, phishing_df], axis=0)
df = df.sample(frac=1)
logging.info("combining legitimate and phishing dataframes, and shuffle completed")

# Step 4 remove 'url' and remove duplicates, then we can create X and Y for the models, Supervised Learning
df = df.drop('URL', axis=1)
df = df.drop_duplicates()
X = df.drop('label', axis=1)
Y = df['label']
logging.info("Removing 'url' and remove duplicates, then we can create X and Y for the models")

# Step 5 split data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=10)
logging.info("spliting data into train and test sets")

# Step 6 create a ML model using sklearn
svm_model = svm.LinearSVC()

# Random Forest
rf_model = RandomForestClassifier(n_estimators=60)

# Decision Tree
dt_model = tree.DecisionTreeClassifier()

# AdaBoost
ab_model = AdaBoostClassifier()

# Gaussian Naive Bayes
nb_model = GaussianNB()


# KNeighborsClassifier
kn_model = KNeighborsClassifier()

logging.info("create a ML models using sklearn ---> Support Vector Machine, Random Forest, Decision Tree,AdaBoost,Gaussian Naive Bayes ")


# Step 7 train the model
logging.info("")
svm_model.fit(x_train, y_train)


# Step 8 make some predictions using test data
predictions = svm_model.predict(x_test)


# Step 9 create a confusion matrix and tn, tp, fn , fp
tn, fp, fn, tp = confusion_matrix(y_true=y_test, y_pred=predictions).ravel()


# Step 10 calculate accuracy, precision and recall scores
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)

print("accuracy --> ", accuracy)
print("precision --> ", precision)
print("recall --> ", recall)


# K-fold cross validation, and K = 5
logging.info("Initiated K-Fold Validation with K = 5")
K = 5
total = X.shape[0]
index = int(total / K)

# 1
X_1_test = X.iloc[:index]
X_1_train = X.iloc[index:]
Y_1_test = Y.iloc[:index]
Y_1_train = Y.iloc[index:]

# 2
X_2_test = X.iloc[index:index*2]
X_2_train = X.iloc[np.r_[:index, index*2:]]
Y_2_test = Y.iloc[index:index*2]
Y_2_train = Y.iloc[np.r_[:index, index*2:]]

# 3
X_3_test = X.iloc[index*2:index*3]
X_3_train = X.iloc[np.r_[:index*2, index*3:]]
Y_3_test = Y.iloc[index*2:index*3]
Y_3_train = Y.iloc[np.r_[:index*2, index*3:]]

# 4
X_4_test = X.iloc[index*3:index*4]
X_4_train = X.iloc[np.r_[:index*3, index*4:]]
Y_4_test = Y.iloc[index*3:index*4]
Y_4_train = Y.iloc[np.r_[:index*3, index*4:]]

# 5
X_5_test = X.iloc[index*4:]
X_5_train = X.iloc[:index*4]
Y_5_test = Y.iloc[index*4:]
Y_5_train = Y.iloc[:index*4]


# X and Y train and test lists
X_train_list = [X_1_train, X_2_train, X_3_train, X_4_train, X_5_train]
X_test_list = [X_1_test, X_2_test, X_3_test, X_4_test, X_5_test]

Y_train_list = [Y_1_train, Y_2_train, Y_3_train, Y_4_train, Y_5_train]
Y_test_list = [Y_1_test, Y_2_test, Y_3_test, Y_4_test, Y_5_test]
logging.info("X and Y train and test lists")


def calculate_measures(TN, TP, FN, FP):
    model_accuracy = (TP + TN) / (TP + TN + FN + FP)
    model_precision = TP / (TP + FP)
    model_recall = TP / (TP + FN)
    return model_accuracy, model_precision, model_recall


rf_accuracy_list, rf_precision_list, rf_recall_list = [], [], []
dt_accuracy_list, dt_precision_list, dt_recall_list = [], [], []
ab_accuracy_list, ab_precision_list, ab_recall_list = [], [], []
svm_accuracy_list, svm_precision_list, svm_recall_list = [], [], []
nb_accuracy_list, nb_precision_list, nb_recall_list = [], [], []
kn_accuracy_list, kn_precision_list, kn_recall_list = [], [], []



for i in range(0, K):
    # ----- RANDOM FOREST ----- #
    rf_model.fit(X_train_list[i], Y_train_list[i])
    rf_predictions = rf_model.predict(X_test_list[i])
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test_list[i], y_pred=rf_predictions).ravel()
    rf_accuracy, rf_precision, rf_recall = calculate_measures(tn, tp, fn, fp)
    rf_accuracy_list.append(rf_accuracy)
    rf_precision_list.append(rf_precision)
    rf_recall_list.append(rf_recall)
    logging.info("Random forest got trained")

    # ----- DECISION TREE ----- #
    dt_model.fit(X_train_list[i], Y_train_list[i])
    dt_predictions = dt_model.predict(X_test_list[i])
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test_list[i], y_pred=dt_predictions).ravel()
    dt_accuracy, dt_precision, dt_recall = calculate_measures(tn, tp, fn, fp)
    dt_accuracy_list.append(dt_accuracy)
    dt_precision_list.append(dt_precision)
    dt_recall_list.append(dt_recall)
    logging.info("Decision tree got trained")

    # ----- SUPPORT VECTOR MACHINE ----- #
    svm_model.fit(X_train_list[i], Y_train_list[i])
    svm_predictions = svm_model.predict(X_test_list[i])
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test_list[i], y_pred=svm_predictions).ravel()
    svm_accuracy, svm_precision, svm_recall = calculate_measures(tn, tp, fn, fp)
    svm_accuracy_list.append(svm_accuracy)
    svm_precision_list.append(svm_precision)
    svm_recall_list.append(svm_recall)
    logging.info("Support vector machine got trained")

    # ----- ADABOOST ----- #
    ab_model.fit(X_train_list[i], Y_train_list[i])
    ab_predictions = ab_model.predict(X_test_list[i])
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test_list[i], y_pred=ab_predictions).ravel()
    ab_accuracy, ab_precision, ab_recall = calculate_measures(tn, tp, fn, fp)
    ab_accuracy_list.append(ab_accuracy)
    ab_precision_list.append(ab_precision)
    ab_recall_list.append(ab_recall)
    logging.info("Ada boost got trained")

    # ----- GAUSSIAN NAIVE BAYES ----- #
    nb_model.fit(X_train_list[i], Y_train_list[i])
    nb_predictions = nb_model.predict(X_test_list[i])
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test_list[i], y_pred=nb_predictions).ravel()
    nb_accuracy, nb_precision, nb_recall = calculate_measures(tn, tp, fn, fp)
    nb_accuracy_list.append(nb_accuracy)
    nb_precision_list.append(nb_precision)
    nb_recall_list.append(nb_recall)
    logging.info("Gaussian naive bayes got trained")


    # ----- K-NEIGHBOURS CLASSIFIER ----- #
    kn_model.fit(X_train_list[i], Y_train_list[i])
    kn_predictions = kn_model.predict(X_test_list[i])
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test_list[i], y_pred=kn_predictions).ravel()
    kn_accuracy, kn_precision, kn_recall = calculate_measures(tn, tp, fn, fp)
    kn_accuracy_list.append(kn_accuracy)
    kn_precision_list.append(kn_precision)
    kn_recall_list.append(kn_recall)
    logging.info("K-neighbours classifier got trained")


RF_accuracy = sum(rf_accuracy_list) / len(rf_accuracy_list)
RF_precision = sum(rf_precision_list) / len(rf_precision_list)
RF_recall = sum(rf_recall_list) / len(rf_recall_list)

print("Random Forest accuracy ==> ", RF_accuracy)
print("Random Forest precision ==> ", RF_precision)
print("Random Forest recall ==> ", RF_recall)
logging.info(f"Accuracy,Precision, and Recall for Random Forest is: {RF_accuracy},{RF_precision},{RF_recall}")


DT_accuracy = sum(dt_accuracy_list) / len(dt_accuracy_list)
DT_precision = sum(dt_precision_list) / len(dt_precision_list)
DT_recall = sum(dt_recall_list) / len(dt_recall_list)

print("Decision Tree accuracy ==> ", DT_accuracy)
print("Decision Tree precision ==> ", DT_precision)
print("Decision Tree recall ==> ", DT_recall)
logging.info(f"Accuracy,Precision, and Recall for Decision tree is: {DT_accuracy},{DT_precision},{DT_recall}")


AB_accuracy = sum(ab_accuracy_list) / len(ab_accuracy_list)
AB_precision = sum(ab_precision_list) / len(ab_precision_list)
AB_recall = sum(ab_recall_list) / len(ab_recall_list)

print("AdaBoost accuracy ==> ", AB_accuracy)
print("AdaBoost precision ==> ", AB_precision)
print("AdaBoost recall ==> ", AB_recall)
logging.info(f"Accuracy,Precision, and Recall for Ada Boost is: {AB_accuracy},{AB_precision},{AB_recall}")


SVM_accuracy = sum(svm_accuracy_list) / len(svm_accuracy_list)
SVM_precision = sum(svm_precision_list) / len(svm_precision_list)
SVM_recall = sum(svm_recall_list) / len(svm_recall_list)

print("Support Vector Machine accuracy ==> ", SVM_accuracy)
print("Support Vector Machine precision ==> ", SVM_precision)
print("Support Vector Machine recall ==> ", SVM_recall)
logging.info("Accuracy,Precision, and Recall for Support Vector Machine is: {SVM_accuracy},{SVM_precision},{SVM_recall}")


NB_accuracy = sum(nb_accuracy_list) / len(nb_accuracy_list)
NB_precision = sum(nb_precision_list) / len(nb_precision_list)
NB_recall = sum(nb_recall_list) / len(nb_recall_list)

print("Gaussian Naive Bayes accuracy ==> ", NB_accuracy)
print("Gaussian Naive Bayes precision ==> ", NB_precision)
print("Gaussian Naive Bayes recall ==> ", NB_recall)
logging.info("Accuracy,Precision, and Recall for Gaussian Naive Bayes is: {NB_accuracy},{NB_precision},{NB_recall}")


KN_accuracy = sum(kn_accuracy_list) / len(kn_accuracy_list)
KN_precision = sum(kn_precision_list) / len(kn_precision_list)
KN_recall = sum(kn_recall_list) / len(kn_recall_list)

print("K-Neighbours Classifier accuracy ==> ", KN_accuracy)
print("K-Neighbours Classifier precision ==> ", KN_precision)
print("K-Neighbours Classifier recall ==> ", KN_recall)
logging.info("Accuracy,Precision, and Recall for K-Neighbours Classifier is: {KN_accuracy},{KN_precision},{KN_recall}")



data = {'accuracy': [NB_accuracy, SVM_accuracy, DT_accuracy, RF_accuracy, AB_accuracy, KN_accuracy],
        'precision': [NB_precision, SVM_precision, DT_precision, RF_precision, AB_precision, KN_precision],
        'recall': [NB_recall, SVM_recall, DT_recall, RF_recall, AB_recall, KN_recall]
        }

index = ['NB', 'SVM', 'DT', 'RF', 'AB', 'KN']

df_results = pd.DataFrame(data=data, index=index)
logging.info("Created the results into a DataFrame")


# visualize the dataframe
ax = df_results.plot.bar(rot=0)
logging.info("visualize the dataframe")

# Calculate confusion matrix
cm_dt = confusion_matrix(y_true=y_test, y_pred=predictions)
print("Confusion Matrix for Decision Tree:")
print(cm_dt)
logging.info("Calculating confusion matrix")


# Plot confusion matrix as heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm_dt, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix - Decision Tree")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()
logging.info("Ploted confusion matrix as heatmap")





