function renderPost(card, post) {
    card.href = post.url;
    card.setAttribute('aria-label', `Leer «${post.title}» en Substack`);

    const title = card.querySelector('.title');
    const image = card.querySelector('.poster-post');

    title.textContent = post.title;

    image.src = post.image_url;
    image.alt = `Imagen de «${post.title}»`;
    image.referrerPolicy = 'no-referrer';
    image.decoding = 'async';
}

async function renderSubstackPosts() {
    const cards = [...document.querySelectorAll('[data-substack-card]')];

    try {
        const response = await fetch('data/substack.json', { cache: 'no-store' });
        if (!response.ok) throw new Error('No se pudieron cargar los datos de Substack');

        const data = await response.json();
        const posts = [...(data.posts || []), ...(data.more_posts || [])];
        cards.forEach((card, index) => {
            const post = posts[index];
            if (post) renderPost(card, post);
            else card.hidden = true;
        });
    } catch (error) {
        console.error(error);
        cards.forEach((card) => {
            const title = card.querySelector('.title');
            title.textContent = 'SUBSTACK';
        });
    }
}

document.addEventListener('DOMContentLoaded', renderSubstackPosts);
