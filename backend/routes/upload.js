const express = require("express");
const router = express.Router();
const { uploadFiles } = require("../controllers/upload");
const upload = require("../multer"); // Multer middleware

// route for uploading resumes and job description
router.post("/upload", upload.fields([{ name: "resumes", maxCount: 50 }, { name: "jobDescription", maxCount: 1 }]), uploadFiles);

module.exports = router;
