const mongoose = require("mongoose");

const JDSchema = new mongoose.Schema(
  {
    filename: { type: String, required: true },
    contentType: { type: String, required: true },
    url: { type: String, required: true },
    public_id: { type: String, required: true }, // Stored filename in the upload folder
  },
  { timestamps: true, collection: "jd" }
);

module.exports = mongoose.model("JD", JDSchema);
