import mongoose from "mongoose";
import dotenv from "dotenv";
import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import Resume from "./models/Resume.js";  // Update the path based on your project structure
import Result from "./models/result.js";  // Update the path based on your project structure

dotenv.config();

const UPLOAD_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), "upload");

// Connect to MongoDB
mongoose
  .connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("MongoDB connection error:", err));

async function deleteUploadedFiles() {
  try {
    const files = await fs.readdir(UPLOAD_DIR);
    await Promise.all(files.map((f) => fs.rm(path.join(UPLOAD_DIR, f), { force: true })));
    console.log(`${files.length} uploaded files deleted`);
  } catch (error) {
    if (error.code === "ENOENT") return;
    console.error("Error deleting uploaded files:", error);
  }
}

async function deleteMongoData() {
  try {
    // Delete all documents from the "resumes" collection
    const resumeDelete = await Resume.deleteMany({});
    console.log(`${resumeDelete.deletedCount} resumes deleted`);

    // Delete all documents from the "results" collection
    const resultDelete = await Result.deleteMany({});
    console.log(`${resultDelete.deletedCount} results deleted`);
  } catch (error) {
    console.error("Error deleting MongoDB data:", error);
  }
}

async function cleanUp() {
  await deleteUploadedFiles();
  await deleteMongoData();
  mongoose.connection.close(); // Close MongoDB connection after completion
  console.log("Cleanup process completed.");
}

// Run the cleanup process
cleanUp();