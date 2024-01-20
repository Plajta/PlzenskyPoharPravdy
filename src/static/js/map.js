
const API_KEY = 'YmWIzXtT9Xx5rhFEc2rLnY8ymxWHpAW5D2pGf3P1QlA';
const options = {
    enableHighAccuracy: false,
    timeout: 5000,
    maximumAge: 0,
};



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
    L.tileLayer(`https://api.mapy.cz/v1/maptiles/basic/256/{z}/{x}/{y}?apikey=${API_KEY}`, {
    minZoom: 0,
    maxZoom: 19,
    attribution: '<a href="https://api.mapy.cz/copyright" target="_blank">&copy; Seznam.cz a.s. a další</a>',
    }).addTo(map);

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
        console.log(longitude)
        console.log(latitude)
        if (!marker_bomb){
            bomb_longitude = longitude
            bomb_latitude = latitude

            

            map.remove()
            map = L.map('map').setView({lng: longitude, lat: latitude}, 16);

            L.tileLayer(`https://api.mapy.cz/v1/maptiles/basic/256/{z}/{x}/{y}?apikey=${API_KEY}`, {
                minZoom: 0,
                maxZoom: 19,
                attribution: '<a href="https://api.mapy.cz/copyright" target="_blank">&copy; Seznam.cz a.s. a další</a>',
            }).addTo(map);



            // add_circle([latitude, longitude])

            marker_gps = L.marker([latitude, longitude], { draggable: false }).addTo(map);
            marker_gps.bindPopup("<b>Vaše poloha</b>").openPopup()
        }
    }
}


