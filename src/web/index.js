window.onload = () => {
    // replace with your own API key
    const API_KEY = 'YmWIzXtT9Xx5rhFEc2rLnY8ymxWHpAW5D2pGf3P1QlA';

    /*
    We create the map and set its initial coordinates and zoom.
    See https://leafletjs.com/reference.html#map
    */
    const map = L.map('map').setView([49.8729317, 14.8981184], 16);

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