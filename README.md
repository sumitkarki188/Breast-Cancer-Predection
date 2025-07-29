Breast Cancer Prediction Using Machine Learning
A machine learning-based project to predict breast cancer using Logistic Regression, Decision Tree, and Random Forest classifiers.

📌 Project Overview
Breast cancer is one of the most common cancers affecting women worldwide. This project applies supervised machine learning models to predict whether a tumor is benign or malignant, using structured medical data. The aim is to assist in early diagnosis and improve treatment decisions.

📂 Table of Contents
Project Overview

Dataset and Preprocessing

Machine Learning Models

Results and Evaluation

Conclusion and Future Work

Author

License

🗂️ Dataset and Preprocessing
Total Samples: 569

Benign: 357

Malignant: 212

Source: Breast cancer dataset from sklearn or included with the repository.

Preprocessing Steps:

Removed null values

Dropped irrelevant columns

Performed basic statistical analysis

Split dataset into 80% training and 20% testing

⚙️ Machine Learning Models
Three classification models were implemented:

Logistic Regression

Decision Tree

Random Forest

The models were evaluated using accuracy, precision, recall, F1-score, and support.

📊 Results and Evaluation
Metric	Logistic Regression	Decision Tree	Random Forest
Accuracy	96.49%	93.86%	97.36%
Precision (Class 1)	98%	93%	100%
Recall (Class 1)	94%	91%	94%
F1 Score (Class 1)	96%	92%	97%
Support (Class 1)	47	47	47

✅ Random Forest achieved the best overall performance.

🧠 Conclusion & Future Work
This study shows that machine learning models — especially Random Forest — can effectively predict breast cancer from diagnostic data. These models have the potential to support healthcare professionals in early diagnosis and patient management.

🔮 Future Improvements
Explore deep learning and ensemble techniques

Leverage AI and radiomics for enhanced medical imaging

Build real-time monitoring using IoT devices

Raise public awareness on ML-based cancer detection
