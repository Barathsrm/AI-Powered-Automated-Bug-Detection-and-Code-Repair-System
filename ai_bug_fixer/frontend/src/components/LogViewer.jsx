export default function LogViewer({ logs }) {
  return (
    <pre style={{ whiteSpace: "pre-wrap", fontFamily: "monospace" }}>
      {logs || "No logs yet."}
    </pre>
  );
}
