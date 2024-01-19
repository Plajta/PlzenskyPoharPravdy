
function Menu() {
    return (<div className="map_cont">Menu</div>)
}
function App() {
    return(
        <div>  
            <Menu />
            <MapShow />
            <h1>hello</h1>
        </div>
    );
}



const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<App />);