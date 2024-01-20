
var socket = io();
function nukedeHandler(nuke_value){
    socket.emit('nukede', {lat:marker_bomb.getLatLng().lat, lng:marker_bomb.getLatLng().lng, choosed_nuke:nuke_value});

}
function generateHandler(){
    socket.emit('generate', {lat:marker_gps.getLatLng().lat, lng:marker_gps.getLatLng().lng});
}



socket.on('explode_nuke', function(nuke_data){
    map.remove()
    map = L.map('map').setView({lng: bomb_longitude, lat: bomb_latitude}, 12);

    L.tileLayer(`https://api.mapy.cz/v1/maptiles/basic/256/{z}/{x}/{y}?apikey=${API_KEY}`, {
        minZoom: 0,
        maxZoom: 19,
        attribution: '<a href="https://api.mapy.cz/copyright" target="_blank">&copy; Seznam.cz a.s. a další</a>',
    }).addTo(map);

    
    L.circle([bomb_latitude, bomb_longitude], {
        color: '#3ef7b3',
        fillColor: '#3ef7b3',
        fillOpacity: 0.2,
        radius: nuke_data["nuke_data"]["l-blast-radius"]*1000
    }).addTo(map);
    L.circle([bomb_latitude, bomb_longitude], {
        color: '#595959',
        fillColor: '#595959',
        fillOpacity: 0.2,
        radius: nuke_data["nuke_data"]["t-radiation-radius"]*1000
    }).addTo(map);
    L.circle([bomb_latitude, bomb_longitude], {
        color: '#ffe100',
        fillColor: '#ffe100',
        fillOpacity: 0.2,
        radius: nuke_data["nuke_data"]["m-blast-radius"]*1000
    }).addTo(map);
    L.circle([bomb_latitude, bomb_longitude], {
        color: 'green',
        fillColor: '#42f56c',
        fillOpacity: 0.2,
        radius: nuke_data["nuke_data"]["radiation-radius"]*1000
    }).addTo(map);
    L.circle([bomb_latitude, bomb_longitude], {
        color: '#ff8800',
        fillColor: '#ff8800',
        fillOpacity: 0.2,
        radius: nuke_data["nuke_data"]["h-blast-radius"]*1000
    }).addTo(map);
    L.circle([bomb_latitude, bomb_longitude], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.2,
        radius: nuke_data["nuke_data"]["fireball-radius"]*1000
    }).addTo(map);
    
}
)

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
    marker_bomb.bindPopup("<b>Vaše bomba</b>").openPopup()
    marker_bomb.on('dragend', function (event) {
        var marker = event.target;
        bomb_latitude = marker_bomb.getLatLng().lat;
        bomb_longitude = marker_bomb.getLatLng().lng;
        marker.bindPopup("<b>Vaše bomba</b>").openPopup()
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
    marker_gps.bindPopup("<b>Vaše poloha</b>").openPopup()
}

const nuke_option_list = nuckes_list.map(nuke =>
    <option key={nuke.value} value={nuke.value}>{nuke.name}</option>
  );
function Menu() {
    const [value, setValue] = React.useState(false);
    const [nuke_value, nuke_setValue] = React.useState("LittleBoy");

    return (
        <>
            <div className="menu_change_buttons">
                <div className={!value && "menu_change_buttons menu_change_button_active"} onClick={() => factsmapChange(setValue)}>Fakty</div>
                <div Style="border-radius: 0 10px 0 0;" className={value && "menu_change_buttons menu_change_button_active"} onClick={() => nukemapChange(setValue)}>Zbraň</div>
            </div>
            <div className="menu">
                
                {!value && (
                    <>
                        <input type="text" className="typetext" id="mesto" name="mesto" placeholder="Search"/>
                    
                        <input type="text" className="typetext" id="dataset" name="dataset"/>
                        <div>
                            <button onClick={generateHandler}>generate</button>
                        </div>
                    </>
                )}
                {value && (
                    <>
                        <select value={nuke_value} onChange={e => nuke_setValue(e.target.value)} className="typetext">
                            {nuke_option_list}
                        </select>
                        <div className="circlecount">
                            <div className="circletitle">
                                <div Style="color:red">■</div>
                                <div>Poloměr hřibu</div>
                            </div>
                            <div className="circletitle">
                                <div Style="color:green">■</div>
                                <div>Poloměr radiace</div>
                            </div>
                        </div>
                        <div className="circlecount">
                            <div className="circletitle">
                                <div Style="color:#ff8800">■</div>
                                <div>Silná rázová vlna</div>
                            </div>
                            <div className="circletitle">
                                <div Style="color:#ffe100">■</div>
                                <div>Střední rázová vlna</div>
                            </div>
                        </div>
                        <div className="circlecount">
                            <div className="circletitle">
                                <div Style="color:#42f56c">■</div>
                                <div>Slabá rázová vlna</div>
                            </div>
                            <div className="circletitle">
                                <div Style="color:#595959">■</div>
                                <div>Tepelné záření</div>
                            </div>
                        </div>
                        <div>
                            <button onClick={() => nukedeHandler(nuke_value)}>Spustit simulaci</button>
                        </div>
                    </>
                )}
            </div>
        </>
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