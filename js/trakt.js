const traktClientId = '421ffeb2db44f26a8a2b6b8a5c3e7c946a333c33ff2b7789bab3fdec2f674472';
const tmdbApiKey = 'd3aea9c9b1bb387d2e83a4bb0c923ab3';
const username = 'AJRA';
const cacheBuster = () => Math.floor(Date.now() / 60000);

async function fetchTraktHistory() {
    try {
        // Fetch history (shows and movies)
        const response = await fetch(`https://api.trakt.tv/users/${username}/history?limit=50&_=${cacheBuster()}`, {
            cache: 'no-store',
            headers: {
                'trakt-api-version': '2',
                'trakt-api-key': traktClientId
            }
        });

        if (!response.ok) throw new Error('Error fetching Trakt history');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
        return [];
    }
}

async function fetchTMDBDetails(tmdbId, type) {
    try {
        const response = await fetch(`https://api.themoviedb.org/3/${type}/${tmdbId}?api_key=${tmdbApiKey}&language=es-ES&_=${cacheBuster()}`, {
            cache: 'no-store'
        });
        if (!response.ok) throw new Error(`Error fetching TMDB ${type}`);
        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

function getPlatformName(networks) {
    if (!networks || networks.length === 0) return 'TV';
    const network = networks[0].name;

    // Mapping for common networks
    const mappings = {
        'HBO': 'HBO Max',
        'Apple TV+': 'Apple TV',
        'Netflix': 'Netflix',
        'Disney+': 'Disney+',
        'Amazon': 'Prime Video',
        'Hulu': 'Hulu',
        'Peacock': 'Peacock'
    };

    return mappings[network] || network;
}

function createLazyImage(className, src, alt) {
    const image = document.createElement('img');
    image.className = className;
    image.src = src;
    image.loading = 'lazy';
    image.alt = alt;
    return image;
}

function createInfoBlock(title, platform) {
    const displayTitle = String(title);
    const displayPlatform = String(platform);
    const info = document.createElement('div');
    info.className = 'info';

    const titleElement = document.createElement('h2');
    titleElement.className = 'title';
    titleElement.textContent = displayTitle.toUpperCase();

    const handle = document.createElement('p');
    handle.className = 'handle';
    handle.textContent = displayPlatform;

    info.append(titleElement, handle);
    return info;
}

function createShowCard({ cssClass, traktUrl, title, platform, posterPath }) {
    const displayTitle = String(title);
    const card = document.createElement('a');
    card.href = traktUrl;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    card.className = `caja caja-tv ${cssClass}`;
    card.setAttribute('aria-label', `Enlace a ${displayTitle}`);

    const content = document.createElement('div');
    content.className = 'mitad';
    content.append(
        createLazyImage('logo-normal', 'images/trakttv.webp', 'Trakt TV'),
        createInfoBlock(title, platform)
    );

    const poster = document.createElement('div');
    poster.className = 'mitad';
    poster.append(createLazyImage('poster', posterPath, `Poster de ${displayTitle}`));

    card.append(content, poster);
    return card;
}

async function renderShows() {
    const history = await fetchTraktHistory();
    const container = document.querySelector('.tv');

    if (history.length === 0) {
        console.log("No history found or API error.");
        return;
    }

    // Remove existing dynamic shows (tv2, tv3, tv4) if any, to prevent duplicates
    const existingShows = container.querySelectorAll('.tv2, .tv3, .tv4');
    existingShows.forEach(el => el.remove());

    const seenIds = new Set();
    let renderedCount = 0;

    for (const item of history) {
        if (renderedCount >= 3) break;

        let data, type, tmdbType;

        if (item.type === 'episode') {
            data = item.show;
            type = 'show';
            tmdbType = 'tv';
        } else if (item.type === 'movie') {
            data = item.movie;
            type = 'movie';
            tmdbType = 'movie';
        } else {
            continue;
        }

        if (!data) continue;

        // Deduplicate based on Trakt ID
        const traktId = data.ids?.trakt;
        if (!traktId || seenIds.has(traktId)) continue;
        seenIds.add(traktId);

        let title = data.title || 'SIN TÍTULO';
        let posterPath = 'images/placeholder.webp';
        // Default platform text
        let platform = data.network || (type === 'movie' ? 'Película' : 'TV');

        const slug = data.ids?.slug || traktId;
        // Trakt URLs: /shows/slug or /movies/slug
        const urlType = type === 'show' ? 'shows' : 'movies';
        const traktUrl = `https://trakt.tv/${urlType}/${encodeURIComponent(String(slug))}`;

        const tmdbId = data.ids?.tmdb;
        if (tmdbId) {
            const tmdbData = await fetchTMDBDetails(tmdbId, tmdbType);
            if (tmdbData) {
                // TMDB movies use 'title', TV uses 'name'
                title = tmdbData.title || tmdbData.name || title;
                const tmdbPosterPath = typeof tmdbData.poster_path === 'string' ? tmdbData.poster_path : '';
                posterPath = tmdbPosterPath ? `https://image.tmdb.org/t/p/w500${tmdbPosterPath}` : posterPath;

                if (tmdbType === 'tv') {
                    platform = getPlatformName(tmdbData.networks);
                } else {
                    // For movies, we can keep 'Película' or leave it as is.
                    // If we wanted to be fancy we could check genres, but 'Película' is a safe fallback.
                    platform = 'Película';
                }
            }
        }

        // Assign classes tv2, tv3, tv4 based on rendered order
        const cssClass = `tv${renderedCount + 2}`;

        container.append(createShowCard({ cssClass, traktUrl, title, platform, posterPath }));
        renderedCount++;
    }
}

document.addEventListener('DOMContentLoaded', renderShows);
