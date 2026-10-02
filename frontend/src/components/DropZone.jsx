import  { useState } from "react";
import { UploadCloud, FileText, X } from "lucide-react";

const formatSize = (bytes) => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const DropZone = ({ id, label, hint, accept, multiple = false, files, onFiles, onRemove }) => {
  const [dragging, setDragging] = useState(false);
  const allowed = accept.split(",").map((ext) => ext.trim().toLowerCase());

  const pick = (fileList) => {
    const picked = Array.from(fileList).filter((file) =>
      allowed.some((ext) => file.name.toLowerCase().endsWith(ext))
    );
    if (picked.length > 0) onFiles(multiple ? picked : picked.slice(0, 1));
  };

  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <label htmlFor={id} className="text-sm font-medium text-slate-200">
          {label}
        </label>
        {files.length > 0 && (
          <span className="rounded-full bg-primary/15 px-2 py-0.5 text-xs text-primary-foreground/80">
            {files.length} selected
          </span>
        )}
      </div>

      <label
        htmlFor={id}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          pick(e.dataTransfer.files);
        }}
        className={`flex cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed px-4 py-8 text-center transition-colors ${
          dragging
            ? "border-primary bg-primary/10"
            : "border-white/15 bg-white/[0.03] hover:border-primary/60 hover:bg-white/[0.06]"
        }`}
      >
        <UploadCloud className={`h-8 w-8 ${dragging ? "text-primary" : "text-slate-400"}`} />
        <p className="text-sm font-medium">
          Drop {multiple ? "files" : "a file"} here or <span className="text-primary">browse</span>
        </p>
        <p className="text-xs text-slate-400">{hint}</p>
        <input
          id={id}
          type="file"
          accept={accept}
          multiple={multiple}
          className="sr-only"
          onChange={(e) => {
            pick(e.target.files);
            e.target.value = "";
          }}
        />
      </label>

      {files.length > 0 && (
        <ul className="mt-3 max-h-48 space-y-1.5 overflow-y-auto pr-1">
          {files.map((file, index) => (
            <li
              key={`${file.name}-${file.size}-${index}`}
              className="flex items-center gap-3 rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm"
            >
              <FileText className="h-4 w-4 shrink-0 text-primary" />
              <span className="truncate">{file.name}</span>
              <span className="ml-auto shrink-0 text-xs text-slate-400">{formatSize(file.size)}</span>
              <button
                type="button"
                onClick={() => onRemove(index)}
                aria-label={`Remove ${file.name}`}
                className="shrink-0 rounded p-1 text-slate-400 transition-colors hover:bg-white/10 hover:text-white"
              >
                <X className="h-4 w-4" />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DropZone;
