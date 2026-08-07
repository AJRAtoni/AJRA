function renderFilm(card, film) {
    card.href = film.url;
    card.setAttribute('aria-label', `Ver ${film.title} en Letterboxd`);

    const title = card.querySelector('.title');
    const poster = card.querySelector('.poster');

    title.textContent = film.title.toUpperCase();

    poster.src = film.poster_url;
    poster.alt = `Póster de ${film.title}`;
    poster.referrerPolicy = 'no-referrer';
    poster.decoding = 'async';
}

async function renderLetterboxdFilms() {
    const cards = [...document.querySelectorAll('[data-letterboxd-card]')];

    try {
        const response = await fetch('data/letterboxd.json', { cache: 'no-store' });
        if (!response.ok) throw new Error('No se pudieron cargar los datos de Letterboxd');

        const data = await response.json();
        cards.forEach((card, index) => {
            const film = data.films[index];
            if (film) renderFilm(card, film);
            else card.hidden = true;
        });
    } catch (error) {
        console.error(error);
        cards.forEach((card) => {
            const title = card.querySelector('.title');
            title.textContent = 'LETTERBOXD';
        });
    }
}

document.addEventListener('DOMContentLoaded', renderLetterboxdFilms);
