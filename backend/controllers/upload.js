const fs = require("fs/promises");
const path = require("path");
const Resume = require("../models/Resume");
const Result = require("../models/result");
const JD = require("../models/jd");
const { UPLOAD_DIR } = require("../multer");

// Remove previous records and files, keeping the files from the current request
const clearOldData = async (keepFilenames) => {
  await Promise.all([Resume.deleteMany({}), JD.deleteMany({}), Result.deleteMany({})]);

  const files = await fs.readdir(UPLOAD_DIR);
  await Promise.all(
    files
      .filter((f) => !keepFilenames.has(f))
      .map((f) => fs.rm(path.join(UPLOAD_DIR, f), { force: true }))
  );
};

const fileUrl = (req, file) =>
  `${req.protocol}://${req.get("host")}/upload/${encodeURIComponent(file.filename)}`;

// Upload Resumes and Job Description
const uploadFiles = async (req, res) => {
  const resumes = req.files.resumes;
  const jobDescriptionFile = req. files.jobDescription?.[0];

  if (!resumes || resumes.length === 0) {
    console.error("No resumes uploaded.");
    return res.status(400).json({ message: "No resumes uploaded." });
  }

  if (!jobDescriptionFile) {
    console.error("No job description file uploaded.");
    return res.status(400).json({ message: "No job description file uploaded." });
  }

  try {
    const uploadedResumes = [];

    await clearOldData(
      new Set([jobDescriptionFile.filename, ...resumes.map((f) => f.filename)])
    );

    // Save the job description in the "jd" collection
    const savedJD = await JD.create({
      filename: jobDescriptionFile.originalname,
      contentType: jobDescriptionFile.mimetype,
      url: fileUrl(req, jobDescriptionFile),
      public_id: jobDescriptionFile.filename,
    });

    const jobDescription = {
      filename: savedJD.filename,
      contentType: savedJD.contentType,
      url: savedJD.url,
      public_id: savedJD.public_id,
    };

    // Save each resume metadata
    for (const file of resumes) {
      const newResume = new Resume({
        jobDescription: jobDescription.url,
        filename: file.originalname,
        contentType: file.mimetype,
        url: fileUrl(req, file),
        public_id: file.filename, // Stored filename in /upload
      });

      const savedResume = await newResume.save();
      uploadedResumes.push(savedResume);
    }

    res.status(200).json({
      message: "Files uploaded successfully!",
      jobDescription,
      resumes: uploadedResumes,
    });
  } catch (error) {
    console.log(error);
    
    console.error("Error during upload process:", error.message);
    res.status(500).json({
      message: "Error uploading files",
      error: error.message,
    });
  }
};

module.exports = {
  uploadFiles,
};
