import './App.css';
import axios from 'axios'
import React, { Component } from 'react'


class App extends React.Component {
  state = {
    selectedFile1: null,
    selectedFile2: null,
    selectedFile3: null,
    fileReadyToDownload: false,
    filePath: null
   }
  
  fileSelectedHandler1 = e => {
    this.setState({
      selectedFile1: e.target.files[0]
    })
    console.log(e.target.files[0]);
  }
  fileSelectedHandler2 = e => {
    this.setState({
      selectedFile2: e.target.files[0]
    })
    console.log(e.target.files[0]);
  }
  fileSelectedHandler3 = e => {
    this.setState({
      selectedFile3: e.target.files[0]
    })
    console.log(e.target.files[0]);
  }
  
  saveFiles = async () => {
    const formData = new FormData();
  
    console.log(this.state.selectedFile1.name)
    console.log(this.state.selectedFile2.name)
    console.log(this.state.selectedFile3.name)
    formData.append('file1',this.state.selectedFile1, this.state.selectedFile1.name);
    formData.append('file2',this.state.selectedFile2, this.state.selectedFile2.name);
    formData.append('file3',this.state.selectedFile3, this.state.selectedFile3.name);
    // Send formData object
    const resp = await axios.post("//localhost:5000/upload", formData);
    console.log(resp.data);
    this.setState({filePath: "http://localhost:5000/upload/" + resp.data})
    this.setState({fileReadyToDownload: true})
  
  }
  render(){
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Who is that Pokemon Generator.
        </h1>
        The worlds only Who is that Pokemon Generator.
        <div><br></br><br></br></div>
        <div>
          <input 
            className="ui-primary-input"  
            type = "file" 
            onChange={this.fileSelectedHandler1}
            id="one"
            style = {{display: 'none'}}
            ref = {fileInput1 => this.fileInput1 = fileInput1}
          />
          <button onClick={() => this.fileInput1.click()}>Upload Picture</button>
          <input 
            className="ui-primary-input"  
            type = "file" 
            onChange={this.fileSelectedHandler2}
            id="two"
            style = {{display: 'none'}}
            ref = {fileInput2 => this.fileInput2 = fileInput2}
          />
          <button onClick={() => this.fileInput2.click()}>Upload Name (.mp3 or .wav)</button>
          <input 
            className="ui-primary-input"  
            type = "file"
            name = "file"
            onChange={this.fileSelectedHandler3} 
            id="three"
            style = {{display: 'none'}}
            ref = {fileInput3 => this.fileInput3 = fileInput3}
          />
          <button onClick={() => this.fileInput3.click()}>Upload Battle Cry (.mp3 or .wav) </button>
        </div>
        <button onClick={this.saveFiles}>Submit</button>
        <a href={this.state.filePath} 
          style = {{display: (this.state.fileReadyToDownload ? 'block' : 'none')}}>
          <button>Download</button>
        </a>
      </header>
    </div>
  );
}
}

export default App;
