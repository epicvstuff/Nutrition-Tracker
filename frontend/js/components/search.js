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

    this.searchStatus.textContent = 'Searching...';
    this.searchResultsList.innerHTML = '';

    try {
      const results = await FoodApi.searchFood(searchTerm);
      this.displayResults(results);
    } catch (error) {
      this.handleError(error);
    }
  }

  displayResults(results) {
    this.searchResultsList.innerHTML = '';
    this.searchStatus.textContent = '';

    if (results.length === 0) {
      this.searchResultsList.innerHTML = '<li class="no-results">No results found. Try different keywords or enter manually below.</li>';
      return;
    }

    results.forEach(result => {
      const li = document.createElement('li');
      li.textContent = result.name;
      li.dataset.nutrients = JSON.stringify(result.nutrients);
      li.addEventListener('click', () => this.handleResultSelection(result));
      this.searchResultsList.appendChild(li);
    });
  }

  handleResultSelection(result) {
    this.onFoodSelect(result);
    this.searchResultsList.innerHTML = '';
    this.searchInput.value = '';
    this.searchStatus.textContent = `Selected: ${result.name}. Enter quantity (g) below.`;
  }

  handleError(error) {
    console.error('Search error:', error);
    this.searchStatus.textContent = 'Error fetching data. Check console or enter manually.';
    this.searchResultsList.innerHTML = '<li class="no-results">Search failed.</li>';
  }
}

export default SearchComponent; 