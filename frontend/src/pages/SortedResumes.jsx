import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AlertCircle, Loader2, RefreshCw, UploadCloud } from "lucide-react";
import { fetchMatchingScores } from "../utils/api";
import ResumeTable from "../components/ResumeTable";

const SortedResumes = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await fetchMatchingScores();
      setResumes(data.data || []);
    } catch (err) {
      console.error("Error fetching resumes:", err);
      setError("Could not load matching scores. Make sure the backend and Python services are running.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) {
    return (
      <div className="flex flex-col items-center gap-4 py-24 text-slate-400">
        <Loader2 className="h-10 w-10 animate-spin text-primary" />
        <p>Analyzing resumes and calculating scores...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-md rounded-2xl border border-red-500/30 bg-red-500/10 p-8 text-center">
        <AlertCircle className="mx-auto h-10 w-10 text-red-400" />
        <p className="mt-3 text-sm text-red-200">{error}</p>
        <div className="mt-5 flex justify-center gap-3">
          <button
            onClick={load}
            className="flex items-center gap-2 rounded-lg bg-white/10 px-4 py-2 text-sm hover:bg-white/20"
          >
            <RefreshCw className="h-4 w-4" /> Retry
          </button>
          <Link to="/" className="flex items-center gap-2 rounded-lg px-4 py-2 text-sm text-slate-300 hover:text-white">
            <UploadCloud className="h-4 w-4" /> Back to upload
          </Link>
        </div>
      </div>
    );
  }

  return <ResumeTable resumes={resumes} />;
};

export default SortedResumes;
