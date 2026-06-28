import html2canvas from "html2canvas";
import { useState, useEffect } from "react";
import axios from "axios";
import { jsPDF } from "jspdf";
import "./App.css";

function App() {

  const [companies, setCompanies] = useState([]);
  const [company, setCompany] = useState("");
  const [searchCompany, setSearchCompany] = useState("");
  const [skills, setSkills] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [result, setResult] = useState(null);
  const [completedSkills, setCompletedSkills] = useState([]);
  const [darkMode, setDarkMode] = useState(false);
  const [loading, setLoading] = useState(false);


  useEffect(() => {
    fetchCompanies();
  }, []);

  async function fetchCompanies() {

    try {

      const response = await axios.get(
        "https://ai-career-prep-assistant.onrender.com/companies"
      );

      const companyNames = Object.keys(response.data);

      setCompanies(companyNames);

      if (companyNames.length > 0) {
        setCompany(companyNames[0]);
      }

    } catch (error) {

      console.log(error);
      alert("Error fetching companies!");

    }
  }

  async function uploadResume() {

    if (!resumeFile) {

      alert("Please select a resume PDF!");
      return;

    }

    try {

      const formData = new FormData();

      formData.append(
        "file",
        resumeFile
      );

      const response = await axios.post(
        "https://ai-career-prep-assistant.onrender.com/upload-resume",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      );
    setSkills(
  response.data.skills.join(", ")
);


alert(
  "Resume analyzed successfully!"
);

    } catch (error) {

      console.log(error);

      alert(
        "Error uploading resume!"
      );

    }
  }

  async function generateRoadmap() {

  try {

    setLoading(true);

    setCompletedSkills([]);

    const skillsList = skills
      .split(",")
      .map((skill) => skill.trim())
      .filter((skill) => skill !== "");

    const response = await axios.post(
      "https://ai-career-prep-assistant.onrender.com/generate-ai-roadmap",
      {
        company: company,
        skills: skillsList
      }
    );

    setResult({
      roadmap: response.data.ai_roadmap.split("\n"),
      missing_skills: skillsList,
      aptitude: [],
      hr_questions: [],
      mock_interview: []
    });

  } catch (error) {

    console.log(error);

    alert("Error connecting to backend!");

  } finally {

    setLoading(false);

  }

}

  async function saveProgress(skill, completed) {

    try {

      await axios.post(
        "https://ai-career-prep-assistant.onrender.com/save-progress",
        {
          company: company,
          skill: skill,
          completed: completed
        }
      );

      if (completed) {

        setCompletedSkills((prev) => [
          ...prev,
          skill
        ]);

      } else {

        setCompletedSkills((prev) =>
          prev.filter((item) => item !== skill)
        );

      }

    } catch (error) {

      console.log(error);
      alert("Error saving progress!");

    }
  }

  function downloadPDF() {

  const input =
    document.getElementById(
      "roadmap-content"
    );

  html2canvas(input).then(
    (canvas) => {

      const imgData =
        canvas.toDataURL("image/png");

      const pdf =
        new jsPDF(
          "p",
          "mm",
          "a4"
        );

      const imgWidth = 210;

      const pageHeight = 297;

      const imgHeight =
        (canvas.height * imgWidth)
        / canvas.width;

      let heightLeft =
        imgHeight;

      let position = 0;

      pdf.addImage(
        imgData,
        "PNG",
        0,
        position,
        imgWidth,
        imgHeight
      );

      heightLeft -= pageHeight;

      while (heightLeft > 0) {

        position =
          heightLeft - imgHeight;

        pdf.addPage();

        pdf.addImage(
          imgData,
          "PNG",
          0,
          position,
          imgWidth,
          imgHeight
        );

        heightLeft -= pageHeight;

      }

      pdf.save(
        `${company}_placement_roadmap.pdf`
      );

    }
  );
}

  const progressPercentage =
    result && result.missing_skills.length > 0
      ? Math.round(
          (
            completedSkills.length /
            result.missing_skills.length
          ) * 100
        )
      : 0;

  const filteredCompanies = companies.filter(
    (item) =>
      item.toLowerCase().includes(
        searchCompany.toLowerCase()
      )
  );

  return (

    <div
      className={
        darkMode
          ? "container dark-mode"
          : "container"
      }
    >

      <h1>
        AI Placement Preparation Assistant
      </h1>

      <button
        className="dark-mode-btn"
        onClick={() =>
          setDarkMode(!darkMode)
        }
      >
        {darkMode
          ? "☀️ Light Mode"
          : "🌙 Dark Mode"}
      </button>

      <label>Search Company:</label>

      <input
        type="text"
        placeholder="Search company..."
        value={searchCompany}
        onChange={(e) =>
          setSearchCompany(
            e.target.value
          )
        }
      />

      <label>Select Company:</label>

      <select
        value={company}
        onChange={(e) =>
          setCompany(
            e.target.value
          )
        }
      >

        {filteredCompanies.map(
          (item) => (

            <option
              key={item}
              value={item}
            >
              {item}
            </option>

          )
        )}

      </select>

      <label>
        Upload Resume (PDF):
      </label>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setResumeFile(
            e.target.files[0]
          )
        }
      />

      <button
        onClick={uploadResume}
      >
        Extract Skills
      </button>

      <label>
        Enter Your Skills:
      </label>

      <input
        type="text"
        placeholder="Example: Python, SQL"
        value={skills}
        onChange={(e) =>
          setSkills(
            e.target.value
          )
        }
      />

      <button
  onClick={generateRoadmap}
  disabled={loading}
>
  {loading
    ? "⏳ Generating AI Roadmap..."
    : "Generate Roadmap"}
</button>
{loading && (

  <div className="loading-text">

    ⏳ Please wait...
    AI is generating your personalized roadmap.

  </div>

)}
      

      {result && (

        <div
  id="roadmap-content"
  className="result-box"
>

          <h2>
  Progress Tracker
</h2>

<div className="progress-tracker">

  {result.missing_skills.map(
    (skill, index) => (

      <label key={index}>

        <input
          type="checkbox"
          checked={completedSkills.includes(
            skill
          )}
          onChange={(e) =>
            saveProgress(
              skill,
              e.target.checked
            )
          }
        />

        <span
          className={
            completedSkills.includes(
              skill
            )
              ? "completed-skill"
              : ""
          }
        >
          {skill}
        </span>

      </label>

    )
  )}

</div>

          <h3>
            Progress:
            {" "}
            {progressPercentage}%
          </h3>

          <div className="progress-bar-container">

            <div
              className="progress-bar"
              style={{
                width:
                  `${progressPercentage}%`
              }}
            ></div>

          </div>

          <button
            onClick={downloadPDF}
          >
            Download PDF
          </button>

<h2>Roadmap</h2>

<div className="roadmap-content">
  {result.roadmap.map((line, index) =>
    line.trim() ? (
      <p key={index}>{line}</p>
    ) : (
      <br key={index} />
    )
  )}
</div>

{result.missing_skills.length > 0 &&
  completedSkills.length ===
    result.missing_skills.length && (

    <h2>
      🎉 Congratulations!
      You completed your roadmap.
    </h2>

)}

        </div>

      )}

    </div>

  );
}

export default App;