self.addEventListener('push', function(event) {
    const data = event.data.json();
    self.registration.showNotification(data.titulo, {
        body: data.mensaje,
        icon: '/static/img/logo.jpeg',
        badge: '/static/img/logo.jpeg',
    });
});