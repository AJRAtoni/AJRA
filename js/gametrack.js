function renderGameTrackGame(card, game) {
    card.hidden = false;
    card.href = game.url;
    card.setAttribute('aria-label', `${game.title} en GameTrack`);

    const poster = card.querySelector('img');
    poster.src = game.poster_url;
    poster.alt = game.title;
    poster.referrerPolicy = 'no-referrer';
    poster.decoding = 'async';
}

async function renderGameTrackGames() {
    const cards = [...document.querySelectorAll('[data-gametrack-card]')];

    try {
        const response = await fetch('data/gametrack.json', { cache: 'no-store' });
        if (!response.ok) throw new Error('No se pudieron cargar los datos de GameTrack');

        const data = await response.json();
        cards.forEach((card, index) => {
            const game = data.games[index];
            if (game) renderGameTrackGame(card, game);
            else card.hidden = true;
        });
    } catch (error) {
        console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', renderGameTrackGames);
