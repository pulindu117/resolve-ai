export default function Message({ role, content, sources }) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-5`}>
      <div className={`max-w-[70%] ${isUser ? "" : "flex flex-col items-start"}`}>
        <div
          className={`px-4 py-3 text-[15px] leading-relaxed ${
            isUser
              ? "bg-[#4F46E5] text-white rounded-2xl rounded-br-md"
              : "bg-white border border-[#E5E4DE] text-[#1A1A1A] rounded-2xl rounded-bl-md"
          }`}
        >
          <p className="whitespace-pre-wrap">{content}</p>
        </div>

        {!isUser && sources && sources.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-2 px-1">
            {sources.map((source, i) => (
              <span
                key={i}
                className="inline-flex items-center gap-1 text-xs px-2.5 py-1 rounded-full bg-[#EEF3EF] text-[#3F5F49] border border-[#D3E0D6]"
              >
                <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                  <path d="M2 5L4 7L8 3" stroke="#3F5F49" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                {source}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}