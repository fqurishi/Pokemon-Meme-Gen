import './App.css';
import axios from 'axios'
import React, { Component } from 'react'
import loadImg from './loading.gif';


class App extends React.Component {
  state = {
    selectedFile1: null,
    selectedFile2: null,
    selectedFile3: null,
    fileReadyToDownload: false,
    filePath: null,
    status: "INIT"
   }
  
  fileSelectedHandler1 = e => {
    this.setState({
      selectedFile1: e.target.files[0]
    })
  }
  fileSelectedHandler2 = e => {
    this.setState({
      selectedFile2: e.target.files[0]
    })
  }
  fileSelectedHandler3 = e => {
    this.setState({
      selectedFile3: e.target.files[0]
    })
  }
  
  saveFiles = async () => {
    const formData = new FormData();
    var name = document.getElementById("name").value;
    if (this.state.selectedFile1 === null) {
      return (alert("Please upload pokemon picture!"));
    }
    if (this.state.selectedFile2 === null) {
      return (alert("Please upload name sound!"));
    }
    if (this.state.selectedFile3 === null) {
      return (alert("Please upload battle cry sound!"));
    }
    if (name === "") {
      return (alert("Please enter a name for pokemon!"));
    }
    formData.append('file1',this.state.selectedFile1, this.state.selectedFile1.name);
    formData.append('file2',this.state.selectedFile2, this.state.selectedFile2.name);
    formData.append('file3',this.state.selectedFile3, this.state.selectedFile3.name);
    formData.append('name',this.state.selectedFile3,name)
    // Send formData object
    this.setState({status: "LOADING"})
    const resp = await axios.post("http://www.whoisthat.lol:5000/upload", formData);
    this.setState({filePath: "http://www.whoisthat.lol:5000/upload/" + resp.data})
    this.setState({fileReadyToDownload: true})
    this.setState({status: "COMPLETE"})
  
  }
  render(){
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Who is that Pokemon!? Generator.
        </h1>
        The world's only Who is that Pokemon!? Generator.
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
          <input 
            className="ui-primary-input"  
            type = "textfield"
            name = "name"
            id="name"
            placeholder="Pokemon Name (enter here)"
          />
        </div>
        <br></br>
        <button style={{display: (this.state.status === "LOADING" ? 'none' : 'block')}} disabled={(this.state.status === "LOADING")} onClick={this.saveFiles}>Submit</button>
        <img src={loadImg} style={{display: (this.state.status === "LOADING" ? 'block' : 'none')}}/>
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
