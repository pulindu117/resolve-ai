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
    <div className="w-72 border-l p-4 flex flex-col gap-4">
      <div>
        <h2 className="font-semibold mb-2">Knowledge Base</h2>
        <input
          type="file"
          accept=".pdf,.md,.markdown,.txt"
          onChange={handleFileChange}
          disabled={uploading}
          className="text-sm"
        />
        {uploading && <p className="text-xs text-gray-400 mt-1">Uploading...</p>}
      </div>

      <div className="flex flex-col gap-2">
        {documents.length === 0 && (
          <p className="text-sm text-gray-400">No documents indexed yet.</p>
        )}

        {documents.map((doc) => (
          <div
            key={doc.source}
            className="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2 text-sm"
          >
            <div>
              <div className="font-medium">{doc.source}</div>
              <div className="text-gray-400 text-xs">{doc.chunk_count} chunks</div>
            </div>
            <button
              onClick={() => handleDelete(doc.source)}
              className="text-red-500 hover:text-red-700 text-xs"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}