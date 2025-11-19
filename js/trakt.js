const traktClientId = '210dc3dd626697b387c064bec175492275e724654a061491802a908f8f62a751';
const tmdbApiKey = 'd3aea9c9b1bb387d2e83a4bb0c923ab3';
const username = 'AJRA';

async function fetchTraktHistory() {
    try {
        // Fetch more items to account for duplicates (multiple episodes of same show)
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

    // Filter for unique shows
    const uniqueShows = [];
    const seenShowSlugs = new Set();

    for (const item of history) {
        const showSlug = item.show?.ids?.slug || item.show?.ids?.trakt;
        if (!showSlug) continue;

        if (!seenShowSlugs.has(showSlug)) {
            seenShowSlugs.add(showSlug);
            uniqueShows.push(item);
            if (uniqueShows.length === 3) break; // Stop once we have 3 unique shows
        }
    }

    // Remove existing dynamic shows (tv2, tv3, tv4) if any, to prevent duplicates
    const existingShows = container.querySelectorAll('.tv2, .tv3, .tv4');
    existingShows.forEach(el => el.remove());

    for (let i = 0; i < uniqueShows.length; i++) {
        const item = uniqueShows[i];
        const show = item.show;
        const tmdbId = show.ids.tmdb;

        const tmdbData = await fetchTMDBShow(tmdbId);

        if (tmdbData) {
            const title = tmdbData.name;
            const posterPath = tmdbData.poster_path ? `https://image.tmdb.org/t/p/w500${tmdbData.poster_path}` : 'images/placeholder.webp';
            const platform = getPlatformName(tmdbData.networks);
            const traktUrl = `https://trakt.tv/shows/${show.ids.slug}`;

            // Assign classes tv2, tv3, tv4 based on index
            const cssClass = `tv${i + 2}`;

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

            container.innerHTML += html;
        }
    }
}

document.addEventListener('DOMContentLoaded', renderShows);
