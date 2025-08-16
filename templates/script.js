// Tab functionality
function openTab(evt, tabName) {
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
  document.getElementById(tabName).classList.add("active");
  evt.currentTarget.classList.add("active");
}

// Sample data for testing
function loadSampleData() {
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
}

// Manual form submission
document.getElementById('cancerForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const resultDiv = document.getElementById('manualResult');
  resultDiv.innerHTML = '<div class="loading"></div>Analyzing data...';
  
  const formData = new FormData(this);
  const data = Object.fromEntries(formData.entries());
  
  try {
    // Simulate API call - replace with your actual endpoint
    const response = await fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });
    
    if (response.ok) {
      const result = await response.json();
      displayResult(result, resultDiv);
    } else {
      throw new Error('Prediction failed');
    }
  } catch (error) {
    // Simulate a prediction for demo purposes
    simulatePrediction(data, resultDiv);
  }
});

// CSV form submission
document.getElementById('csvForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const resultDiv = document.getElementById('csvResult');
  resultDiv.innerHTML = '<div class="loading"></div>Processing CSV file...';
  
  const formData = new FormData(this);
  
  try {
    // Simulate API call - replace with your actual endpoint
    const response = await fetch('/predict_csv', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      const result = await response.json();
      displayCSVResults(result, resultDiv);
    } else {
      throw new Error('CSV prediction failed');
    }
  } catch (error) {
    // Simulate CSV processing for demo purposes
    simulateCSVPrediction(resultDiv);
  }
});

// Display single prediction result
function displayResult(result, container) {
  const prediction = result.prediction || result;
  const confidence = result.confidence || Math.random() * 0.3 + 0.7; // Simulate confidence
  
  const className = prediction.toLowerCase() === 'malignant' ? 'malignant' : 'benign';
  const emoji = className === 'malignant' ? '⚠️' : '✅';
  
  container.innerHTML = `
    <div class="result ${className}">
      ${emoji} Prediction: <strong>${prediction.toUpperCase()}</strong>
      <br>
      <small>Confidence: ${(confidence * 100).toFixed(1)}%</small>
    </div>
  `;
}

// Display CSV prediction results
function displayCSVResults(results, container) {
  let html = '<div class="csv-results">';
  html += '<h3>Prediction Results</h3>';
  html += '<table><thead><tr><th>Row</th><th>Prediction</th><th>Confidence</th></tr></thead><tbody>';
  
  results.forEach((result, index) => {
    const className = result.prediction.toLowerCase() === 'malignant' ? 'malignant' : 'benign';
    html += `
      <tr>
        <td>${index + 1}</td>
        <td class="${className}">${result.prediction}</td>
        <td>${(result.confidence * 100).toFixed(1)}%</td>
      </tr>
    `;
  });
  
  html += '</tbody></table></div>';
  container.innerHTML = html;
}

// Simulate prediction for demo purposes
function simulatePrediction(data, container) {
  setTimeout(() => {
    // Simple simulation based on some features
    const radiusMean = parseFloat(data.radius_mean);
    const areaMean = parseFloat(data.area_mean);
    const concavityMean = parseFloat(data.concavity_mean);
    
    // Very basic simulation logic
    const score = (radiusMean > 15 ? 1 : 0) + 
                  (areaMean > 800 ? 1 : 0) + 
                  (concavityMean > 0.1 ? 1 : 0);
    
    const prediction = score >= 2 ? 'Malignant' : 'Benign';
    const confidence = Math.random() * 0.2 + 0.75; // 75-95% confidence
    
    displayResult({ prediction, confidence }, container);
  }, 1500);
}

// Simulate CSV prediction for demo purposes
function simulateCSVPrediction(container) {
  setTimeout(() => {
    const mockResults = [
      { prediction: 'Benign', confidence: 0.89 },
      { prediction: 'Malignant', confidence: 0.76 },
      { prediction: 'Benign', confidence: 0.92 },
      { prediction: 'Benign', confidence: 0.84 },
      { prediction: 'Malignant', confidence: 0.78 }
    ];
    
    displayCSVResults(mockResults, container);
  }, 2000);
}

// File input enhancement
document.getElementById('fileInput').addEventListener('change', function(e) {
  const fileName = e.target.files[0]?.name;
  if (fileName) {
    const label = document.querySelector('.file-label span');
    label.textContent = `Selected: ${fileName}`;
  }
});

// Drag and drop functionality
const fileLabel = document.querySelector('.file-label');

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
    document.getElementById('fileInput').files = files;
    const label = document.querySelector('.file-label span');
    label.textContent = `Selected: ${files[0].name}`;
  }
});
