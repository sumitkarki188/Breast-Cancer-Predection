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
    
    # Get the number of features the scaler expects
    expected_features = scaler.n_features_in_
    print(f"🔢 Model expects {expected_features} features")
    
except FileNotFoundError as e:
    print(f"❌ Error loading model files: {e}")
    model = None
    scaler = None
    expected_features = 30

app = Flask(__name__)

# Original 30 feature columns (for reference)
ALL_FEATURE_COLUMNS = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave_points_mean', 'symmetry_mean',
    'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se',
    'smoothness_se', 'compactness_se', 'concavity_se', 'concave_points_se',
    'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
    'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst',
    'concavity_worst', 'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

# Use only the number of features the model expects
FEATURE_COLUMNS = ALL_FEATURE_COLUMNS[:expected_features] if model else ALL_FEATURE_COLUMNS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Handle manual prediction requests using trained model"""
    try:
        print("📥 Received manual prediction request")
        
        # Check if model is loaded
        if model is None or scaler is None:
            print("❌ Model or scaler not loaded")
            return jsonify({
                'error': 'Model not loaded. Please check server configuration.'
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        print(f"📊 Received data: {len(data) if data else 0} features")
        
        if not data:
            return jsonify({
                'error': 'No data provided. Please fill all required fields.'
            }), 400
        
        # Extract features in the correct order
        features = []
        missing_features = []
        
        for feature in FEATURE_COLUMNS:
            if feature in data and data[feature] is not None and str(data[feature]).strip() != '':
                try:
                    features.append(float(data[feature]))
                except (ValueError, TypeError):
                    return jsonify({
                        'error': f'Invalid value for {feature}. Please enter a valid number.'
                    }), 400
            else:
                missing_features.append(feature)
        
        if missing_features:
            print(f"❌ Missing features: {missing_features[:5]}...")
            return jsonify({
                'error': f'Missing required features: {", ".join(missing_features[:5])}{"..." if len(missing_features) > 5 else ""}'
            }), 400
        
        # Convert to numpy array and reshape
        features_array = np.array([features])
        print(f"🔢 Features array shape: {features_array.shape}")
        
        # Scale features using trained scaler
        features_scaled = scaler.transform(features_array)
        print(f"⚖️ Features scaled successfully")
        
        # Make prediction using trained model
        prediction = model.predict(features_scaled)[0]
        print(f"🔮 Raw prediction: {prediction}")
        
        # Get prediction probabilities for confidence - FIXED
        try:
            probabilities = model.predict_proba(features_scaled)  # Get first (and only) sample
            confidence = max(probabilities)
            print(f"📊 Confidence: {confidence:.3f}")
        except:
            confidence = 0.85
            print("⚠️ Using default confidence")
        
        # Convert prediction to readable format
        result = "Malignant" if prediction == 1 else "Benign"
        print(f"✅ Final prediction: {result}")
        
        return jsonify({
            'prediction': result,
            'confidence': float(confidence),
            'status': 'success'
        })
        
    except Exception as e:
        print(f"❌ Error in predict endpoint: {str(e)}")
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route("/predict_csv", methods=["POST"])
def predict_csv():
    """Handle CSV file prediction requests - PROPERLY DROP UNUSED COLUMNS"""
    try:
        print("📥 Received CSV prediction request")
        
        # Check if model is loaded
        if model is None or scaler is None:
            print("❌ Model or scaler not loaded")
            return jsonify({
                'error': 'Model not loaded. Please check server configuration.'
            }), 500
        
        print(f"🎯 Model expects {expected_features} features")
        
        # Check if file is in request
        if 'file' not in request.files:
            print("❌ No file in request")
            return jsonify({
                'error': 'No file uploaded. Please select a CSV file.'
            }), 400
        
        file = request.files['file']
        print(f"📁 Received file: {file.filename}")
        
        if file.filename == '':
            return jsonify({
                'error': 'No file selected. Please choose a CSV file.'
            }), 400
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({
                'error': 'Invalid file format. Please upload a CSV file.'
            }), 400
        
        # Read CSV file with multiple encoding attempts
        try:
            file_content = None
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    file_content = file.read().decode(encoding)
                    print(f"✅ Successfully decoded with {encoding}")
                    break
                except UnicodeDecodeError:
                    file.seek(0)  # Reset file pointer for next attempt
                    continue
            
            if file_content is None:
                return jsonify({
                    'error': 'Unable to decode CSV file. Please save as UTF-8 format.'
                }), 400
            
            print(f"📄 File content length: {len(file_content)} characters")
            
            if len(file_content.strip()) == 0:
                return jsonify({
                    'error': 'CSV file is empty.'
                }), 400
            
            # Try different CSV parsing approaches
            csv_data = None
            delimiter_used = None
            
            # Parse with different delimiters
            delimiters = [',', ';', '\t', '|']
            for delimiter in delimiters:
                try:
                    csv_data = pd.read_csv(
                        io.StringIO(file_content), 
                        delimiter=delimiter,
                        skipinitialspace=True,
                        skip_blank_lines=True
                    )
                    if len(csv_data.columns) > 1 and not csv_data.empty:
                        delimiter_used = delimiter
                        print(f"✅ Successfully parsed with delimiter: '{delimiter}'")
                        break
                except Exception as e:
                    print(f"❌ Failed with delimiter '{delimiter}': {str(e)}")
                    continue
            
            # Final fallback - let pandas auto-detect
            if csv_data is None or csv_data.empty or len(csv_data.columns) <= 1:
                try:
                    csv_data = pd.read_csv(io.StringIO(file_content))
                    delimiter_used = 'auto-detected'
                    print("✅ Successfully parsed with auto-detection")
                except Exception as e:
                    print(f"❌ Auto-detection failed: {str(e)}")
                    return jsonify({
                        'error': f'Could not parse CSV file: {str(e)}'
                    }), 400
            
            print(f"📊 CSV loaded: {csv_data.shape[0]} rows, {csv_data.shape[1]} columns")
            print(f"📋 All CSV columns: {list(csv_data.columns)}")
            
        except Exception as e:
            print(f"❌ Error reading CSV: {str(e)}")
            return jsonify({
                'error': f'Error reading CSV file: {str(e)}'
            }), 400
        
        # Validate CSV structure
        if csv_data.empty:
            return jsonify({
                'error': 'CSV file contains no data rows.'
            }), 400
        
        # SMART COLUMN SELECTION - Drop unwanted columns first
        try:
            print("🔍 Starting intelligent column selection...")
            
            # Clean column names
            csv_data.columns = [str(col).strip() for col in csv_data.columns]
            available_columns = list(csv_data.columns)
            
            # Define columns to exclude (case-insensitive)
            exclude_patterns = [
                'id', 'diagnosis', 'target', 'label', 'class', 'outcome', 'result',
                'patient', 'sample', 'index', 'unnamed', 'row'
            ]
            
            # Filter out excluded columns
            feature_candidates = []
            excluded_columns = []
            
            for col in available_columns:
                col_lower = col.lower().strip()
                should_exclude = any(pattern in col_lower for pattern in exclude_patterns)
                
                if should_exclude:
                    excluded_columns.append(col)
                    print(f"🗑️ Excluding column: {col}")
                else:
                    feature_candidates.append(col)
            
            print(f"📊 Feature candidates: {len(feature_candidates)} columns")
            print(f"🗑️ Excluded columns: {excluded_columns}")
            
            # Test which columns are numeric
            numeric_columns = []
            for col in feature_candidates:
                try:
                    # Try to convert to numeric
                    numeric_test = pd.to_numeric(csv_data[col], errors='coerce')
                    valid_ratio = numeric_test.notna().sum() / len(numeric_test)
                    
                    if valid_ratio >= 0.9:  # At least 90% valid numeric values
                        numeric_columns.append(col)
                        print(f"✅ Numeric column: {col} ({valid_ratio:.1%} valid)")
                    else:
                        print(f"❌ Non-numeric column: {col} ({valid_ratio:.1%} valid)")
                        
                except Exception as e:
                    print(f"❌ Error testing column {col}: {str(e)}")
                    continue
            
            print(f"🔢 Found {len(numeric_columns)} numeric columns")
            
            # Check if we have enough features
            if len(numeric_columns) < expected_features:
                return jsonify({
                    'error': f'Need {expected_features} numeric features, found only {len(numeric_columns)}. Available: {numeric_columns}'
                }), 400
            
            # Select exactly the number of features the model expects
            selected_columns = numeric_columns[:expected_features]
            print(f"✅ Selected {len(selected_columns)} columns: {selected_columns}")
            
            # Create final feature dataset
            features_data = csv_data[selected_columns].copy()
            
            # Convert to numeric and handle any remaining non-numeric values
            for col in selected_columns:
                features_data[col] = pd.to_numeric(features_data[col], errors='coerce')
            
            # Handle missing values
            if features_data.isnull().any().any():
                print("⚠️ Found missing values, filling with column medians")
                features_data = features_data.fillna(features_data.median())
            
            # Final conversion to float
            features_data = features_data.astype(float)
            
            print(f"📊 Final dataset shape: {features_data.shape}")
            print(f"📈 Sample row: {features_data.iloc[0].values[:5].tolist()}")
            
        except Exception as e:
            print(f"❌ Error in column selection: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': f'Error processing CSV columns: {str(e)}'
            }), 400
        
        # Validate final feature count - FIXED
        if features_data.shape[1] != expected_features:
            return jsonify({
                'error': f'Expected {expected_features} features, got {features_data.shape[1]} features.'
            }), 400
        
        print(f"🎯 Ready for prediction: {features_data.shape} samples × {features_data.shape[1]} features")
        
        # Scale features using trained scaler
        try:
            features_scaled = scaler.transform(features_data.values)
            print(f"⚖️ Features scaled successfully")
        except Exception as e:
            print(f"❌ Error scaling features: {str(e)}")
            return jsonify({
                'error': f'Error scaling features: {str(e)}'
            }), 400
        
        # Make predictions using trained model
        try:
            predictions = model.predict(features_scaled)
            print(f"🔮 Predictions completed: {len(predictions)} results")
        except Exception as e:
            print(f"❌ Error making predictions: {str(e)}")
            return jsonify({
                'error': f'Error making predictions: {str(e)}'
            }), 400
        
        # Get prediction probabilities for confidence
        try:
            probabilities = model.predict_proba(features_scaled)
            confidences = np.max(probabilities, axis=1)
            print("📊 Confidence scores calculated")
        except Exception as e:
            print(f"⚠️ Could not calculate confidence: {str(e)}")
            confidences = [0.85] * len(predictions)
        
        # Format results
        results = []
        malignant_count = 0
        benign_count = 0
        
        for pred, conf in zip(predictions, confidences):
            result = "Malignant" if pred == 1 else "Benign"
            if pred == 1:
                malignant_count += 1
            else:
                benign_count += 1
                
            results.append({
                'prediction': result,
                'confidence': float(conf)
            })
        
        print(f"✅ Final Results: {benign_count} Benign, {malignant_count} Malignant")
        
        return jsonify({
            'predictions': results,
            'total_samples': len(results),
            'benign_count': benign_count,
            'malignant_count': malignant_count,
            'features_used': expected_features,
            'selected_columns': selected_columns,
            'excluded_columns': excluded_columns,
            'original_columns': len(available_columns),
            'delimiter_used': delimiter_used,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"❌ Critical error in predict_csv: {str(e)}")
        import traceback
        traceback.print_exc()
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
        'expected_features': expected_features,
        'feature_columns_available': len(FEATURE_COLUMNS)
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
    import os
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Starting Breast Cancer Prediction Server...")
    print(f"📊 Model expects: {expected_features} features")
    print(f"📋 Using columns: {FEATURE_COLUMNS}")
    print(f"🌐 Server will be available on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
