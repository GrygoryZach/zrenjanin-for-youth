document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.top-bar input[type="text"]');
    const searchButton = document.querySelector('#search-button');
    const categoryButtons = document.querySelectorAll('.toggle-places-events button');
    const cards = document.querySelectorAll('.card');

    let selectedCategory = 'places'; // по умолчанию выбрана "Mesta"

    function filterCards() {
        const query = searchInput.value.toLowerCase().trim();

        cards.forEach(card => {
            const title = card.querySelector('h3')?.textContent.toLowerCase() || '';
            const description = card.querySelector('p')?.textContent.toLowerCase() || '';
            const category = card.dataset.category?.toLowerCase() || '';

            const matchesCategory = !selectedCategory || category === selectedCategory.toLowerCase();
            const matchesQuery = !query || title.includes(query) || description.includes(query);

            if (matchesCategory && matchesQuery) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }

    // Обновляем selectedCategory при клике
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            selectedCategory = button.dataset.category || 'places';
            filterCards();
        });
    });

    function redirectToSearch() {
        const query = encodeURIComponent(searchInput.value.trim());
        if (!query) return; // Если пусто, ничего не делать

        let url = '/place_search';
        if (selectedCategory === 'events') {
            url = '/event_search';
        }
        window.location.href = `${url}?search=${query}`;
    }

    searchButton.addEventListener('click', (e) => {
        e.preventDefault();
        redirectToSearch();
    });

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            redirectToSearch();
        }
    });

});
