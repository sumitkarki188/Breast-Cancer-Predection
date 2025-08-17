// Safe JSON response parser
async function safeJsonResponse(response) {
  const text = await response.text();
  if (!text) {
    throw new Error('Server returned empty response');
  }
  try {
    return JSON.parse(text);
  } catch (err) {
    throw new Error(`Invalid JSON response: ${text.substring(0, 100)}...`);
  }
}

// Tab functionality
function openTab(evt, tabName) {
  console.log('Tab clicked:', tabName);
  
  const tabContents = document.getElementsByClassName("tab-content");
  const tabBtns = document.getElementsByClassName("tab-btn");
  
  // Hide all tab contents
  for (let i = 0; i < tabContents.length; i++) {
    tabContents[i].classList.remove("active");
  }
  
  // Remove active class from all tab buttons
  for (let i = 0; i < tabBtns.length; i++) {
    tabBtns[i].classList.remove("active");
  }
  
  // Show the selected tab content and mark button as active
  const targetTab = document.getElementById(tabName);
  if (targetTab) {
    targetTab.classList.add("active");
    evt.currentTarget.classList.add("active");
    console.log('✅ Tab switched to:', tabName);
  } else {
    console.error('❌ Tab not found:', tabName);
  }
}

// Sample data for testing
function loadSampleData() {
  console.log('Loading sample data...');
  
  const sampleData = {
    radius_mean: 14.127,
    texture_mean: 19.26,
    perimeter_mean: 91.97,
    area_mean: 654.9,
    smoothness_mean: 0.096,
    compactness_mean: 0.104,
    concavity_mean: 0.089,
    concave_points_mean: 0.049,
    symmetry_mean: 0.181,
    fractal_dimension_mean: 0.0628,
    radius_se: 0.405,
    texture_se: 1.217,
    perimeter_se: 2.868,
    area_se: 40.34,
    smoothness_se: 0.007,
    compactness_se: 0.025,
    concavity_se: 0.032,
    concave_points_se: 0.012,
    symmetry_se: 0.020,
    fractal_dimension_se: 0.003,
    radius_worst: 16.27,
    texture_worst: 26.22,
    perimeter_worst: 108.9,
    area_worst: 858.1,
    smoothness_worst: 0.133,
    compactness_worst: 0.253,
    concavity_worst: 0.251,
    concave_points_worst: 0.132,
    symmetry_worst: 0.29,
    fractal_dimension_worst: 0.08
  };
  
  // Fill the form with sample data
  Object.keys(sampleData).forEach(key => {
    const input = document.querySelector(`input[name="${key}"]`);
    if (input) {
      input.value = sampleData[key];
    }
  });
  
  console.log('✅ Sample data loaded');
}

// Manual form submission - USES TRAINED MODEL
document.addEventListener('DOMContentLoaded', function() {
  const cancerForm = document.getElementById('cancerForm');
  if (cancerForm) {
    cancerForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      console.log('🔄 Starting manual prediction with trained model...');
      
      const resultDiv = document.getElementById('manualResult');
      resultDiv.innerHTML = '<div class="loading"></div>🤖 Analyzing with trained ML model...';
      
      const formData = new FormData(this);
      const data = Object.fromEntries(formData.entries());
      
      console.log('📊 Sending data:', Object.keys(data).length, 'features');
      
      try {
        const response = await fetch('/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });
        
        if (!response.ok) {
          const errorText = await response.text();
          console.error('❌ Server error:', errorText);
          resultDiv.innerHTML = `<div class="error">❌ Server Error (${response.status}): ${errorText || response.statusText}</div>`;
          return;
        }
        
        const result = await safeJsonResponse(response);
        console.log('✅ Prediction result:', result);
        displayResult(result, resultDiv);
        
      } catch (error) {
        console.error('❌ Prediction error:', error);
        resultDiv.innerHTML = `<div class="error">❌ Connection error: ${error.message}</div>`;
      }
    });
  }
  
  // CSV form submission - USES TRAINED MODEL
  const csvForm = document.getElementById('csvForm');
  if (csvForm) {
    csvForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      console.log('🔄 Starting CSV prediction with trained model...');
      
      const resultDiv = document.getElementById('csvResult');
      resultDiv.innerHTML = '<div class="loading"></div>🤖 Processing CSV with trained ML model...';
      
      const formData = new FormData(this);
      const file = formData.get('file');
      
      if (!file) {
        resultDiv.innerHTML = '<div class="error">❌ No file selected</div>';
        return;
      }
      
      console.log('📁 Uploading file:', file.name, 'Size:', file.size, 'bytes');
      
      try {
        const response = await fetch('/predict_csv', {
          method: 'POST',
          body: formData
        });
        
        console.log('📡 Response status:', response.status);
        
        if (!response.ok) {
          const errorText = await response.text();
          console.error('❌ Server error:', errorText);
          resultDiv.innerHTML = `<div class="error">❌ Server Error (${response.status}): ${errorText || response.statusText}</div>`;
          return;
        }
        
        const result = await safeJsonResponse(response);
        console.log('✅ CSV prediction results:', result.total_samples, 'predictions');
        
        if (result.predictions && Array.isArray(result.predictions)) {
          displayCSVResults(result, resultDiv);
        } else {
          resultDiv.innerHTML = `<div class="error">❌ Unexpected response format</div>`;
        }
        
      } catch (error) {
        console.error('❌ CSV prediction error:', error);
        resultDiv.innerHTML = `<div class="error">❌ Connection error: ${error.message}</div>`;
      }
    });
  }
});

// Display single prediction result
function displayResult(result, container) {
  const prediction = result.prediction;
  const confidence = result.confidence || 0.85;
  
  const className = prediction.toLowerCase() === 'malignant' ? 'malignant' : 'benign';
  const emoji = className === 'malignant' ? '⚠️' : '✅';
  const message = className === 'malignant' ? 
    'Please consult with a healthcare professional immediately' : 
    'The tumor appears to be non-cancerous';
  
  container.innerHTML = `
    <div class="result ${className}">
      <h3>${emoji} ML Model Prediction</h3>
      <p><strong>${prediction.toUpperCase()}</strong></p>
      <p>Confidence: ${(confidence * 100).toFixed(1)}%</p>
      <small>🤖 ${message}</small>
    </div>
  `;
}

// Display CSV prediction results
// Enhanced CSV results display function
function displayCSVResults(result, container) {
  const results = result.predictions;
  
  let html = '<div class="csv-results">';
  html += `<h3>🤖 Trained ML Model Results</h3>`;
  html += `<p>Processed ${results.length} samples using your trained model.pkl</p>`;
  
  // Show column info if available
  if (result.original_columns && result.columns_used) {
    html += `<div class="column-info">
      <small>📋 Original CSV had ${result.original_columns} columns, used ${result.columns_used.length} required columns for prediction</small>
    </div>`;
  }
  
  html += '<table><thead><tr><th>Sample #</th><th>Prediction</th><th>Confidence</th></tr></thead><tbody>';
  
  results.forEach((pred, index) => {
    const className = pred.prediction.toLowerCase() === 'malignant' ? 'malignant' : 'benign';
    const confidence = pred.confidence ? (pred.confidence * 100).toFixed(1) + '%' : 'N/A';
    
    html += `
      <tr>
        <td>${index + 1}</td>
        <td class="${className}"><strong>${pred.prediction}</strong></td>
        <td>${confidence}</td>
      </tr>
    `;
  });
  
  html += '</tbody></table>';
  
  // Add summary statistics
  const benignCount = result.benign_count || results.filter(r => r.prediction.toLowerCase() === 'benign').length;
  const malignantCount = result.malignant_count || results.filter(r => r.prediction.toLowerCase() === 'malignant').length;
  
  html += `
    <div class="summary">
      <h4>📊 ML Model Summary</h4>
      <p>✅ Benign: ${benignCount} samples (${((benignCount/results.length)*100).toFixed(1)}%)</p>
      <p>⚠️ Malignant: ${malignantCount} samples (${((malignantCount/results.length)*100).toFixed(1)}%)</p>
      <small>🤖 Predictions made using your trained model.pkl</small>
    </div>
  `;
  
  html += '</div>';
  container.innerHTML = html;
}


// File input enhancement
document.addEventListener('DOMContentLoaded', function() {
  // File input change handler
  const fileInput = document.getElementById('csvFile');
  if (fileInput) {
    fileInput.addEventListener('change', function(e) {
      const fileName = e.target.files[0]?.name;
      const fileNameSpan = document.getElementById('fileName');
      if (fileName && fileNameSpan) {
        fileNameSpan.textContent = `Selected: ${fileName}`;
      }
    });
  }
  
  // Drag and drop functionality
  const fileLabel = document.querySelector('.file-label');
  if (fileLabel) {
    fileLabel.addEventListener('dragover', function(e) {
      e.preventDefault();
      this.style.borderColor = '#667eea';
      this.style.background = '#edf2f7';
    });
    
    fileLabel.addEventListener('dragleave', function(e) {
      e.preventDefault();
      this.style.borderColor = '#cbd5e0';
      this.style.background = '#f7fafc';
    });
    
    fileLabel.addEventListener('drop', function(e) {
      e.preventDefault();
      this.style.borderColor = '#cbd5e0';
      this.style.background = '#f7fafc';
      
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        fileInput.files = files;
        const fileNameSpan = document.getElementById('fileName');
        if (fileNameSpan) {
          fileNameSpan.textContent = `Selected: ${files[0].name}`;
        }
      }
    });
  }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 Breast Cancer Prediction System Initialized');
  console.log('🤖 Using trained model.pkl for all predictions');
  
  // Test tab functionality
  const manualTab = document.getElementById('manual');
  const csvTab = document.getElementById('csv');
  console.log('Manual tab found:', !!manualTab);
  console.log('CSV tab found:', !!csvTab);
  
  // Check model status
  fetch('/health')
    .then(response => response.json())
    .then(status => {
      if (status.model_loaded) {
        console.log('✅ Trained ML Model is loaded and ready');
      } else {
        console.warn('⚠️ ML Model may not be loaded properly');
      }
    })
    .catch(error => console.error('❌ Health check failed:', error));
});
