
const API_KEY = 'YmWIzXtT9Xx5rhFEc2rLnY8ymxWHpAW5D2pGf3P1QlA';
const options = {
    enableHighAccuracy: false,
    timeout: 5000,
    maximumAge: 0,
};

var longitude = 13.381112
var latitude = 49.736953

var map = undefined

var userIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
    text: "vaše poloha"
});

var targetIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

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

    // finally we add our LogoControl to the map
    new LogoControl().addTo(map);
}


function watch(pos) {
    const crd = pos.coords;

    if (crd.longitude != longitude && crd.latitude != latitude){
        longitude = crd.longitude
        latitude = crd.latitude

        console.log(longitude)
        console.log(latitude)

        map.remove()
        map = L.map('map').setView({lng: longitude, lat: latitude}, 16);

        L.tileLayer(`https://api.mapy.cz/v1/maptiles/basic/256/{z}/{x}/{y}?apikey=${API_KEY}`, {
            minZoom: 0,
            maxZoom: 19,
            attribution: '<a href="https://api.mapy.cz/copyright" target="_blank">&copy; Seznam.cz a.s. a další</a>',
        }).addTo(map);

        add_icon([latitude, longitude], userIcon, "vaše poloha")

        //test
        add_icon([latitude + 0.05, longitude + 0.05], targetIcon, "místo odpálení bomby")
        add_polygon([
            [latitude, longitude],
            [latitude - 5, longitude - 5],
            [latitude - 5, longitude + 5]
        ], map)

        add_circle([latitude, longitude])
        marker = L.marker([latitude, longitude], { draggable: true }).addTo(map);

        // Event listener to handle marker dragend event
        marker.on('dragend', function (event) {
            var marker = event.target;
            var position = marker.getLatLng();
            console.log('Marker dragged to:', position);
        });
        marker.bindPopup("<b>Tohle to je </b><br>místo odpálení bomby").openPopup()
    }
}

function add_polygon(coords, map){
    L.polygon(coords).addTo(map);
}

function add_circle(coords){
    L.circle(coords, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 3000
    }).addTo(map);
}

function add_icon(coords, marker_color, text = ""){
    L.marker(coords, {icon: marker_color})
    .bindTooltip(text, 
    {
        permanent: true, 
        direction: 'right'
    }).
    addTo(map)
    .openPopup()
}

