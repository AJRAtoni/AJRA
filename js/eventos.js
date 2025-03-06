const SPREADSHEET_ID = '1bjuRsUCQLT_MwgKQ9GR7gPHJyYq339v-JHM_ErPbGjI';
const API_KEY = 'AIzaSyBVknxjJb5j7AFLBrltXfOptE1xWweeGJ0';
const eventsContainer = document.getElementById('events');
const placeholderimagen = 'images/eventos/eventos.webp';
let allEvents = [];

// 📌 Formatea la fecha en formato DD/MM/YYYY
const formatDate = (date) => {
    return new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(date);
};

// 📌 Calcula cuántos días faltan para el evento
const calculateDaysRemaining = (eventDate) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const eventDay = new Date(eventDate);
    eventDay.setHours(0, 0, 0, 0);
    const diffDays = Math.ceil((eventDay - today) / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? `FALTAN ${diffDays} DÍAS` : "HOY";
};

// 📌 Convierte fechas del formato "DD/MM/YY" a `Date()`
const parseDate = (dateString) => {
    const [day, month, yearShort] = dateString.split('/').map(Number);
    const year = yearShort < 100 ? 2000 + yearShort : yearShort;
    return new Date(year, month - 1, day);
};

// 📌 Muestra los eventos en la página
const displayEvents = (events) => {
    eventsContainer.innerHTML = '';
    events.forEach(({ titulo, eventDate, descripcion, imagen, url }) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <a href="${url || '#'}" target="_blank">
                <img src="${imagen}" class="event-image" alt="${titulo}" loading="lazy">
            </a>
            <div class="card-body">
                <h2 class="titulo">${titulo}</h2>
                <p class="fecha">${formatDate(eventDate)}</p>
                <p class="descripcion">${descripcion}</p>
                <div class="faltan-container">
                    <p class="faltan">${calculateDaysRemaining(eventDate)}</p>
                </div>
            </div>`;
        eventsContainer.appendChild(card);
    });
};

// 📌 Obtiene los eventos desde Google Sheets
const fetchGoogleSheetEvents = async () => {
    try {
        const response = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Eventos!A2:F?key=${API_KEY}`);
        const data = await response.json();
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        allEvents = (data.values || []).map(row => {
            const [titulo, dateString, descripcion, imageUrl, categoria, url] = row;
            const eventDate = parseDate(dateString);
            return (!isNaN(eventDate.getTime()) && eventDate >= today)
                ? { titulo, eventDate, descripcion, imagen: imageUrl || placeholderimagen, categoria, url }
                : null;
        }).filter(Boolean).sort((a, b) => a.eventDate - b.eventDate);

        displayEvents(allEvents);
    } catch (error) {
        console.error('Error al cargar eventos:', error);
    }
};

// 📌 Filtra eventos por categoría
function filterEvents(categoria) {
    if (!allEvents.length) return;

    document.querySelectorAll('.botonesfiltro').forEach(button => {
        button.classList.add('inactive');
    });

    const activeButton = document.querySelector(`button[data-category="${categoria}"]`);
    if (activeButton) activeButton.classList.remove('inactive');

    const filteredEvents = categoria === 'todos'
        ? allEvents
        : allEvents.filter(event => event.categoria.toLowerCase() === categoria.toLowerCase());

    displayEvents(filteredEvents);
}

// 📌 Configura eventos al cargar la página
document.addEventListener("DOMContentLoaded", function () {
    fetchGoogleSheetEvents();

    document.querySelectorAll('.botonesfiltro').forEach(button => {
        button.addEventListener("click", function () {
            filterEvents(this.getAttribute("data-category"));
        });
    });

    document.getElementById("searchInput").addEventListener("input", searchEvents);
});
