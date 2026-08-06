export default function CodeDiffViewer({ diffLines }) {
  return (
    <div>
      {diffLines.map((line, i) => (
        <div
          key={i}
          style={{
            backgroundColor:
              line.type === "add" ? "#eaf3de" : line.type === "remove" ? "#faece7" : "transparent",
          }}
        >
          {line.text}
        </div>
      ))}
    </div>
  );
}
