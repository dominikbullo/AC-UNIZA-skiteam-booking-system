// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = 'sport-agenda-v' + new Date().getTime()
var filesToCache = [
  '/offline',
  '/css/django-pwa-app.css',
  '/images/icons/icon-72x72.png',
  '/images/icons/icon-96x96.png',
  '/images/icons/icon-128x128.png',
  '/images/icons/icon-144x144.png',
  '/images/icons/icon-152x152.png',
  '/images/icons/icon-192x192.png',
  '/images/icons/icon-384x384.png',
  '/images/icons/icon-512x512.png'
]
// Bump this version number each time a cached or asset changes.
// If you don't, the SW won't be reinstalled and the pages you cache initially won't be updated
// (by default at least, see next sections for more on caching).
const VERSION = '0.0.2'

// Cache on install
self.addEventListener('install', event => {
  console.log('[SW] Installing SW version:', VERSION, staticCacheName)
  this.skipWaiting()
  event.waitUntil(
    caches.open(staticCacheName)
      .then(cache => {
        return cache.addAll(filesToCache)
      })
  )
})

// Clear cache on activate
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(cacheName => (cacheName.startsWith('sport-agenda-')))
          .filter(cacheName => (cacheName !== staticCacheName))
          .map(cacheName => caches.delete(cacheName))
      )
    })
  )
})

// Serve from Cache
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request)
      })
      .catch(() => {
        console.log('offline')
        // return caches.match('offline')
      })
  )
})
