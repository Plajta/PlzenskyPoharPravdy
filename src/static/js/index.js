
function Menu() {
    return (
    <div className="menu">

        
        <div className="typetextdiv">
            <i className="fa-solid fa-magnifying-glass search"></i>
            <input type="text" className="typetext" id="mesto" name="mesto" placeholder="Search"/>
            </div>
        
        <input type="text" className="typetext" id="dataset" name="dataset"/>

        <div>
            <button >nukede</button>
            <button >generate</button>
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