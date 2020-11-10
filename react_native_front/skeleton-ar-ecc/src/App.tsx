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
            <h3 className="ribbon"><strong className="ribbon-content">Data Acqusition</strong></h3>
            <p className="tulisan-kecil">In this steps, we investigate a number of Pose-Estimation Algorithms (OpenPose, PoseNet, HyperPose) to extract skeleton data from video</p>
            <hr className="dashed"></hr>
            <button className="button"><span>Turn On Camera</span></button>
            <button className="button"> <span>Turn Off Camera</span> </button> 
            <div className="camera-canvas">
                            
              <video id="video" width="512" height="512"></video>

            </div>
            
          </div>
          <div className="column">
            <h3 className="ribbon"><strong className="ribbon-content">Skeleton</strong></h3>
            
            <p className="tulisan-kecil">The skeleton-data are sent to the Cloud simultaneously to be the input for GCN Based Inferences, the skeleton-data are saved as continously retrain the model at particular period </p>
            <hr className="dashed"></hr>
            <div className="skeleton-canvas"></div>
          </div>
         
          <div className="column">
            <h3 className="ribbon"><strong className="ribbon-content">Output</strong></h3>
            
            <p className="tulisan-kecil">Action Label from GCN-Based Model then sent back to the Edge. In this case, we focus on nine action on mutual-action subset of NTU RGBD Dataset, TPIR of UT Interaction dataset</p>
            <hr className="dashed"></hr>
            <div className="output-canvas"></div>
          </div>
         
        </div>     
        <br></br>
        

      </div>
      <div className="App-footer"> 
      
      <div className="row"> 
      
      <div className="App-footer-col"> 
        <p>All rights reserved	&copy; SimsLab 2020</p>
      </div >
      <div className="App-footer-col">
          SIMSLAB, NTUST <hr></hr>
          Address: No. 43號, Section 4, Keelung Rd, Da’an District, Taipei City, 106
      </div>
      <div className="App-footer-col">
        Link <hr></hr>
        <p><a href="https://github.com/hendrikTpl/skeleton-based-ar-ecc" className="App-link"> Github </a></p>
        <p><a href="https://deepx.id" className="App-link"> DeepX.id </a></p>
        <p><a href="http://sims.im.ntust.edu.tw/simslabweb/en/home/" className="App-link"> SimsLab </a></p>
      </div>
      </div>
      </div>
      


    </div>

  );
}

export default App;
