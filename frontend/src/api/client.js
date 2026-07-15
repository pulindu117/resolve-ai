const BASE_URL = "http://localhost:8000";

export async function sendChatMessage(query, topK = 5) {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, top_k: topK }),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed: ${response.status}`);
  }

  return response.json();
}

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.status}`);
  }

  return response.json();
}

export async function listDocuments() {
  const response = await fetch(`${BASE_URL}/documents`);

  if (!response.ok) {
    throw new Error(`Failed to list documents: ${response.status}`);
  }

  return response.json();
}

export async function deleteDocument(source) {
  const response = await fetch(`${BASE_URL}/documents/${source}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Delete failed: ${response.status}`);
  }

  return response.json();
}