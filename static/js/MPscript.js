// Waiting for the DOM to load
document.addEventListener("DOMContentLoaded", function() {
    const mapToggle = document.getElementById("toggle-map");
    const mapModal = document.getElementById("map-modal");
    const closeMap = document.querySelector(".close-map");
    const mapContainer = document.getElementById("map");
    const searchInput = document.getElementById("search-input");
    const filterCheckboxes = document.querySelectorAll(".filters input[type='checkbox']");

    let places = []; // PLaces data (should be uploaded from server)

    mapToggle.addEventListener("click", openMap);
    closeMap.addEventListener("click", closeMapModal);

    function openMap() {
        mapModal.classList.remove("hidden");
        if (!mapModal.dataset.initialized) {
            initializeMap();
            mapModal.dataset.initialized = "true";
        }
    }

    function closeMapModal() {
        mapModal.classList.add("hidden");
    }

    function initializeMap() {
        const map = L.map(mapContainer).setView([45.38036, 20.39056], 15); // Centered on Zrenjanin city center

        // Basic map layers
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        const bounds = new L.LatLngBounds(); // Create a bounds object to contain all markers

        // Add markers for each place
        places.forEach(place => {
            const marker = L.marker([place.latitude, place.longitude]).addTo(map);
            marker.bindPopup(`
                <strong>${place.name}</strong><br>
                <p>${place.short_description}</p>
                <a href="/places/${place.id}">Više</a>
            `);

            bounds.extend([place.latitude, place.longitude]); // Extend the bounds to include each marker's position
        });

        // Fit map bounds to include all places
        map.fitBounds(bounds);

        // Adjust zoom level to be a bit smaller (zoom out by 1 level)
        const currentZoom = map.getZoom(); // Get the current zoom level after fitBounds
        map.setZoom(currentZoom - 1); // Zoom out by 1 level (adjust this value as needed)
    }


    function filterPlacesByCategory() {
        const selectedCategories = Array.from(filterCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);

        const filteredPlaces = places.filter(place => {
            if (selectedCategories.length === 0) return true; // If no filters used, show all places
            return selectedCategories.includes(place.category);
        });

        displayPlaces(filteredPlaces);
    }

    function displayPlaces(filteredPlaces) {
        const placesContainer = document.querySelector(".places-grid");
        placesContainer.innerHTML = ""; // Clear the container

        filteredPlaces.forEach(place => {
            const placeCard = document.createElement("div");
            placeCard.classList.add("place-card");
            placeCard.innerHTML = `
                <img src="${place.image_url || '/static/img/placeholder.jpg'}" alt="${place.name}">
                <h4>${place.name}</h4>
                <p class="category">${place.category}</p>
                <p class="short-desc">${place.short_description}</p>
                <a href="/places/${place.id}" class="more-btn">Više</a>
            `;
            placesContainer.appendChild(placeCard);
        });
    }

    // Handle input in the search field
    searchInput.addEventListener("input", function() {
        const query = searchInput.value.toLowerCase();
        const filteredPlaces = places.filter(place =>
        place.name.toLowerCase().includes(query) ||
        place.short_description.toLowerCase().includes(query)
        );
        displayPlaces(filteredPlaces);
    });

    // Listen to changes in the filters
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", filterPlacesByCategory);
    });

    places = [
        {
            "id": 1,
            "name": "Vinyl Bassic",
            "category": "entertainment",
            "latitude": 45.37995,
            "longitude": 20.39280,
            "image_url": "https://media.ilovezrenjanin.com/2024/05/vinyl-bassic-2-e1716305224556.jpg",
            "short_description": "Popularno mesto u centru grada sa muzičkim događajima i opuštenom atmosferom."
        },
        {
            "id": 2,
            "name": "Caffe Bridge",
            "category": "entertainment",
            "latitude": 45.37934,
            "longitude": 20.38927,
            "image_url": "https://scontent.fbeg7-2.fna.fbcdn.net/v/t39.30808-6/471450851_1144297101034417_3375446139899935729_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=833d8c&_nc_ohc=cqp7u19PUJkQ7kNvwFP4bxO&_nc_oc=AdmHaLa4vSYKPxpGesmmiXni7droYJuJYl4LsIkABoqvKOUB1-ae-O7I2KPc_gLDxNY&_nc_zt=23&_nc_ht=scontent.fbeg7-2.fna&_nc_gid=x9yGxgEB7FE_WkgSNTSXZw&oh=00_AfKAUpelC3FGSpVoqHQX-Bp8X8_86XE0xNPm_pf4m4y26A&oe=68290B22",
            "short_description": "Kafić sa prelepim pogledom na reku, idealan za opuštanje uz koktel ili kafu."
        },
        {
            "id": 4,
            "name": "Kulturni centar Zrenjanin",
            "category": "culture",
            "latitude": 45.37826,
            "longitude": 20.38999,
            "image_url": "https://105.rs/wp-content/uploads/2023/05/kulturni-centar-zr.png",
            "short_description": "Savremeni prostor za kulturna dešavanja u srcu grada, sa bogatim programom koncerata, izložbi i predstava."
        }
    ]

    displayPlaces(places);
});


const currentUrl = window.location.href; 
// Example: "http://localhost:5000/page?name=John"

console.log(currentUrl);