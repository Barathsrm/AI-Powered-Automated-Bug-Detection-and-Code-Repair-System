import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { startAnalysis, getAnalysisStatus } from "../services/api";

export default function AnalysisPage() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState(null);

  useEffect(() => {
    let poll;
    async function begin() {
      if (!projectId) return;
      try {
        const analysis = await startAnalysis(projectId);
        poll = setInterval(async () => {
          const updated = await getAnalysisStatus(analysis.id);
          setStatus(updated);
          if (["success", "failed"].includes(updated.status)) {
            clearInterval(poll);
            navigate(`/diff/${analysis.id}`);
          }
        }, 2000);
      } catch (err) {
        console.error("Failed to start analysis", err);
      }
    }
    begin();
    return () => clearInterval(poll);
  }, [projectId, navigate]);

  return (
    <div>
      <h1>Analyzing project</h1>
      <p>Status: {status?.status ?? "starting..."}</p>
      <p>Attempt {status?.attempt_count ?? 0} of {status?.max_attempts ?? "?"}</p>
    </div>
  );
}
