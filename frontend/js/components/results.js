class ResultsComponent {
  constructor() {
    this.resultsContainer = document.getElementById('results-container');
    this.bindEvents();
  }

  bindEvents() {
    // Add any event listeners if needed
  }

  displayResults(result) {
    if (!result || !result.classification) {
      this.showError('No classification results available.');
      return;
    }

    const { classification, confidence, nutritional_info } = result;
    
    const resultsHTML = `
      <div class="results-card">
        <h3>Classification Results</h3>
        <div class="result-item">
          <span class="label">Food Item:</span>
          <span class="value">${classification}</span>
        </div>
        <div class="result-item">
          <span class="label">Confidence:</span>
          <span class="value">${(confidence * 100).toFixed(1)}%</span>
        </div>
        ${this.renderNutritionalInfo(nutritional_info)}
      </div>
    `;

    this.resultsContainer.innerHTML = resultsHTML;
    this.resultsContainer.style.display = 'block';
  }

  renderNutritionalInfo(nutritionalInfo) {
    if (!nutritionalInfo) {
      return '<div class="result-item error">Nutritional information not available</div>';
    }

    return `
      <div class="nutritional-info">
        <h4>Nutritional Information</h4>
        <div class="result-item">
          <span class="label">Calories:</span>
          <span class="value">${nutritionalInfo.calories || 'N/A'} kcal</span>
        </div>
        <div class="result-item">
          <span class="label">Protein:</span>
          <span class="value">${nutritionalInfo.protein || 'N/A'} g</span>
        </div>
        <div class="result-item">
          <span class="label">Carbohydrates:</span>
          <span class="value">${nutritionalInfo.carbohydrates || 'N/A'} g</span>
        </div>
        <div class="result-item">
          <span class="label">Fat:</span>
          <span class="value">${nutritionalInfo.fat || 'N/A'} g</span>
        </div>
      </div>
    `;
  }

  showError(message) {
    this.resultsContainer.innerHTML = `
      <div class="results-error">
        <p>${message}</p>
      </div>
    `;
    this.resultsContainer.style.display = 'block';
  }

  clear() {
    this.resultsContainer.innerHTML = '';
    this.resultsContainer.style.display = 'none';
  }
}

export default ResultsComponent; 