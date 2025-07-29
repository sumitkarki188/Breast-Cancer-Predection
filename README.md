🧠 Breast Cancer Prediction Using Machine Learning
A machine learning-based approach to predict breast cancer using Logistic Regression, Decision Tree, and Random Forest classifiers.

📌 Project Overview
Breast cancer is one of the leading causes of death among women worldwide. This project aims to build predictive models that can assist in early detection of breast cancer using structured medical data. By leveraging supervised learning algorithms, the models predict whether a tumor is benign or malignant based on diagnostic attributes.

📂 Contents
Introduction

Dataset and Preprocessing

Machine Learning Models

Results and Evaluation

Conclusion and Future Work

🗂️ Dataset
Total Samples: 569

Benign: 357

Malignant: 212

Features: Medical diagnostic measurements from digitized images of breast mass.

Source: Included in the code repository or loaded from sklearn.datasets.

⚙️ Models Used
Logistic Regression

Decision Tree

Random Forest

Each model was trained using 80% of the data and tested on 20%.

🧪 Evaluation Metrics
Metric	Logistic Regression	Decision Tree	Random Forest
Accuracy	96.49%	93.86%	97.36%
Precision (Class 1)	98%	93%	100%
Recall (Class 1)	94%	91%	94%
F1 Score (Class 1)	96%	92%	97%
Support (Class 1)	47	47	47

📌 Random Forest achieved the highest accuracy and F1 score among all.

📈 Flow Diagram
nginx
Copy
Edit
Collecting Data → Preprocessing → Model Training → Evaluation → Results
📌 Key Findings
Random Forest outperforms the other models with an accuracy of 97.36%, precision of 100%, and F1-score of 97%.

Logistic Regression is simple and effective, offering near-comparable performance.

Decision Tree has slightly lower recall, indicating some false negatives.

🔮 Conclusion & Future Work
This project demonstrates that machine learning algorithms, especially Random Forest, are effective in predicting breast cancer. These models can aid healthcare professionals in diagnosis and treatment planning.

🔬 Future Enhancements
Integrate deep learning and ensemble methods for more advanced prediction.

Explore radiomics and AI-enhanced imaging (e.g., mammograms, MRIs).

Implement IoT-based real-time monitoring systems.

Develop public awareness programs leveraging this tech.

