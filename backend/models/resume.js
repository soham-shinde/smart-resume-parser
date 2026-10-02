const mongoose = require('mongoose');

const ResumeSchema = new mongoose.Schema(
  {
    jobDescription: {
      type: String, // Updated to store URL of the uploaded job description PDF
      required: true,
    },
    filename: {
      type: String,
      required: true,
    },
    contentType: {
      type: String,
      required: true,
    },
    url: {
      type: String, // URL of the file served from /upload
      required: true,
    },
    public_id: {
      type: String, // Stored filename in the upload folder
      required: true,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Resume', ResumeSchema);
