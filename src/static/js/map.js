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

    /*
    We create the map and set its initial coordinates and zoom.
    See https://leafletjs.com/reference.html#map
    */
    map = L.map('map').setView({lng: longitude, lat: latitude}, 16);

    /*
    Then we add a raster tile layer with Mapy NG tiles
    See https://leafletjs.com/reference.html#tilelayer
    */
    L.tileLayer(`https://api.mapy.cz/v1/maptiles/basic/256/{z}/{x}/{y}?apikey=${map_key}`, {
    minZoom: 0,
    maxZoom: 19,
    attribution: '<a href="https://api.mapy.cz/copyright" target="_blank">&copy; Seznam.cz a.s. a další</a>',
    }).addTo(map);
    marker_gps = L.marker([latitude, longitude], { draggable: true }).addTo(map);
    marker_gps.on('dragend', function (event) {
        var marker = event.target;
        socket.emit('get_city', {lat:marker.getLatLng().lat, lng:marker.getLatLng().lng});
        fact_latitude = marker.getLatLng().lat;
        fact_longitude = marker.getLatLng().lng;
        marker_same = false;
    });

    /*
    We also require you to include our logo somewhere over the map.
    We create our own map control implementing a documented interface,
    that shows a clickable logo.
    See https://leafletjs.com/reference.html#control
    */
    // const LogoControl = L.Control.extend({
    // options: {
    //     position: 'bottomleft',
    // },

    // onAdd: function (map) {
    //     const container = L.DomUtil.create('div');
    //     const link = L.DomUtil.create('a', '', container);

    //     link.setAttribute('href', 'http://mapy.cz/');
    //     link.setAttribute('target', '_blank');
    //     link.innerHTML = '<img src="https://api.mapy.cz/img/api/logo.svg" />';
    //     L.DomEvent.disableClickPropagation(link);

    //     return container;
    // },
    // });
    // new LogoControl().addTo(map);
    
}


function watch(pos) {
    const crd = pos.coords;

    if (crd.longitude != longitude && crd.latitude != latitude){
        longitude = crd.longitude
        latitude = crd.latitude
        if (marker_same){
            fact_latitude = latitude
            fact_longitude = longitude
        }
        if (!marker_bomb){
            bomb_longitude = longitude
            bomb_latitude = latitude
            if (marker_same){
                map.setView({lng: longitude, lat: latitude});
                marker_gps.setLatLng([latitude,longitude]);
            
                navigator.geolocation.clearWatch(id)
            }
        }
    }
    navigator.geolocation.clearWatch(id)
    id = undefined;
}


