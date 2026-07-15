import { useState, useRef, useEffect } from "react";
import Message from "./Message";
import { sendChatMessage } from "../api/client";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    const query = input.trim();
    if (!query || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setInput("");
    setLoading(true);

    try {
      const result = await sendChatMessage(query);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: result.answer, sources: result.sources },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Something went wrong. Try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto px-8 py-6">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-12 h-12 rounded-xl bg-[#EEF3EF] flex items-center justify-center mb-3">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#3F5F49" strokeWidth="1.5" strokeLinejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="#3F5F49" strokeWidth="1.5" strokeLinejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="#3F5F49" strokeWidth="1.5" strokeLinejoin="round"/>
              </svg>
            </div>
            <p className="text-[#1A1A1A] font-medium text-[15px]">Ask about your knowledge base</p>
            <p className="text-[#8B8D98] text-sm mt-1">Answers are grounded in your uploaded documents</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <Message key={i} role={msg.role} content={msg.content} sources={msg.sources} />
        ))}

        {loading && (
          <div className="flex justify-start mb-5">
            <div className="bg-white border border-[#E5E4DE] rounded-2xl rounded-bl-md px-4 py-3 flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#D97B2C] animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="w-1.5 h-1.5 rounded-full bg-[#D97B2C] animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="w-1.5 h-1.5 rounded-full bg-[#D97B2C] animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="border-t border-[#E5E4DE] p-4 flex gap-2 bg-white">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question..."
          rows={1}
          className="flex-1 resize-none border border-[#E5E4DE] rounded-xl px-4 py-2.5 text-[15px] focus:outline-none focus:ring-2 focus:ring-[#4F46E5] focus:border-transparent"
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-[#4F46E5] hover:bg-[#4338CA] text-white px-5 py-2.5 rounded-xl text-sm font-medium disabled:opacity-40 transition-colors"
        >
          Send
        </button>
      </div>
    </div>
  );
}