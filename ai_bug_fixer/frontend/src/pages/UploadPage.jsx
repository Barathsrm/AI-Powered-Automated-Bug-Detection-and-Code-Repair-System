import { useNavigate } from "react-router-dom";
import ProjectUpload from "../components/ProjectUpload";

export default function UploadPage() {
  const navigate = useNavigate();

  function handleUploaded(project) {
    navigate(`/analysis/${project.id}`);
  }

  return (
    <div>
      <h1>Upload a project</h1>
      <ProjectUpload onUploaded={handleUploaded} />
    </div>
  );
}
