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

    L.tileLayer(`https://tile.openstreetmap.org/{z}/{x}/{y}.png`, {
    minZoom: 0,
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
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


