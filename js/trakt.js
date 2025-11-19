const traktClientId = '210dc3dd626697b387c064bec175492275e724654a061491802a908f8f62a751';
const tmdbApiKey = 'd3aea9c9b1bb387d2e83a4bb0c923ab3';
const username = 'AJRA';

async function fetchTraktHistory() {
    try {
        // Fetch more items to account for multiple episodes of the same show
        const response = await fetch(`https://api.trakt.tv/users/${username}/history/shows?limit=15`, {
            headers: {
                'Content-Type': 'application/json',
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

async function fetchTMDBShow(tmdbId) {
    try {
        const response = await fetch(`https://api.themoviedb.org/3/tv/${tmdbId}?api_key=${tmdbApiKey}&language=es-ES`);
        if (!response.ok) throw new Error('Error fetching TMDB show');
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

    const seenShowSlugs = new Set();
    let renderedCount = 0;

    for (const item of history) {
        if (renderedCount >= 3) break;

        const show = item.show;
        if (!show) continue;

        const showSlug = show.ids?.slug || show.ids?.trakt;
        if (!showSlug || seenShowSlugs.has(showSlug)) continue;
        seenShowSlugs.add(showSlug);

        let title = show.title || 'SIN TÍTULO';
        let posterPath = 'images/placeholder.webp';
        let platform = show.network || 'TV';
        const traktUrl = `https://trakt.tv/shows/${showSlug}`;

        const tmdbId = show.ids?.tmdb;
        if (tmdbId) {
            const tmdbData = await fetchTMDBShow(tmdbId);
            if (tmdbData) {
                title = tmdbData.name || title;
                posterPath = tmdbData.poster_path ? `https://image.tmdb.org/t/p/w500${tmdbData.poster_path}` : posterPath;
                platform = getPlatformName(tmdbData.networks);
            }
        }

        // Assign classes tv2, tv3, tv4 based on rendered order
        const cssClass = `tv${renderedCount + 2}`;

        const html = `
            <a href="${traktUrl}" target="_blank" class="caja caja-tv ${cssClass}" aria-label="Enlace a ${title}">
                <div class="mitad">
                    <img class="logo-normal" src="images/trakttv.webp" loading="lazy" alt="Trakt TV">
                    <div class="info">
                        <h2 class="title">${title.toUpperCase()}</h2>
                        <p class="handle">${platform}</p>
                    </div>
                </div>
                <div class="mitad">
                    <img class="poster" src="${posterPath}" loading="lazy" alt="Poster">
                </div>
            </a>
        `;

        container.insertAdjacentHTML('beforeend', html);
        renderedCount++;
    }
}

document.addEventListener('DOMContentLoaded', renderShows);
