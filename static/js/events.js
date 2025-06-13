const searchInput = document.getElementById('search-input');
let filterCheckboxes = document.querySelectorAll(".filters input[type='checkbox']");
const eventsResultsDiv = document.getElementById("results");
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

let events_data = [];

const categoriesFilterDiv = document.querySelector(".filters .category-filters");
const perPageSelect = document.getElementById('perPageSelect');

let paginationContainer;
let prevPageButton;
let nextPageButton;
let currentPageInfo;

async function fetchAndDisplayCategories() {
    try {
        const response = await fetch('/api/event_categories/basic');
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const categories = await response.json();

        if (categoriesFilterDiv) {
            categoriesFilterDiv.innerHTML = '<h3>Kategorije događaja</h3>';

            categories.forEach(category => {
                const label = document.createElement('label');
                label.innerHTML = `<input type="checkbox" name="category" value="${category.name}"> ${category.name}`;
                categoriesFilterDiv.appendChild(label);
            });

            filterCheckboxes = document.querySelectorAll(".filters input[type='checkbox']");
            filterCheckboxes.forEach(checkbox => {
                checkbox.addEventListener("change", () => filterEventsByCategory());
            });
        }
    } catch (error) {
        console.error('Error fetching categories:', error);
        if (categoriesFilterDiv) {
            categoriesFilterDiv.innerHTML = '<h3>Kategorije događaja</h3><p>Greška pri učitavanju kategorija.</p>';
        }
    }
}

function filterEventsByCategory() {
    currentPage = 1;
    performSearch();
}

function openMap(modal, container, events) {
    modal.classList.remove("hidden");
    setTimeout(() => {
        if (!modal.dataset.initialized) {
            initializeMap(container, events);
            modal.dataset.initialized = "true";
        } else {
            const map = container.mapInstance;
            if (map) map.invalidateSize();
        }
    }, 200);
}

function closeMapModal(modal) {
    modal.classList.add("hidden");
}

function initializeMap(container, events) {
    if (container.mapInstance) {
        container.mapInstance.remove();
        container.mapInstance = null;
    }

    const map = L.map(container, {
        center: [45.38036, 20.39056],
        zoom: 15,
        zoomSnap: 0.25,
        zoomDelta: 1
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    map.invalidateSize();
    const bounds = new L.LatLngBounds();

    if (events && events.length > 0) {
        events.forEach(event => {
            const [latStr, lngStr] = event.position.split(',');
            const lat = parseFloat(latStr);
            const lng = parseFloat(lngStr);

            if (!isNaN(lat) && !isNaN(lng)) {
                const marker = L.marker([lat, lng]).addTo(map);
                marker.bindPopup(`
                    <strong>${event.name}</strong><br>
                    <p>${event.short_description || 'No description'}</p>
                    <a href="/events/${event.id}">Više</a>
                `);
                bounds.extend([lat, lng]);
            }
        });

        if (bounds.isValid()) {
            bounds.getSouthWest().equals(bounds.getNorthEast())
                ? map.setView(bounds.getCenter(), 16)
                : map.fitBounds(bounds, { padding: [50, 50] });
        } else {
            map.setView([45.38036, 20.39056], 13);
        }
    } else {
        map.setView([45.38036, 20.39056], 13);
    }

    container.mapInstance = map;
}

async function getEvents({ page = 1, per_page = 10, search = '', categories = [] } = {}) {
    const params = new URLSearchParams({ page, per_page });
    if (search) params.append('search', search);
    if (categories.length > 0) params.append('categories', categories.join(','));

    try {
        const response = await fetch(`/api/events?${params.toString()}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Status: ${response.status}, Message: ${errorData.message || 'Unknown error'}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching events:', error);
        throw error;
    }
}

function updateURLWithSearch() {
    const params = new URLSearchParams();
    const searchTerm = searchInput.value.trim();
    if (searchTerm) params.set('search', searchTerm);

    const selectedCategories = Array.from(filterCheckboxes).filter(cb => cb.checked).map(cb => cb.value);
    if (selectedCategories.length > 0) params.set('categories', selectedCategories.join(','));

    if (currentPage !== 1) params.set('page', currentPage);
    if (itemsPerPage !== 10) params.set('per_page', itemsPerPage);

    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.history.replaceState({}, '', newUrl);
}

async function performSearch() {
    updateURLWithSearch();
    loadingMessage.style.display = 'block';
    errorMessage.style.display = 'none';
    eventsResultsDiv.innerHTML = '';

    const searchTerm = searchInput.value;
    const selectedCategories = Array.from(filterCheckboxes).filter(cb => cb.checked).map(cb => cb.value);

    try {
        const { events, total_events, page, per_page, total_pages } = await getEvents({
            page: currentPage,
            per_page: itemsPerPage,
            search: searchTerm,
            categories: selectedCategories
        });

        loadingMessage.style.display = 'none';
        events_data = events;

        if (!events || events.length === 0) {
            eventsResultsDiv.innerHTML = '<p>Ništa nije pronađeno za vašu pretragu.</p>';
        } else {
            displayEvents(events);
        }

        currentPage = page;
        totalPages = total_pages;
        updatePaginationControls();

        initializeMap(mapContainer, events_data);
    } catch (error) {
        loadingMessage.style.display = 'none';
        errorMessage.style.display = 'block';
        console.log(error);
        eventsResultsDiv.innerHTML = '<p>Došlo je do greške. Pokušajte ponovo.</p>';
    }
}

function displayEvents(events) {
    eventsResultsDiv.innerHTML = '';
    events.forEach(event => {
        const eventCard = document.createElement('div');
        eventCard.classList.add('place-card');
        eventCard.innerHTML = `
            <img src="${event.image_url || '/static/img/placeholder.jpg'}" alt="${event.name}">
            <h4>${event.name}</h4>
            <p class="category">${event.category?.category_name || 'Nedefinisano'}</p>
            <p class="short-desc">${event.short_description || event.description || 'Opis nije dostupan'}</p>
            <a href="/events/${event.id}" class="more-btn">Više</a>
        `;
        eventsResultsDiv.appendChild(eventCard);
    });
}

function updatePaginationControls() {
    currentPageInfo.textContent = `Stranica ${currentPage} od ${totalPages}`;
    document.querySelectorAll('.page-number-button').forEach(b => b.remove());

    prevPageButton.disabled = currentPage <= 1;
    nextPageButton.disabled = currentPage >= totalPages;

    const maxButtons = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxButtons / 2));
    let endPage = Math.min(totalPages, startPage + maxButtons - 1);

    if (endPage - startPage < maxButtons - 1) {
        startPage = Math.max(1, endPage - maxButtons + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
        const btn = document.createElement('button');
        btn.classList.add('page-number-button');
        btn.textContent = i;
        if (i === currentPage) btn.disabled = true;
        btn.addEventListener('click', () => {
            currentPage = i;
            performSearch();
        });
        paginationContainer.insertBefore(btn, nextPageButton);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    paginationContainer = document.querySelector('.pagination');
    prevPageButton = document.getElementById('prevPageButton');
    nextPageButton = document.getElementById('nextPageButton');
    currentPageInfo = document.getElementById('currentPageInfo');

    if (!paginationContainer || !prevPageButton || !nextPageButton || !currentPageInfo) {
        console.error("Pagination elements not found.");
        return;
    }

    fetchAndDisplayCategories();

    openMapButton.addEventListener("click", () => openMap(mapModal, mapContainer, events_data));
    closeMapButton.addEventListener("click", () => closeMapModal(mapModal));

    searchButton.addEventListener("click", () => {
        currentPage = 1;
        performSearch();
    });

    searchInput.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            event.preventDefault();
            currentPage = 1;
            performSearch();
        }
    });

    perPageSelect?.addEventListener('change', () => {
        itemsPerPage = parseInt(perPageSelect.value, 10);
        currentPage = 1;
        performSearch();
    });

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

    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('search');
    if (query) {
        searchInput.value = query;
    }

    performSearch();
});
