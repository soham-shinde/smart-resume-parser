const mongoose = require("mongoose");

const ResultSchema = new mongoose.Schema({
  filename: { type: String, required: true },
  matching_score: { type: Number, required: true },
  skills_matched: { type: [String], required: true },
  reference_id: { type: String, required: true },
  url: { type: String, required: false },
});

module.exports = mongoose.model("Result", ResultSchema);
