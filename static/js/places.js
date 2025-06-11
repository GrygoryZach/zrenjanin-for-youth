const searchInput = document.getElementById('search-input');
const filterCheckboxes = document.querySelectorAll(".filters input[type='checkbox']");
const placesResultsDiv = document.querySelector(".places-grid-container");
const loadingMessage = document.getElementById('loading-message');
const errorMessage = document.getElementById('error-message');
const searchButton = document.getElementById('search-button'); // New element: search button

let currentPage = 1;
let totalPages = 1;
const openMapButton = document.getElementById("toggle-map");
const mapModal = document.getElementById("map-modal");
const closeMapButton = document.querySelector(".close-map");
const mapContainer = document.getElementById("map");

let places_data = []; // PLaces data (should be uploaded from server)

// Waiting for the DOM to load
document.addEventListener("DOMContentLoaded", function() {
    openMapButton.addEventListener("click", () => {
        openMap(mapModal, mapContainer, places_data)
    });
    closeMapButton.addEventListener("click", () => {
        closeMapModal(mapModal, mapContainer)
    });

    // Handle input in the search field
    searchInput.addEventListener("input", (event) => {
        searchFunction(event.target, places_data);
    });


    // Listen to changes in the filters
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            filterPlacesByCategory(places, filterCheckboxes);
        });
    });

    // --- Event Listeners ---

    // Request is sent only when the search button is clicked
    searchButton.addEventListener("click", () => {
        currentPage = 1; // Always reset to the first page for a new search/filter
        performSearch();
    });

    performSearch()
});


function openMap(mapModal, mapContainer, places) {
    mapModal.classList.remove("hidden");
    if (!mapModal.dataset.initialized) {
        initializeMap(mapContainer, places);
        mapModal.dataset.initialized = "true";
    }
}

function closeMapModal(mapModal) {
    mapModal.classList.add("hidden");
}

function initializeMap(mapContainer, places) {
    const map = L.map(mapContainer, {
        center: [45.38036, 20.39056], // Zrenjanin city center
        zoom: 15,
        zoomSnap: 0.25,
        zoomDelta: 1
    });

    // Basic map layers
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    const bounds = new L.LatLngBounds(); // Create a bounds object to contain all markers

    // Add markers for each place
    places.forEach(place => {
        const [latStr, lngStr] = place.position.split(',');
        const latitude = parseFloat(latStr);
        const longitude = parseFloat(lngStr);
        const marker = L.marker([latitude, longitude]).addTo(map);
        marker.bindPopup(`
            <strong>${place.name}</strong><br>
            <p>${place.short_description}</p>
            <a href="/places/${place.id}">Više</a>
        `);
        bounds.extend([latitude, longitude]); // Extend the bounds to include each marker's position
    });

    // Fit map bounds to include all places
    map.fitBounds(bounds);

    // Adjust zoom level to be a bit smaller (zoom out by 1 level)
    const currentZoom = map.getZoom(); // Get the current zoom level after fitBounds
    map.setZoom(currentZoom - 0.25); // Zoom out by 1 level (adjust this value as needed)
}



// --- Asynchronous JavaScript function to make an API request ---
async function getPlaces(options = {}) {
    const { page = 1, per_page = 10, search = '', categories = [] } = options;

    const params = new URLSearchParams();
    params.append('page', page);
    params.append('per_page', per_page);

    if (search) params.append('search', search);
    if (categories.length > 0) params.append('categories', categories.join(','));
    const url = `/api/places?${params.toString()}`;

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
        console.error('Error fetching places:', error);
        throw error;
    }
}


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
        places_data = places;

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
        console.error('Error in performSearch:', error);
    }
}

// --- Function to display places on the page ---
function displayPlaces(filteredPlaces) {
    placesResultsDiv.innerHTML = '';

    filteredPlaces.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.classList.add('place-card');

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