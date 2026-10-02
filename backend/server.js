const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const { UPLOAD_DIR } = require("./multer");
const axios = require("axios"); // Import axios for HTTP requests
const connectDB = require("./config/db"); // Database connection
const uploadRoutes = require("./routes/upload"); // Upload routes
const Resume = require("./models/Resume"); // Import Resume model
const Result = require("./models/result"); // Import Result model
const JD = require("./models/jd"); // Import JD model

dotenv.config(); // Load environment variables

const app = express();

// MongoDB connection
connectDB();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve uploaded files
app.use("/upload", express.static(UPLOAD_DIR));

// Routes
app.use("/api", uploadRoutes);

// API Endpoint to get resumes
app.get("/resumes", async (req, res) => {
  try {
    // Fetch resumes with only the jobDescription, url, and filename fields
    const resumes = await Resume.find({}, "jobDescription url filename");
    res.json(resumes); // Send the filtered resume metadata as JSON
  } catch (err) {
    console.error("Error retrieving resumes:", err);
    res.status(500).send("Error retrieving resumes");
  }
});

// API Endpoint to get the most recently uploaded job description
app.get("/jd/latest", async (req, res) => {
  try {
    const jd = await JD.findOne().sort({ createdAt: -1 });
    if (!jd) return res.status(404).json({ message: "No job description found" });
    res.json(jd);
  } catch (err) {
    console.error("Error retrieving job description:", err);
    res.status(500).send("Error retrieving job description");
  }
});

// API Endpoint to get matching scores from Python API and store in MongoDB
app.get("/matching-scores", async (req, res) => {
  try {
    // Call the Python API
    const pythonApiUrl = "http://localhost:5001/calculate-matching-scores"; // Replace with your Python API endpoint
    const response = await axios.post(pythonApiUrl);

    console.log("Received response from Python API:", response.data); // Log response data

    // Store the results in MongoDB
    const results = response.data; // Python API should return an array
    console.log("Results to be saved:", results);

    await Result.deleteMany({}); // Avoid duplicate results on repeated calls
    await Result.insertMany(results); // Insert results into MongoDB

    // Fetch sorted results (descending order by matching_score)
    const sortedResults = await Result.find({}).sort({ matching_score: -1 });

    // Send sorted results as a response
    res.json({ message: "Matching scores stored and sorted successfully", data: sortedResults });
  } catch (err) {
    console.error("Error fetching or storing matching scores:", err.response ? err.response.data : err.message);
    res.status(500).send("Error fetching or storing matching scores");
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
