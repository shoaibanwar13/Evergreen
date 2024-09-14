const CACHE_NAME = 'cdn-cache-v1';
const urlsToCache = [
  'https://cdn.tailwindcss.com',
  'https://kit.fontawesome.com/a076d05399.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
  'https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.x.x/dist/alpine.js',
  'https://cdnjs.cloudflare.com/ajax/libs/zxcvbn/4.4.2/zxcvbn.js',
  'https://cdnjs.cloudflare.com/ajax/libs/MaterialDesign-Webfont/5.3.45/css/materialdesignicons.min.css',
  'https://unpkg.com/htmx.org@1.7.0/dist/htmx.min.js'
];

// Install the service worker and cache the CDN resources
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Opened cache');
      return cache.addAll(urlsToCache);
    })
  );
});

// Intercept requests and serve from the cache if available
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      if (response) {
        return response; // Serve from cache
      }
      return fetch(event.request); // Fetch from network
    })
  );
});
