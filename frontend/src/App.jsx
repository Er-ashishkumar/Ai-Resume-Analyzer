import { useState, useEffect } from "react";
import api from "./services/api";
import ResumeUpload from "./components/ResumeUpload";
import "./App.css";

function App() {
  const [status, setStatus] = useState("Checking backend connection...");

  useEffect(() => {
    api
      .get("/health")
      .then((response) => {
        setStatus(`Backend connected: ${response.data.status}`);
      })
      .catch(() => {
        setStatus("Backend not reachable. Is the Flask server running?");
      });
  }, []);

  return (
    <div className="App">
      <h1>AI Resume Analyzer</h1>
      <p>{status}</p>
      <ResumeUpload />
    </div>
  );
}

export default App;