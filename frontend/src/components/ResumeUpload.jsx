import { useState } from "react";
import api from "../services/api";

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState("");
  const [skills, setSkills] = useState(null);
  const [atsScore, setAtsScore] = useState(null);
  const [atsBreakdown, setAtsBreakdown] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError("");

    try {
      const response = await api.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setExtractedText(response.data.extracted_text);
      setSkills(response.data.skills);
      setAtsScore(response.data.ats_score);
      setAtsBreakdown(response.data.ats_breakdown);
      setSuggestions(response.data.suggestions);
    } catch (err) {
      setError(
        err.response?.data?.error || "Upload failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatCategoryName = (key) => {
    return key
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  return (
    <div className="resume-upload">
      <h2>Upload Your Resume</h2>
      <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {atsScore !== null && (
        <div className="ats-score-section">
          <h3>ATS Score: {atsScore}/100</h3>
          {atsBreakdown && (
            <ul>
              <li>Formatting: {atsBreakdown.formatting}/25</li>
              <li>Keywords: {atsBreakdown.keywords}/30</li>
              <li>Education: {atsBreakdown.education}/20</li>
              <li>Experience: {atsBreakdown.experience}/25</li>
            </ul>
          )}
          {suggestions.length > 0 && (
            <div className="suggestions">
              <strong>Suggestions:</strong>
              <ul>
                {suggestions.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {skills && (
        <div className="skills-section">
          <h3>Extracted Skills</h3>
          {Object.entries(skills).map(([category, skillList]) => (
            <div key={category} className="skill-category">
              <strong>{formatCategoryName(category)}:</strong>{" "}
              {skillList.join(", ")}
            </div>
          ))}
        </div>
      )}

      {extractedText && (
        <div className="extracted-text">
          <h3>Extracted Text</h3>
          <pre>{extractedText}</pre>
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;
