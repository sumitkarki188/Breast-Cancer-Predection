🩺 Breast Cancer Prediction using Machine Learning
[![Python](https://img.shields.io/img.g.shields. project for predicting breast cancer using three different algorithms: Logistic Regression, Decision Tree, and Random Forest.

📋 Table of Contents
🎯 Overview

📊 Dataset

🛠️ Methodology

🤖 Machine Learning Models

📈 Results

🚀 Installation

💻 Usage

📊 Performance Metrics

🔮 Future Work

🤝 Contributing

📝 License

👨💻 Author

🎯 Overview
Breast cancer occurs when cells in the breast tissue grow uncontrollably and form tumors. Early detection and accurate prediction are crucial for effective treatment. This project implements three machine learning algorithms to predict whether a person has breast cancer or not, providing high accuracy results to assist in medical diagnosis.

✨ Key Features
🔬 Three ML algorithms implemented for comprehensive comparison

🎯 High accuracy rates - up to 97.3% with Random Forest

🧹 Comprehensive data preprocessing and cleaning pipeline

📊 Detailed performance evaluation using multiple metrics

📊 Dataset
Metric	Value
Total Samples	569 medical data values
Benign Cases	357 data values (62.7%)
Malignant Cases	212 data values (37.3%)
Training Split	80% (455 samples)
Testing Split	20% (114 samples)
The dataset contains various features extracted from breast cancer diagnostic images, including measurements from mammography and other medical imaging techniques.

🛠️ Methodology
1. 📥 Data Collection
Collection of medical data values comprising both benign and malignant breast cancer cases.

2. 🧹 Data Preprocessing and Cleaning
❌ Removal of null values from the dataset

🗑️ Elimination of irrelevant columns

📈 Statistical analysis (mean, standard deviation, minimum, maximum values)

⚖️ Data normalization and feature scaling

3. 🎓 Model Training and Testing
📊 Data split: 80% training, 20% testing

✅ Cross-validation techniques applied

⚙️ Hyperparameter tuning for optimal performance

4. 📋 Model Evaluation
Comprehensive evaluation using multiple metrics:

Accuracy - Overall correctness

Precision - True positive rate

Recall - Sensitivity measure

F1-Score - Harmonic mean of precision and recall

🤖 Machine Learning Models
<details> <summary><strong>🌳 Decision Tree</strong></summary>
Structure: Tree-like model starting with root nodes

Process: Splits data into similar subsets based on conditions

Output: Reaches final leaf nodes for classification

Advantage: Interpretable and easy to understand

</details> <details> <summary><strong>🌲 Random Forest</strong></summary>
Structure: Ensemble method combining multiple decision trees

Process: Uses majority voting for final prediction

Output: More accurate and robust results

Advantage: Reduces overfitting and improves generalization

</details> <details> <summary><strong>📊 Logistic Regression</strong></summary>
Function: Uses sigmoid function for probabilistic output

Output: Probability values between 0 and 1

Prediction: Binary classification ("yes" or "no")

Advantage: Provides probability estimates

</details>
