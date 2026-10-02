import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { AlertCircle, Loader2, Sparkles } from "lucide-react";
import DropZone from "../components/DropZone";
import { uploadFiles } from "../utils/api";

const HRUpload = () => {
  const navigate = useNavigate();
  const [jobDescription, setJobDescription] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");

  const addResumes = (files) => {
    setResumes((prev) => {
      const seen = new Set(prev.map((f) => `${f.name}-${f.size}`));
      return [...prev, ...files.filter((f) => !seen.has(`${f.name}-${f.size}`))];
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setIsUploading(true);

    const formData = new FormData();
    formData.append("jobDescription", jobDescription);
    resumes.forEach((file) => formData.append("resumes", file));

    try {
      await uploadFiles(formData);
      navigate("/results");
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || "Upload failed. Please check the server and try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const canSubmit = jobDescription && resumes.length > 0 && !isUploading;

  return (
    <div className="mx-auto max-w-2xl animate-fade-in-up">
      <div className="mb-8 text-center">
        <h1 className="bg-gradient-to-r from-primary to-fuchsia-500 bg-clip-text text-4xl font-bold tracking-tight text-transparent">
          Find the best candidates, faster
        </h1>
        <p className="mt-3 text-slate-400">
          Upload a job description and a batch of resumes. Candidates are ranked by how well their skills match.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-8 rounded-2xl border border-white/10 bg-white/5 p-6 shadow-2xl backdrop-blur-md sm:p-8"
      >
        <DropZone
          id="jobDescription"
          label="1. Job description"
          hint="PDF only"
          accept=".pdf"
          files={jobDescription ? [jobDescription] : []}
          onFiles={(files) => setJobDescription(files[0])}
          onRemove={() => setJobDescription(null)}
        />

        <DropZone
          id="resumes"
          label="2. Candidate resumes"
          hint="PDF, DOC or DOCX - select multiple files"
          accept=".pdf,.doc,.docx"
          multiple
          files={resumes}
          onFiles={addResumes}
          onRemove={(index) => setResumes((prev) => prev.filter((_, i) => i !== index))}
        />

        {error && (
          <div role="alert" className="flex items-start gap-2 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
            <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={!canSubmit}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-primary to-fuchsia-600 px-4 py-3.5 font-medium text-white shadow-lg shadow-primary/20 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:brightness-100"
        >
          {isUploading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              Uploading and matching...
            </>
          ) : (
            <>
              <Sparkles className="h-5 w-5" />
              Match resumes
            </>
          )}
        </button>
        {!jobDescription || resumes.length === 0 ? (
          <p className="-mt-4 text-center text-xs text-slate-500">
            Add a job description and at least one resume to continue.
          </p>
        ) : null}
      </form>
    </div>
  );
};

export default HRUpload;
