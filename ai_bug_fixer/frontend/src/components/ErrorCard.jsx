export default function ErrorCard({ error }) {
  return (
    <div>
      <strong>{error.test}</strong>
      <div>{error.file_path}{error.line_number ? `:${error.line_number}` : ""}</div>
      <pre>{error.raw}</pre>
    </div>
  );
}
