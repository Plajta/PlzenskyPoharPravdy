const options = {
    enableHighAccuracy: false,
    timeout: 5000,
    maximumAge: 0,
};

var id;

window.onload = () => {

    id = navigator.geolocation.watchPosition(watch, (err) => {
        console.error(`ERROR(${err.code}): ${err.message}`);
    }, options);

    map = L.map('map').setView({lng: longitude, lat: latitude}, 16);

    L.tileLayer(`https://api.mapy.cz/v1/maptiles/basic/256/{z}/{x}/{y}?apikey=${API_KEY}`, {
    minZoom: 0,
    maxZoom: 19,
    attribution: '<a href="https://api.mapy.cz/copyright" target="_blank">&copy; Seznam.cz a.s. a další</a>',
    }).addTo(map);
    marker_group = L.featureGroup();
    map.addLayer(marker_group);

    marker_gps = L.marker([latitude, longitude], { draggable: true }).addTo(marker_group);
    marker_gps.on('dragend', function (event) {
        var marker = event.target;
        fact_latitude = marker.getLatLng().lat;
        fact_longitude = marker.getLatLng().lng;
        socket.emit('get_city', {lat:fact_latitude, lng:fact_longitude});
        marker_same = false;
    });

    marker_bomb = L.marker([latitude, longitude], { draggable: true });
    marker_bomb.bindPopup("<b>Vaše bomba</b>")
    marker_bomb.on('dragend', function (event) {
        var marker = event.target;
        bomb_latitude = marker_bomb.getLatLng().lat;
        bomb_longitude = marker_bomb.getLatLng().lng;
        marker_same = false;
        marker.openPopup()
    });

    /*
    We also require you to include our logo somewhere over the map.
    We create our own map control implementing a documented interface,
    that shows a clickable logo.
    See https://leafletjs.com/reference.html#control
    */
    const LogoControl = L.Control.extend({
    options: {
        position: 'bottomleft',
    },

    onAdd: function (map) {
        const container = L.DomUtil.create('div');
        const link = L.DomUtil.create('a', '', container);

        link.setAttribute('href', 'http://mapy.cz/');
        link.setAttribute('target', '_blank');
        link.innerHTML = '<img src="https://api.mapy.cz/img/api/logo.svg" />';
        L.DomEvent.disableClickPropagation(link);

        return container;
    },
    });
    new LogoControl().addTo(map);
    
}


function map_reset() {

    marker_group.remove();
    marker_group = L.featureGroup();
    map.addLayer(marker_group);

}


function watch(pos) {
    const crd = pos.coords;

    if (crd.longitude != longitude && crd.latitude != latitude){
        longitude = crd.longitude
        latitude = crd.latitude
        if (marker_same){
            bomb_latitude = fact_latitude = latitude
            bomb_longitude = fact_longitude = longitude

            map.setView({lng: longitude, lat: latitude});

            marker_gps.setLatLng([latitude,longitude]);
            socket.emit('get_city', {lat:latitude, lng:longitude});
            marker_bomb.setLatLng([latitude,longitude]);

            navigator.geolocation.clearWatch(id)
        }
    }
    navigator.geolocation.clearWatch(id)
    id = undefined;
}


