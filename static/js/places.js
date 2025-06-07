// --- Asynchronous JavaScript function to make an API request ---
async function getPlaces(options = {}) {
    const { page = 1, per_page = 10, search = '', categories = [] } = options;

    const params = new URLSearchParams();
    params.append('page', page);
    params.append('per_page', per_page);

    if (search) {
        params.append('search', search);
    }

    if (categories.length > 0) {
        params.append('categories', categories.join(','));
    }

    const url = `/api/places?${params.toString()}`; // Use relative path

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorData.message || 'Unknown error'}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching places:", error);
        throw error;
    }
}

// --- DOM Elements ---
const searchInput = document.getElementById('search-input');
const filterCheckboxes = document.querySelectorAll(".filters input[type='checkbox']");
const placesResultsDiv = document.querySelector(".places-grid-container");
const loadingMessage = document.getElementById('loading-message');
const errorMessage = document.getElementById('error-message');
const searchButton = document.getElementById('search-button'); // New element: search button

let currentPage = 1;
let totalPages = 1;

// --- Function to perform search and display results ---
async function performSearch() {
    if (loadingMessage) loadingMessage.style.display = 'block';
    if (errorMessage) errorMessage.style.display = 'none';
    placesResultsDiv.innerHTML = '';

    const searchTerm = searchInput.value;
    const selectedCategories = Array.from(filterCheckboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);

    const itemsPerPage = 10;

    try {
        const result = await getPlaces({
            page: currentPage,
            per_page: itemsPerPage,
            search: searchTerm,
            categories: selectedCategories
        });

        if (loadingMessage) loadingMessage.style.display = 'none';

        const { places, total_places, page, per_page, total_pages } = result;

        if (places.length === 0) {
            placesResultsDiv.innerHTML = '<p>No places found for your query.</p>';
        } else {
            displayPlaces(places);
        }

        currentPage = page;
        totalPages = total_pages;

    } catch (error) {
        if (loadingMessage) loadingMessage.style.display = 'none';
        if (errorMessage) errorMessage.style.display = 'block';
        placesResultsDiv.innerHTML = '<p>Failed to load places. Please try again.</p>';
        console.error("Error in performSearch:", error);
    }
}

// --- Function to display places on the page ---
function displayPlaces(filteredPlaces) {
    placesResultsDiv.innerHTML = "";

    filteredPlaces.forEach(place => {
        const placeCard = document.createElement("div");
        placeCard.classList.add("place-card");
        placeCard.innerHTML = `
            <img src="${place.image_url || '/static/img/placeholder.jpg'}" alt="${place.name}">
            <h4>${place.name}</h4>
            <p class="category">${place.category ? place.category.name : 'Not specified'}</p>
            <p class="short-desc">${place.short_description || place.description || 'No description available'}</p>
            <a href="/places/${place.id}" class="more-btn">Više</a>
        `;
        placesResultsDiv.appendChild(placeCard);
    });
}

// --- Event Listeners ---

// Request is sent only when the search button is clicked
searchButton.addEventListener("click", () => {
    currentPage = 1; // Always reset to the first page for a new search/filter
    performSearch();
});

// Load data on initial page load (without needing to press the button)
document.addEventListener('DOMContentLoaded', performSearch);
