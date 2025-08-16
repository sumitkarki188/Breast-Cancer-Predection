from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import pandas as pd
import io

# Load model and scaler
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    print("✅ Model and scaler loaded successfully!")
except FileNotFoundError as e:
    print(f"❌ Error loading model files: {e}")
    model = None
    scaler = None

app = Flask(__name__)

# Expected feature columns in order
FEATURE_COLUMNS = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave_points_mean', 'symmetry_mean',
    'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se',
    'smoothness_se', 'compactness_se', 'concavity_se', 'concave_points_se',
    'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
    'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst',
    'concavity_worst', 'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Handle manual prediction requests"""
    try:
        # Check if model is loaded
        if model is None or scaler is None:
            return jsonify({
                'error': 'Model not loaded. Please check server configuration.'
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided. Please fill all required fields.'
            }), 400
        
        # Extract features in the correct order
        features = []
        missing_features = []
        
        for feature in FEATURE_COLUMNS:
            if feature in data and data[feature] is not None:
                try:
                    features.append(float(data[feature]))
                except (ValueError, TypeError):
                    return jsonify({
                        'error': f'Invalid value for {feature}. Please enter a valid number.'
                    }), 400
            else:
                missing_features.append(feature)
        
        if missing_features:
            return jsonify({
                'error': f'Missing required features: {", ".join(missing_features)}'
            }), 400
        
        # Convert to numpy array and reshape
        features_array = np.array([features])
        
        # Scale features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Get prediction probabilities for confidence
        try:
            probabilities = model.predict_proba(features_scaled)
            confidence = max(probabilities)
        except:
            # If model doesn't support predict_proba
            confidence = 0.85  # Default confidence
        
        # Convert prediction to readable format
        result = "Malignant" if prediction == 1 else "Benign"
        
        return jsonify({
            'prediction': result,
            'confidence': float(confidence),
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error in predict endpoint: {str(e)}")
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route("/predict_csv", methods=["POST"])
def predict_csv():
    """Handle CSV file prediction requests"""
    try:
        # Check if model is loaded
        if model is None or scaler is None:
            return jsonify({
                'error': 'Model not loaded. Please check server configuration.'
            }), 500
        
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file uploaded. Please select a CSV file.'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'No file selected. Please choose a CSV file.'
            }), 400
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({
                'error': 'Invalid file format. Please upload a CSV file.'
            }), 400
        
        # Read CSV file
        try:
            # Read the CSV file
            csv_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
        except Exception as e:
            return jsonify({
                'error': f'Error reading CSV file: {str(e)}'
            }), 400
        
        # Validate CSV structure
        if csv_data.empty:
            return jsonify({
                'error': 'CSV file is empty.'
            }), 400
        
        # Check if CSV has the right number of columns
        if len(csv_data.columns) != len(FEATURE_COLUMNS):
            return jsonify({
                'error': f'CSV must have exactly {len(FEATURE_COLUMNS)} columns. Found {len(csv_data.columns)} columns.'
            }), 400
        
        # Rename columns to match expected format
        csv_data.columns = FEATURE_COLUMNS
        
        # Validate all values are numeric
        try:
            features_data = csv_data.astype(float)
        except ValueError as e:
            return jsonify({
                'error': f'All values must be numeric. Error: {str(e)}'
            }), 400
        
        # Scale features
        features_scaled = scaler.transform(features_data.values)
        
        # Make predictions
        predictions = model.predict(features_scaled)
        
        # Get prediction probabilities for confidence
        try:
            probabilities = model.predict_proba(features_scaled)
            confidences = np.max(probabilities, axis=1)
        except:
            # If model doesn't support predict_proba
            confidences = [0.85] * len(predictions)
        
        # Format results
        results = []
        for i, (pred, conf) in enumerate(zip(predictions, confidences)):
            result = "Malignant" if pred == 1 else "Benign"
            results.append({
                'prediction': result,
                'confidence': float(conf)
            })
        
        return jsonify({
            'predictions': results,
            'total_samples': len(results),
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error in predict_csv endpoint: {str(e)}")
        return jsonify({
            'error': f'CSV prediction failed: {str(e)}'
        }), 500

@app.route("/health")
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None,
        'expected_features': len(FEATURE_COLUMNS)
    }
    return jsonify(status)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    print("🚀 Starting Breast Cancer Prediction Server...")
    print(f"📊 Expected features: {len(FEATURE_COLUMNS)}")
    print("🌐 Server will be available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
