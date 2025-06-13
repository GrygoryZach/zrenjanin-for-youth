const eventId = window.location.pathname.split('/').pop();

document.addEventListener('DOMContentLoaded', async () => {
  const [eventRes, placeRes] = await Promise.all([
    fetch(`/api/events/${eventId}`),
    fetch(`/api/events/${eventId}/place`)
  ]);

  if (!eventRes.ok || !placeRes.ok) {
    alert("Error during downloading the place");
    return;
  }

  const event = await eventRes.json();
  const place = await placeRes.json();

  document.getElementById('event-name').textContent = event.name;
  document.getElementById('event-category').textContent = event.category?.name || '—';
  document.getElementById('event-datetime').textContent = new Date(event.datetime).toLocaleString();
  document.getElementById('event-description').textContent = event.description || '—';
  document.getElementById('event-image').src = '/' + event.image_url || '/static/placeholder.jpg';

  const placeName = place.name || '—';
  const placeId = place.id;
  document.getElementById('event-place').innerHTML = `<a href="/places/${placeId}">${placeName}</a>`;

  if (place.position) {
    const [lat, lng] = place.position.split(',').map(coord => parseFloat(coord.trim()));
    const map = L.map('map').setView([lat, lng], 16 );
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    L.marker([lat, lng]).addTo(map).bindPopup(place.name);
  }
});
