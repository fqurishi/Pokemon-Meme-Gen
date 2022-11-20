import logo from './logo.svg';
import './App.css';
import Input from './input.js';


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
          <Input content="Upload File2" onChange={(e) => {
            
          }}
          />
          <br></br>
          <label>Upload Name (.mp3 or .wav)</label>
          <Input content="Upload File2" onChange={(e) => {
            
          }}
          />
          <br></br>
          <label>Upload Battle Cry (.mp3 or .wav)</label>
          <Input content="Upload File3" onChange={(e) => {
            
          }}
          />
        </div>
      </header>
    </div>
  );
}

export default App;
