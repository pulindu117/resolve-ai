import { useState, useEffect } from "react";
import { listDocuments, uploadDocument, deleteDocument } from "../api/client";

export default function DocumentPanel() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);

  async function refresh() {
    try {
      const docs = await listDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error("Failed to load documents", err);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      await uploadDocument(file);
      await refresh();
    } catch (err) {
      alert("Upload failed. Check the file type and try again.");
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  }

  async function handleDelete(source) {
    try {
      await deleteDocument(source);
      await refresh();
    } catch (err) {
      alert("Delete failed.");
    }
  }

  return (
    <div className="w-80 border-l border-[#E5E4DE] bg-white flex flex-col">
      <div className="p-5 border-b border-[#E5E4DE]">
        <h2 className="text-sm font-semibold text-[#1A1A1A] mb-3">Knowledge base</h2>

        <label className="flex items-center justify-center gap-2 border border-dashed border-[#D3D2CA] rounded-xl py-3 text-sm text-[#8B8D98] cursor-pointer hover:border-[#4F46E5] hover:text-[#4F46E5] transition-colors">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M12 4V16M12 4L7 9M12 4L17 9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M4 17V19C4 20.1 4.9 21 6 21H18C19.1 21 20 20.1 20 19V17" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
          </svg>
          {uploading ? "Uploading..." : "Upload document"}
          <input
            type="file"
            accept=".pdf,.md,.markdown,.txt"
            onChange={handleFileChange}
            disabled={uploading}
            className="hidden"
          />
        </label>
      </div>

      <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-2">
        {documents.length === 0 && (
          <p className="text-sm text-[#8B8D98] text-center mt-8">No documents indexed yet.</p>
        )}

        {documents.map((doc) => (
          <div
            key={doc.source}
            className="flex items-center justify-between bg-[#FAFAF8] border border-[#E5E4DE] rounded-xl px-3 py-2.5"
          >
            <div className="min-w-0">
              <div className="font-medium text-sm text-[#1A1A1A] truncate">{doc.source}</div>
              <div className="text-[#8B8D98] text-xs">{doc.chunk_count} chunks</div>
            </div>
            <button
              onClick={() => handleDelete(doc.source)}
              className="text-[#B54545] hover:text-[#8F3535] text-xs font-medium flex-shrink-0 ml-2"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}