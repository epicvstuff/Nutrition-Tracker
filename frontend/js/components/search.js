import FoodApi from '../api/foodApi.js';

class SearchComponent {
  constructor(onFoodSelect) {
    this.onFoodSelect = onFoodSelect;
    this.searchInput = document.getElementById('food-search');
    this.searchButton = document.getElementById('search-button');
    this.searchResultsList = document.getElementById('search-results');
    this.searchStatus = document.getElementById('search-status');
    
    this.bindEvents();
  }

  bindEvents() {
    this.searchButton.addEventListener('click', this.handleSearch.bind(this));
    this.searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.handleSearch(e);
      }
    });
  }

  async handleSearch(event) {
    event.preventDefault();
    const searchTerm = this.searchInput.value.trim();
    
    if (!searchTerm) {
      this.searchStatus.textContent = 'Please enter a food to search.';
      return;
    }

    this.searchStatus.textContent = 'Searching USDA database...';
    this.searchResultsList.innerHTML = '';

    try {
      const results = await FoodApi.searchFood(searchTerm);
      this.displayResults(results, searchTerm);
    } catch (error) {
      this.handleError(error);
    }
  }

  displayResults(results, searchTerm) {
    this.searchResultsList.innerHTML = '';
    
    if (results.length === 0) {
      this.searchStatus.textContent = 'No results found. Try different keywords or enter manually below.';
      this.searchResultsList.innerHTML = `
        <li class="no-results">
          <div class="no-results-message">
            <p>No foods found for "${searchTerm}"</p>
            <p>Try searching with different keywords or add the food manually using the form below.</p>
          </div>
        </li>
      `;
      return;
    }

    // Show status with data source information
    const hasUSDA = results.some(r => r.source === 'USDA FoodData Central');
    const hasOFF = results.some(r => r.source === 'OpenFoodFacts');
    
    let statusText = `Found ${results.length} results`;
    if (hasUSDA && hasOFF) {
      statusText += ' (USDA + OpenFoodFacts)';
    } else if (hasUSDA) {
      statusText += ' from USDA database';
    } else if (hasOFF) {
      statusText += ' from OpenFoodFacts';
    }
    this.searchStatus.textContent = statusText;

    results.forEach(result => {
      const li = document.createElement('li');
      li.className = `search-result ${result.source === 'USDA FoodData Central' ? 'usda-result' : 'off-result'}`;
      
      li.innerHTML = this.createResultHTML(result);
      li.addEventListener('click', () => this.handleResultSelection(result));
      this.searchResultsList.appendChild(li);
    });
  }

  createResultHTML(result) {
    const nutrients = result.nutrients;
    const sourceClass = result.source === 'USDA FoodData Central' ? 'usda' : 'off';
    const sourceIcon = result.source === 'USDA FoodData Central' ? '🏛️' : '🌍';
    
    return `
      <div class="result-header">
        <h4 class="result-name">${result.name}</h4>
        <span class="result-source ${sourceClass}">
          ${sourceIcon} ${result.source === 'USDA FoodData Central' ? 'USDA' : 'OpenFoodFacts'}
        </span>
      </div>
      
      <div class="result-details">
        ${result.dataType ? `<span class="data-type">${result.dataType}</span>` : ''}
        <span class="serving-size">Per ${result.servingSize || '100g'}</span>
      </div>
      
      <div class="nutrition-summary">
        <div class="nutrition-item">
          <span class="nutrient-value">${Math.round(nutrients.calories)}</span>
          <span class="nutrient-label">cal</span>
        </div>
        <div class="nutrition-item">
          <span class="nutrient-value">${nutrients.protein.toFixed(1)}</span>
          <span class="nutrient-label">protein</span>
        </div>
        <div class="nutrition-item">
          <span class="nutrient-value">${nutrients.carbs.toFixed(1)}</span>
          <span class="nutrient-label">carbs</span>
        </div>
        <div class="nutrition-item">
          <span class="nutrient-value">${nutrients.fat.toFixed(1)}</span>
          <span class="nutrient-label">fat</span>
        </div>
        ${nutrients.fiber > 0 ? `
          <div class="nutrition-item">
            <span class="nutrient-value">${nutrients.fiber.toFixed(1)}</span>
            <span class="nutrient-label">fiber</span>
          </div>
        ` : ''}
      </div>
      
      <div class="result-action">
        <span class="click-hint">Click to select this food</span>
      </div>
    `;
  }

  handleResultSelection(result) {
    // Convert to format expected by the food form
    const formattedResult = {
      name: result.name,
      nutrients: result.nutrients,
      source: result.source,
      servingSize: result.servingSize,
      dataType: result.dataType
    };
    
    this.onFoodSelect(formattedResult);
    this.searchResultsList.innerHTML = '';
    this.searchInput.value = '';
    this.searchStatus.textContent = `Selected: ${result.name}. Enter quantity (g) below.`;
  }

  handleError(error) {
    console.error('Search error:', error);
    this.searchStatus.textContent = 'Error searching database. Check console or enter manually.';
    this.searchResultsList.innerHTML = `
      <li class="search-error">
        <div class="error-message">
          <p>Search failed. Please try again or enter food manually below.</p>
          <small>Error: ${error.message}</small>
        </div>
      </li>
    `;
  }
}

export default SearchComponent; 