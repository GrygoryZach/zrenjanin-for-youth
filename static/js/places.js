const searchInput = document.getElementById('search-input');
let filterCheckboxes = document.querySelectorAll(".filters input[type='checkbox']");
const placesResultsDiv = document.getElementById("placesResults");
const loadingMessage = document.getElementById('loading-message');
const errorMessage = document.getElementById('error-message');
const searchButton = document.getElementById('search-button');

let currentPage = 1;
let totalPages = 1;
let itemsPerPage = 10;
const openMapButton = document.getElementById("toggle-map");
const mapModal = document.getElementById("map-modal");
const closeMapButton = document.querySelector(".close-map");
const mapContainer = document.getElementById("map");

let places_data = [];

const categoriesFilterDiv = document.querySelector(".filters .category-filters");
const perPageSelect = document.getElementById('perPageSelect');

let paginationContainer;
let prevPageButton;
let nextPageButton;
let currentPageInfo;

async function fetchAndDisplayCategories() {
    try {
        const response = await fetch('/api/place_categories/basic');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const categories = await response.json();

        if (categoriesFilterDiv) {
            categoriesFilterDiv.innerHTML = '<h3>Kategorije</h3>';

            categories.forEach(category => {
                const label = document.createElement('label');
                // Using category.name for both value and displayed text.
                // Your backend's find_places endpoint filters by PlaceCategory.name.
                label.innerHTML = `<input type="checkbox" name="category" value="${category.name}"> ${category.name}`;
                categoriesFilterDiv.appendChild(label);
            });

            filterCheckboxes = document.querySelectorAll(".filters input[type='checkbox']");
            filterCheckboxes.forEach(checkbox => {
                checkbox.addEventListener("change", () => {
                    filterPlacesByCategory();
                });
            });
        }
    } catch (error) {
        console.error('Error fetching categories:', error);
        if (categoriesFilterDiv) {
            categoriesFilterDiv.innerHTML = '<h3>Kategorije</h3><p>Greška pri učitavanju kategorija.</p>';
        }
    }
}

function filterPlacesByCategory() {
    currentPage = 1;
    performSearch();
}

// TODO обновление маркеров при поиске или фильстрации по категориям
function openMap(mapModal, mapContainer, places) {
    mapModal.classList.remove("hidden");
    setTimeout(() => {
        if (!mapModal.dataset.initialized) {
            initializeMap(mapContainer, places);
            mapModal.dataset.initialized = "true";
        } else {
            const map = mapContainer.mapInstance;
            if (map) {
                map.invalidateSize();
            }
        }
    }, 50);
}

function closeMapModal(mapModal) {
    mapModal.classList.add("hidden");
}

function initializeMap(mapContainer, places) {
    if (mapContainer.mapInstance) {
        mapContainer.mapInstance.remove();
        mapContainer.mapInstance = null;
    }

    const map = L.map(mapContainer, {
        center: [45.38036, 20.39056], // Zrenjanin city center
        zoom: 15,
        zoomSnap: 0.25,
        zoomDelta: 1
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    map.invalidateSize();
    const bounds = new L.LatLngBounds();

    if (places && places.length > 0) {
        places.forEach(place => {
            const [latStr, lngStr] = place.position.split(',');
            const latitude = parseFloat(latStr);
            const longitude = parseFloat(lngStr);

            if (!isNaN(latitude) && !isNaN(longitude)) {
                const marker = L.marker([latitude, longitude]).addTo(map);
                marker.bindPopup(`
                    <strong>${place.name}</strong><br>
                    <p>${place.short_description || 'No description'}</p>
                    <a href="/places/${place.id}">Više</a>
                `);
                bounds.extend([latitude, longitude]);
            } else {
                console.warn(`Invalid coordinates for place: ${place.name} (${place.position})`);
            }
        });

        map.fitBounds(bounds, { padding: [5, 5] });
    } else {
        console.warn("No places data available to display on the map.");
        map.setView([45.38036, 20.39056], 13);
    }

    mapContainer.mapInstance = map;
}

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
        updatePaginationControls();
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
            <p class="category">${place.category && place.category.name ? place.category.name : 'Not specified'}</p>
            <p class="short-desc">${place.short_description || place.description || 'No description available'}</p>
            <a href="/places/${place.id}" class="more-btn">Više</a>
        `;
        placesResultsDiv.appendChild(placeCard);
    });
}


function updatePaginationControls() {
    currentPageInfo.textContent = `Stranica ${currentPage} od ${totalPages}`;

    // Удаляем старые кнопки с номерами страниц
    document.querySelectorAll('.page-number-button').forEach(button => button.remove());

    // Управление активностью кнопок "Prethodna" и "Sledeća"
    prevPageButton.disabled = currentPage <= 1;
    nextPageButton.disabled = currentPage >= totalPages;

    const maxButtons = 5;
    let startPage, endPage;

    if (totalPages <= maxButtons) {
        startPage = 1;
        endPage = totalPages;
    } else if (currentPage <= Math.ceil(maxButtons / 2)) {
        startPage = 1;
        endPage = maxButtons;
    } else if (currentPage + Math.floor(maxButtons / 2) >= totalPages) {
        startPage = totalPages - maxButtons + 1;
        endPage = totalPages;
    } else {
        startPage = currentPage - Math.floor(maxButtons / 2);
        endPage = currentPage + Math.floor(maxButtons / 2);
    }

    for (let i = startPage; i <= endPage; i++) {
        const pageButton = document.createElement('button');
        pageButton.classList.add('page-number-button');
        pageButton.textContent = i;
        if (i === currentPage) {
            pageButton.disabled = true;
        }
        pageButton.addEventListener('click', () => {
            currentPage = i;
            performSearch();
        });
        paginationContainer.insertBefore(pageButton, nextPageButton);
    }
}


document.addEventListener("DOMContentLoaded", function() {
    paginationContainer = document.querySelector('.pagination');
    prevPageButton = document.getElementById('prevPageButton');
    nextPageButton = document.getElementById('nextPageButton');
    currentPageInfo = document.getElementById('currentPageInfo');

    if (!paginationContainer || !prevPageButton || !nextPageButton || !currentPageInfo) {
        console.error("Critical: One or more pagination elements were not found in the DOM.");
        return;
    }
    fetchAndDisplayCategories();

    openMapButton.addEventListener("click", () => {
        openMap(mapModal, mapContainer, places_data);
    });
    closeMapButton.addEventListener("click", () => {
        closeMapModal(mapModal, mapContainer);
    });

    searchButton.addEventListener("click", () => {
        currentPage = 1;
        performSearch();
    });

    searchInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            currentPage = 1;
            performSearch();
        }
    });

    if (perPageSelect) {
        perPageSelect.addEventListener('change', () => {
            itemsPerPage = parseInt(perPageSelect.value, 10);
            currentPage = 1;
            performSearch();
        });
    }

    prevPageButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            performSearch();
        }
    });

    nextPageButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            performSearch();
        }
    });

    performSearch();
});