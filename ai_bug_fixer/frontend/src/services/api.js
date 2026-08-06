const BASE_URL = import.meta.env.VITE_API_URL || "";

function authHeaders() {
  const token = localStorage.getItem("access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function uploadProject(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE_URL}/upload/`, {
    method: "POST",
    headers: authHeaders(),
    body: form,
  });
  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function startAnalysis(projectId) {
  const res = await fetch(`${BASE_URL}/analysis/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ project_id: projectId }),
  });
  if (!res.ok) throw new Error("Failed to start analysis");
  return res.json();
}

export async function getAnalysisStatus(analysisId) {
  const res = await fetch(`${BASE_URL}/analysis/${analysisId}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch analysis status");
  return res.json();
}

export async function getPatches(analysisId) {
  const res = await fetch(`${BASE_URL}/repair/${analysisId}/patches`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch patches");
  return res.json();
}

export async function approvePatch(patchId) {
  return fetch(`${BASE_URL}/repair/${patchId}/approve`, {
    method: "POST",
    headers: authHeaders(),
  });
}

export async function rejectPatch(patchId) {
  return fetch(`${BASE_URL}/repair/${patchId}/reject`, {
    method: "POST",
    headers: authHeaders(),
  });
}

export async function getReport(analysisId) {
  const res = await fetch(`${BASE_URL}/report/${analysisId}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch report");
  return res.json();
}
