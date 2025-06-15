importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.4.2/workbox-sw.js');

if (workbox) {
  console.log('Workbox is loaded');
 
    
  // Precache files
  workbox.precaching.precacheAndRoute([
    {url: 'https://cdn.tailwindcss.com', revision: '1'},
    {url: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap', revision: '1'},
    {url: 'https://kit.fontawesome.com/a076d05399.js', revision: '1'},
    {url: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css', revision: '1'},
    {url: 'https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.x.x/dist/alpine.js', revision: '1'},
    {url: 'https://cdnjs.cloudflare.com/ajax/libs/zxcvbn/4.4.2/zxcvbn.js', revision: '1'},
    {url: 'https://cdnjs.cloudflare.com/ajax/libs/MaterialDesign-Webfont/5.3.45/css/materialdesignicons.min.css', revision: '1'},
    {url: 'https://unpkg.com/htmx.org@1.7.0/dist/htmx.min.js', revision: '1'},
    {url: 'https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.x.x/dist/alpine.min.js', revision: '1'},
  ]);

  // Cache images and other assets
  workbox.routing.registerRoute(
    new RegExp('https://cdn.tailwindcss.com'),
    new workbox.strategies.CacheFirst({
      cacheName: 'cdn-cache',
    })
  );
} else {
  console.log('Workbox failed to load');
}
