export default function ReportViewer({ report }) {
  if (!report) return null;
  return (
    <div>
      <pre style={{ whiteSpace: "pre-wrap" }}>{report.summary}</pre>
    </div>
  );
}
