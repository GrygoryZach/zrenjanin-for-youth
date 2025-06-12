const data = [
    {
        id: 'p1',
        type: 'place',
        name: 'Kafić Central',
        description: 'Moderan kafić sa prostranom baštom, idealan za opuštanje uz dobru muziku.',
        address: 'Glavna 10',
        image: 'https://via.placeholder.com/600x400/3498db/ffffff?text=Kafic+Central',
        meta: 'Kafić | ⭐ 4.5'
    },
    {
        id: 'p2',
        type: 'place',
        name: 'Klub Inferno',
        description: 'Najbolji noćni provod uz domaću i stranu muziku. Vrhunski DJ-evi.',
        address: 'Subotićeva 5',
        image: 'https://via.placeholder.com/600x400/e74c3c/ffffff?text=Klub+Inferno',
        meta: 'Klub | ⭐ 4.8'
    },
    {
        id: 'p3',
        type: 'place',
        name: 'Restoran Ukus',
        description: 'Odlična hrana i prijatna atmosfera za ručak ili večeru. Domaća kuhinja.',
        address: 'Trg Slobode 3',
        image: 'https://via.placeholder.com/600x400/27ae60/ffffff?text=Restoran+Ukus',
        meta: 'Restoran | ⭐ 4.2'
    },
    {
        id: 'p4',
        type: 'place',
        name: 'Caffe Bar Ritam',
        description: 'Opustite se uz dobru kafu i omiljeno piće. Često i live svirke.',
        address: 'Vojvode Putnika 12',
        image: 'https://via.placeholder.com/600x400/8e44ad/ffffff?text=Caffe+Bar+Ritam',
        meta: 'Caffe Bar | ⭐ 4.3'
    },
    {
        id: 'p5',
        type: 'place',
        name: 'Gaming Centar Matrix',
        description: 'Mesto za gejmere! Najnovije konzole i PC oprema.',
        address: 'Žarka Zrenjanina 2',
        image: 'https://via.placeholder.com/600x400/f1c40f/ffffff?text=Gaming+Centar',
        meta: 'Gaming | ⭐ 4.6'
    },
    {
        id: 'p6',
        type: 'place',
        name: 'Zelena Oaza',
        description: 'Zdrav obroci, smutiji i veganska hrana. Mirna atmosfera.',
        address: 'Bulevar Revolucije 7',
        image: 'https://via.placeholder.com/600x400/2ecc71/ffffff?text=Zdrava+Hrana',
        meta: 'Zdrava Hrana | ⭐ 4.1'
    },
    {
        id: 'e1',
        type: 'event',
        name: 'Koncert "Rock Veče"',
        description: 'Svirka lokalnog rock benda "Zrenjaninski Orlovi" u Klubu Inferno.',
        date: '05.07.2025. u 21:00',
        location: 'Klub Inferno',
        image: 'https://via.placeholder.com/600x400/f39c12/ffffff?text=Rock+Vec%CC%8Ce',
        meta: 'Ulaz: 500 RSD'
    },
    {
        id: 'e2',
        type: 'event',
        name: 'Žurka "Letnje Hlađenje"',
        description: 'DJ set: DJ Srećko - elektronska muzika do jutra u bašti Kafića Central!',
        date: '12.07.2025. u 22:00',
        location: 'Kafić Central (Bašta)',
        image: 'https://via.placeholder.com/600x400/1abc9c/ffffff?text=Letnje+Hladjenje',
        meta: 'Ulaz: Besplatno'
    },
    {
        id: 'e3',
        type: 'event',
        name: 'Stand-up Komedija Veče',
        description: 'Smejte se uz najbolje komičare iz regiona u Kulturnom Centru Zrenjanin.',
        date: '19.07.2025. u 20:00',
        location: 'Kulturni Centar Zrenjanin',
        image: 'https://via.placeholder.com/600x400/9b59b6/ffffff?text=Stand-up',
        meta: 'Ulaz: 700 RSD'
    },
    {
        id: 'e4',
        type: 'event',
        name: 'Filmsko Veče na Otvorenom',
        description: 'Projekcija popularnog filma pod zvezdama u Gradskom Parku.',
        date: '26.07.2025. u 21:00',
        location: 'Gradski Park',
        image: 'https://via.placeholder.com/600x400/34495e/ffffff?text=Film+Park',
        meta: 'Ulaz: Besplatno'
    },
    {
        id: 'e5',
        type: 'event',
        name: 'Turnir u FIFA 25',
        description: 'Veliki FIFA turnir za sve gejmere u Matrix centru. Nagrade za najbolje!',
        date: '03.08.2025. u 18:00',
        location: 'Gaming Centar Matrix',
        image: 'https://via.placeholder.com/600x400/f1c40f/ffffff?text=FIFA+Turnir',
        meta: 'Kotizacija: 200 RSD'
    },
    {
        id: 'e6',
        type: 'event',
        name: 'Joga u Prirodi',
        description: 'Opuštanje i meditacija na otvorenom, voditeljka Ana. Za sve nivoe.',
        date: '10.08.2025. u 09:00',
        location: 'Kej - kod fontane',
        image: 'https://via.placeholder.com/600x400/2ecc71/ffffff?text=Joga+Kej',
        meta: 'Učešće: Besplatno'
    }
];

function createCard(item) {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
        <img src="${item.image}" alt="${item.name}">
        <div class="card-content">
            <h3>${item.name}</h3>
            <p>${item.description}</p>
            <div class="meta">
                ${item.type === 'event' ? `<strong>Kada:</strong> ${item.date}<br><strong>Gde:</strong> ${item.location}` : `<strong>Adresa:</strong> ${item.address}`}
                <br>${item.meta}
            </div>
            <a href="#" class="details-btn">Saznaj više</a>
        </div>
    `;
    return card;
}

function displayFeatured() {
    const eventsGrid = document.getElementById('eventsGrid');
    const placesGrid = document.getElementById('placesGrid');

    eventsGrid.innerHTML = '';
    placesGrid.innerHTML = '';

    const featuredEvents = data.filter(item => item.type === 'event').slice(0, 4);
    const featuredPlaces = data.filter(item => item.type === 'place').slice(0, 4);

    featuredEvents.forEach(event => {
        eventsGrid.appendChild(createCard(event));
    });

    featuredPlaces.forEach(place => {
        placesGrid.appendChild(createCard(place));
    });

    document.getElementById('searchResults').style.display = 'none';
    document.getElementById('featuredEvents').style.display = 'block';
    document.getElementById('featuredPlaces').style.display = 'block';
}

function displaySearchResults(results, searchTerm = '') {
    const searchResultsSection = document.getElementById('searchResults');
    const searchResultGrid = document.getElementById('searchResultGrid');
    searchResultGrid.innerHTML = '';

    const resultsTitle = searchResultsSection.querySelector('h2');
    resultsTitle.textContent = searchTerm ? `Rezultati Pretrage za "${searchTerm}"` : 'Svi Rezultati';

    if (results.length === 0) {
        searchResultGrid.innerHTML = '<p style="text-align: center; color: #777; font-size: 1.1em; padding: 30px;">Nema rezultata za vašu pretragu.</p>';
    } else {
        results.forEach(item => {
            searchResultGrid.appendChild(createCard(item));
        });
    }

    document.getElementById('featuredEvents').style.display = 'none';
    document.getElementById('featuredPlaces').style.display = 'none';
    searchResultsSection.style.display = 'block';
}

function performSearch() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
    const selectedCategory = document.querySelector('.category-filter button.active').dataset.category;

    const filteredResults = data.filter(item => {
        const matchesSearchTerm = item.name.toLowerCase().includes(searchTerm) ||
                                  item.description.toLowerCase().includes(searchTerm) ||
                                  (item.address && item.address.toLowerCase().includes(searchTerm)) ||
                                  (item.location && item.location.toLowerCase().includes(searchTerm));

        if (selectedCategory === 'all') {
            return matchesSearchTerm;
        } else {
            return matchesSearchTerm && item.type === selectedCategory;
        }
    });

    displaySearchResults(filteredResults, searchTerm);
}

document.addEventListener('DOMContentLoaded', () => {
    displayFeatured();

    document.getElementById('search-button').addEventListener('click', performSearch);
    document.getElementById('searchInput').addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            performSearch();
        }
    });

    document.querySelectorAll('.category-filter button').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.category-filter button').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            if (document.getElementById('searchInput').value.trim() !== '') {
                performSearch();
            } else {
                const selectedCategory = this.dataset.category;
                let resultsToDisplay = [];
                if (selectedCategory === 'all') {
                    resultsToDisplay = data;
                    displayFeatured();
                    return;
                } else {
                    resultsToDisplay = data.filter(item => item.type === selectedCategory);
                }
                displaySearchResults(resultsToDisplay, '');
            }
        });
    });

    document.getElementById('searchInput').addEventListener('input', function() {
        const currentCategory = document.querySelector('.category-filter button.active').dataset.category;
        if (this.value.trim() === '' && currentCategory === 'all') {
            displayFeatured();
        } else {
            performSearch();
        }
    });
});