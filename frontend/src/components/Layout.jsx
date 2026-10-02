import React from "react";
import { Link, useLocation } from "react-router-dom";
import { FileSearch } from "lucide-react";
import BackgroundSVG from "./BackgroundSVG";

const steps = [
  { path: "/", label: "Upload" },
  { path: "/results", label: "Results" },
];

const Layout = ({ children }) => {
  const { pathname } = useLocation();

  return (
    <div className="relative min-h-screen text-slate-100">
      <BackgroundSVG />

      <header className="border-b border-white/10 backdrop-blur-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <Link to="/" className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-fuchsia-600">
              <FileSearch className="h-5 w-5 text-white" />
            </span>
            <span className="text-lg font-semibold tracking-tight">Resume Matcher</span>
          </Link>

          <nav className="flex items-center gap-2 text-sm">
            {steps.map((step, index) => {
              const active = pathname === step.path;
              return (
                <Link
                  key={step.path}
                  to={step.path}
                  className={`flex items-center gap-2 rounded-full px-3 py-1.5 transition-colors ${
                    active ? "bg-white/10 text-white" : "text-slate-400 hover:text-white"
                  }`}
                >
                  <span
                    className={`flex h-5 w-5 items-center justify-center rounded-full text-xs ${
                      active ? "bg-primary text-white" : "bg-white/10"
                    }`}
                  >
                    {index + 1}
                  </span>
                  {step.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-10">{children}</main>
    </div>
  );
};

export default Layout;
