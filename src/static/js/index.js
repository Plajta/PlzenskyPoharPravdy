
var socket = io();
function nukedeHandler(){
    socket.emit('generate', marker.getLatLng());
}


function Menu() {
    const [value, setValue] = React.useState(false);
    return (
        
    <div className="menu">
        <div className="menu_change_buttons">
            <div className={!value && "menu_change_buttons menu_change_button_active"} onClick={() => {setValue(false)}}>Farts</div>
            <div className={value && "menu_change_buttons menu_change_button_active"} onClick={() => {setValue(true)}}>Nukede</div>
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
                <input type="text" className="typetext" id="mesto" name="mesto" placeholder="Bomb Name"/>
            
                <input type="text" className="typetext" id="dataset" name="dataset"/>

                <div>
                    <button onClick={nukedeHandler}>nukede</button>
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