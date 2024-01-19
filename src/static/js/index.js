
function Menu() {
    return (<div className="map_cont">Menu</div>)
}
function App() {
    return(
        <div className="main_cont">  
            <Menu />
            <MapShow />
        </div>
    );
}



const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<App />);