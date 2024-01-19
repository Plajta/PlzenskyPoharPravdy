
function Menu() {
    return (
    <div className="menu">
        
        <div className="search"></div>
        <input type="text" id="mesto" name="mesto" placeholder="Search"/>
        <input type="text" id="dataset" name="dataset" placeholder=""/>

        <div>
            <button>nukede</button>
            <button>generate</button>
        </div>
        
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