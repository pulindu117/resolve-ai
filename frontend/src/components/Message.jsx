export default function Message({ role, content, sources }) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 ${
          isUser ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-900"
        }`}
      >
        <p className="whitespace-pre-wrap">{content}</p>

        {sources && sources.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-300 text-xs text-gray-500">
            Sources: {sources.join(", ")}
          </div>
        )}
      </div>
    </div>
  );
}