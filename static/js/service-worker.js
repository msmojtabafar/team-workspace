const CACHE_NAME = 'team-workspace-v1.0.0';

self.addEventListener('install', function(event) {
  console.log('Service Worker installing...');
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  console.log('Service Worker activating...');
});

self.addEventListener('fetch', function(event) {
  // برای حالا، همه درخواست‌ها از شبکه می‌آیند
  event.respondWith(fetch(event.request));
});
