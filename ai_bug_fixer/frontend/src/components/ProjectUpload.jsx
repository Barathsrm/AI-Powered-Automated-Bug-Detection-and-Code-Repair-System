import { useState } from "react";
import { uploadProject } from "../services/api";

export default function ProjectUpload({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) return;
    setBusy(true);
    setError(null);
    try {
      const project = await uploadProject(file);
      onUploaded(project);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept=".zip"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button type="submit" disabled={!file || busy}>
        {busy ? "Uploading..." : "Upload project"}
      </button>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}
