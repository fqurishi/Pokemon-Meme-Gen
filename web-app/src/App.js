import logo from './logo.svg';
import './App.css';
import Input from './input.js';
import axios from 'axios'

const saveFiles = async(file1,file2,file3) => {
  const formData = new FormData();
  const url = 'http://localhost:3000/uploadFile';

  formData.append('File1',file1);
  formData.append('File2',file2);
  formData.append('File3',file3);
  // Send formData object
  axios.post("api/uploadfile", formData);

}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Who is that Pokemon Generator.
        </h1>
        The worlds only Who is that Pokemon Generator.
        <div><br></br><br></br></div>
        <div>
          <label>Upload Picture</label>
          <br></br>
          <input 
            className="ui-primary-input"  
            type = "file" 
            onChange={(e) => {
              // Update the state
              this.setState({ selectedFile: e.target.files[0] });
            }}
            id="one"
          />
          <br></br><br></br>
          <label>Upload Name (.mp3 or .wav)</label>
          <br></br>
          <input 
            className="ui-primary-input"  
            type = "file" 
            onChange={(e) => {
              // Update the state
              this.setState({ selectedFile: e.target.files[0] });
            }}
            id="two"
          />
          <br></br><br></br>
          <label>Upload Battle Cry (.mp3 or .wav)</label>
          <br></br>
          <input 
            className="ui-primary-input"  
            type = "file" 
            onChange={(e) => {
              // Update the state
              this.setState({ selectedFile: e.target.files[0] });
            }}
            id="three"
          />
        </div>
        <button onClick={saveFiles}>Submit</button>
      </header>
    </div>
  );
}

export default App;
