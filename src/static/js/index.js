
var socket = io();
function nukedeHandler(nuke_value){
    socket.emit('generate', {lat:marker_bomb.getLatLng().lat, lng:marker_bomb.getLatLng().lng, choosed_nuke:nuke_value});

}

const nukemapChange = (setValue) => {
    setValue(true)
    console.log(bomb_longitude)
    console.log(bomb_latitude)

    map.remove()
    map = L.map('map').setView({lng: bomb_longitude, lat: bomb_latitude}, 16);

    L.tileLayer(`https://api.mapy.cz/v1/maptiles/basic/256/{z}/{x}/{y}?apikey=${API_KEY}`, {
        minZoom: 0,
        maxZoom: 19,
        attribution: '<a href="https://api.mapy.cz/copyright" target="_blank">&copy; Seznam.cz a.s. a další</a>',
    }).addTo(map);



    // add_circle([latitude, longitude])

    marker_bomb = L.marker([bomb_latitude, bomb_longitude], { draggable: true }).addTo(map);
    marker_bomb.bindPopup("<b>Vaši bomba</b>").openPopup()
    marker_bomb.on('dragend', function (event) {
        var marker = event.target;
        bomb_latitude = marker_bomb.getLatLng().lat;
        bomb_longitude = marker_bomb.getLatLng().lng;
        marker.bindPopup("<b>Vaši bomba</b>").openPopup()
    });
}

const factsmapChange = (setValue) => {
    setValue(false)

    console.log(longitude)
    console.log(latitude)
    map.remove()
    map = L.map('map').setView({lng: longitude, lat: latitude}, 16);
    L.tileLayer(`https://api.mapy.cz/v1/maptiles/basic/256/{z}/{x}/{y}?apikey=${API_KEY}`, {
        minZoom: 0,
        maxZoom: 19,
        attribution: '<a href="https://api.mapy.cz/copyright" target="_blank">&copy; Seznam.cz a.s. a další</a>',
    }).addTo(map);
    marker_gps = L.marker([latitude, longitude], { draggable: false }).addTo(map);
    marker_gps.bindPopup("<b>Vaši poloha</b>").openPopup()
}

const nuke_option_list = nuckes_list.map(nuke =>
    <option key={nuke.value} value={nuke.value}>{nuke.name}</option>
  );
function Menu() {
    const [value, setValue] = React.useState(false);
    const [nuke_value, nuke_setValue] = React.useState("Little Boy");
    return (
        
    <div className="menu">
        <div className="menu_change_buttons">
            <div className={!value && "menu_change_buttons menu_change_button_active"} onClick={() => factsmapChange(setValue)}>Farts</div>
            <div className={value && "menu_change_buttons menu_change_button_active"} onClick={() => nukemapChange(setValue)}>Nukede</div>
        </div>
        {!value && (
            <>
                <input type="text" className="typetext" id="mesto" name="mesto" placeholder="Search"/>
            
                <input type="text" className="typetext" id="dataset" name="dataset"/>
                <div>
                    <button>generate</button>
                </div>
            </>
        )}
        {value && (
            <>
                <select value={nuke_value} onChange={e => nuke_setValue(e.target.value)} className="typetext">
                    {nuke_option_list}
                </select>

                <div>
                    <button onClick={() => nukedeHandler(nuke_value)}>Nukede!</button>
                </div>
            </>
        )}
    </div>
    )
}
function App() {
    return(
        <div className="main_cont">  
            <Menu />
        </div>
    );
}



const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<App />);