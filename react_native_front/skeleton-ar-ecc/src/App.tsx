import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="App-header">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h3>Skeleton Based GCN for TPIR on Edge-Cloud Computing</h3>
        </header>

      </div>
      
      <div className="App-body">
        <div className="row">
          <div className="column">
            <button> Turn on Camera </button>
            <button> Upload Image </button>    
          </div>
          <div className="column">
            <p>Skeleton data</p>
          </div>
          <div className="column">
            <button> SIMSLAB </button>
          </div>
        </div>     
        
        

      </div>
      <div className="App-footer"> 
      <p>This is footer</p>
      
      </div>
      


    </div>

  );
}

export default App;
