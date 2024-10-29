
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(".csv")

df.hist(bins=20, figsize=(15, 10))
plt.suptitle('Feature Distributions')
plt.show()

def correlationheatmap(data):
    correlation = data.corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    cax = ax.matshow(correlation, cmap='coolwarm')
    plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=90)
    plt.yticks(range(len(correlation.columns)), correlation.columns)
    fig.colorbar(cax)
    plt.title('Correlation Heatmap', pad=20)
    plt.show()
correlationheatmap(df)

X = df.drop('target', axis=1).values
y = df['target'].values

X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
X = np.hstack((np.ones((X.shape[0], 1)), X))
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
def compute_loss(y, y_hat):
    return -np.mean(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))

def gradient_descent(X, y, weights, learning_rate, num_iterations):
    m = len(y)
    for i in range(num_iterations):
        z = np.dot(X, weights)
        y_hat = sigmoid(z)
        gradients = np.dot(X.T, (y_hat - y)) / m
        weights -= learning_rate * gradients
        if i % 1000 == 0:
            loss = compute_loss(y, y_hat)
            print(f"Iteration {i}, Loss: {loss}")
    return weights

np.random.seed(50)
weights = np.random.rand(X.shape[1])
learning_rate = 0.01
num_iterations = 100000

weights = gradient_descent(X, y, weights, learning_rate, num_iterations)
def predict(X, weights):
    z = np.dot(X, weights)
    return sigmoid(z) >= 0.5

y_pred = predict(X, weights)

def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

def precision(y_true, y_pred):
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    predicted_positives = np.sum(y_pred == 1)
    return true_positives / predicted_positives if predicted_positives != 0 else 0

def recall(y_true, y_pred):
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    actual_positives = np.sum(y_true == 1)
    return true_positives / actual_positives if actual_positives != 0 else 0

def f1_score(y_true, y_pred):
    prec = precision(y_true, y_pred)
    rec = recall(y_true, y_pred)
    return 2 * (prec * rec) / (prec + rec) if (prec + rec) != 0 else 0
print(f"Accuracy: {accuracy(y, y_pred)}")
print(f"Precision: {precision(y, y_pred)}")
print(f"Recall: {recall(y, y_pred)}")
print(f"F1-Score: {f1_score(y, y_pred)}")

feature_names = ['Intercept'] + list(df.drop('target', axis=1).columns)
coefficients = weights

plt.figure(figsize=(10, 6))
plt.barh(feature_names, coefficients, color='blue')
plt.title("Feature Coefficients (Effect on Prediction)")
plt.xlabel("Coefficient Value")
plt.ylabel("Feature")
plt.show()

def plot_confusion_matrix(y_true, y_pred):
    cm = np.zeros((2, 2))
    cm[0, 0] = np.sum((y_true == 0) & (y_pred == 0))  # True negatives
    cm[0, 1] = np.sum((y_true == 0) & (y_pred == 1))  # False positives
    cm[1, 0] = np.sum((y_true == 1) & (y_pred == 0))  # False negatives
    cm[1, 1] = np.sum((y_true == 1) & (y_pred == 1))  # True positives

    fig, ax = plt.subplots()
    cax = ax.matshow(cm, cmap='Blues')
    plt.title('Confusion Matrix')
    fig.colorbar(cax)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')

    for (i, j), value in np.ndenumerate(cm):
        ax.text(j, i, int(value), ha='center', va='center', color='black')

    plt.show()

plot_confusion_matrix(y, y_pred)

def plot_roc_curve(X, y, weights):
    z = np.dot(X, weights)
    y_hat = sigmoid(z)
    fpr, tpr, thresholds = [], [], []

# Compute FPR, TPR at different thresholds
    for threshold in np.linspace(0, 1, 100):
        y_pred_threshold = y_hat >= threshold
        true_positives = np.sum((y == 1) & (y_pred_threshold == 1))
        false_positives = np.sum((y == 0) & (y_pred_threshold == 1))
        actual_positives = np.sum(y == 1)
        actual_negatives = np.sum(y == 0)

        tpr.append(true_positives / actual_positives if actual_positives != 0 else 0)
        fpr.append(false_positives / actual_negatives if actual_negatives != 0 else 0)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label="Logistic Regression")
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.show()

plot_roc_curve(X, y, weights)
