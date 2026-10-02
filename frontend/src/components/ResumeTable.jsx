import React, { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ExternalLink, Search, Trophy, Users, TrendingUp, UploadCloud, Inbox } from "lucide-react";

const SORTS = {
  scoreDesc: { label: "Score: high to low", fn: (a, b) => b.score - a.score },
  scoreAsc: { label: "Score: low to high", fn: (a, b) => a.score - b.score },
  name: { label: "Name: A to Z", fn: (a, b) => a.filename.localeCompare(b.filename) },
};

const scoreStyle = (score) => {
  if (score >= 70) return { bar: "bg-emerald-500", text: "text-emerald-400" };
  if (score >= 40) return { bar: "bg-amber-500", text: "text-amber-400" };
  return { bar: "bg-red-500", text: "text-red-400" };
};

const toHref = (url) => (!url ? "#" : url.startsWith("http") ? url : `https://${url}`);

const Stat = ({ icon: Icon, label, value }) => (
  <div className="flex items-center gap-4 rounded-xl border border-white/10 bg-white/5 p-4">
    <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/15 text-primary">
      <Icon className="h-5 w-5" />
    </span>
    <div>
      <p className="text-xs text-slate-400">{label}</p>
      <p className="text-xl font-semibold">{value}</p>
    </div>
  </div>
);

const ResumeTable = ({ resumes }) => {
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("scoreDesc");

  const rows = useMemo(
    () =>
      resumes.map((r) => ({
        ...r,
        score: Number(r.matching_score) || 0,
        skills: Array.isArray(r.skills_matched) ? r.skills_matched : [],
      })),
    [resumes]
  );

  const stats = useMemo(() => {
    if (rows.length === 0) return { top: 0, avg: 0 };
    const scores = rows.map((r) => r.score);
    return {
      top: Math.max(...scores),
      avg: scores.reduce((a, b) => a + b, 0) / scores.length,
    };
  }, [rows]);

  // Rank is fixed by score so it stays stable while filtering or re-sorting.
  const ranks = useMemo(() => {
    const ordered = [...rows].sort(SORTS.scoreDesc.fn);
    return new Map(ordered.map((r, i) => [r._id ?? r.reference_id ?? r.filename, i + 1]));
  }, [rows]);

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    return rows
      .filter(
        (r) =>
          !q || r.filename.toLowerCase().includes(q) || r.skills.some((s) => s.toLowerCase().includes(q))
      )
      .sort(SORTS[sort].fn);
  }, [rows, query, sort]);

  return (
    <div className="animate-fade-in-up space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Matching results</h1>
          <p className="mt-1 text-slate-400">Candidates ranked by skill match with the job description.</p>
        </div>
        <Link
          to="/"
          className="flex items-center gap-2 rounded-lg bg-gradient-to-r from-primary to-fuchsia-600 px-4 py-2 text-sm font-medium text-white hover:brightness-110"
        >
          <UploadCloud className="h-4 w-4" /> New search
        </Link>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <Stat icon={Users} label="Candidates" value={rows.length} />
        <Stat icon={Trophy} label="Top score" value={`${stats.top.toFixed(1)}%`} />
        <Stat icon={TrendingUp} label="Average score" value={`${stats.avg.toFixed(1)}%`} />
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <div className="relative min-w-[220px] flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by name or skill"
            className="w-full rounded-lg border border-white/10 bg-white/5 py-2 pl-9 pr-3 text-sm placeholder:text-slate-500 focus:border-primary focus:outline-none"
          />
        </div>
        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          aria-label="Sort resumes"
          className="rounded-lg border border-white/10 bg-slate-900 px-3 py-2 text-sm focus:border-primary focus:outline-none"
        >
          {Object.entries(SORTS).map(([key, { label }]) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>
      </div>

      {visible.length === 0 ? (
        <div className="flex flex-col items-center gap-2 rounded-2xl border border-white/10 bg-white/5 py-16 text-slate-400">
          <Inbox className="h-10 w-10" />
          <p>{rows.length === 0 ? "No results yet." : "No candidates match your search."}</p>
        </div>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm">
          <table className="w-full min-w-[720px] text-left text-sm">
            <thead className="border-b border-white/10 text-xs uppercase tracking-wide text-slate-400">
              <tr>
                <th className="px-4 py-3 w-16">Rank</th>
                <th className="px-4 py-3">Candidate</th>
                <th className="px-4 py-3 w-56">Match score</th>
                <th className="px-4 py-3">Matched skills</th>
                <th className="px-4 py-3 w-28 text-right">Resume</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {visible.map((r) => {
                const key = r._id ?? r.reference_id ?? r.filename;
                const rank = ranks.get(key);
                const style = scoreStyle(r.score);
                return (
                  <tr key={key} className="transition-colors hover:bg-white/[0.04]">
                    <td className="px-4 py-3">
                      <span
                        className={`inline-flex h-7 w-7 items-center justify-center rounded-full text-xs font-semibold ${
                          rank === 1 ? "bg-amber-400/20 text-amber-300" : "bg-white/10 text-slate-300"
                        }`}
                      >
                        {rank}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-medium">{r.filename}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <div className="h-2 flex-1 overflow-hidden rounded-full bg-white/10">
                          <div
                            className={`h-full rounded-full ${style.bar}`}
                            style={{ width: `${Math.min(r.score, 100)}%` }}
                          />
                        </div>
                        <span className={`w-14 text-right font-semibold ${style.text}`}>{r.score.toFixed(1)}%</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      {r.skills.length === 0 ? (
                        <span className="text-slate-500">None</span>
                      ) : (
                        <div className="flex flex-wrap gap-1.5">
                          {r.skills.map((skill) => (
                            <span key={skill} className="rounded-full bg-primary/15 px-2 py-0.5 text-xs text-slate-200">
                              {skill}
                            </span>
                          ))}
                        </div>
                      )}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <a
                        href={toHref(r.url)}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-primary hover:underline"
                      >
                        View <ExternalLink className="h-3.5 w-3.5" />
                      </a>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ResumeTable;
