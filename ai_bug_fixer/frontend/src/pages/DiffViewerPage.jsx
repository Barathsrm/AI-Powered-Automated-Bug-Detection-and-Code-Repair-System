import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getPatches, approvePatch, rejectPatch } from "../services/api";
import CodeDiffViewer from "../components/CodeDiffViewer";

export default function DiffViewerPage() {
  const { analysisId } = useParams();
  const navigate = useNavigate();
  const [patches, setPatches] = useState([]);

  useEffect(() => {
    getPatches(analysisId).then(setPatches);
  }, [analysisId]);

  async function handleDecision(patchId, approve) {
    await (approve ? approvePatch(patchId) : rejectPatch(patchId));
    navigate(`/report/${analysisId}`);
  }

  return (
    <div>
      <h1>Review changes</h1>
      {patches.map((p) => (
        <div key={p.id}>
          <h2>{p.file_path}</h2>
          <p>{p.explanation}</p>
          <CodeDiffViewer diffLines={[{ type: "context", text: p.diff }]} />
          <button onClick={() => handleDecision(p.id, true)}>Approve &amp; apply</button>
          <button onClick={() => handleDecision(p.id, false)}>Reject / manual edit</button>
        </div>
      ))}
    </div>
  );
}
