import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getReport } from "../services/api";
import ReportViewer from "../components/ReportViewer";

export default function ReportPage() {
  const { analysisId } = useParams();
  const [report, setReport] = useState(null);

  useEffect(() => {
    getReport(analysisId).then(setReport);
  }, [analysisId]);

  return (
    <div>
      <h1>Report</h1>
      <ReportViewer report={report} />
    </div>
  );
}
