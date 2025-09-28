// src/app/ai-chat/page.tsx

"use client";

import React, { useState, FormEvent, useRef, useEffect } from "react";
import { PaperAirplaneIcon } from "@heroicons/react/24/outline";
import { motion, AnimatePresence } from "framer-motion";

const AiChatPage = () => {
  const [messages, setMessages] = useState<
    { role: "user" | "ai"; content: string }[]
  >([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const sendMessage = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: "user" as const, content: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input.trim();
    setInput("");
    setIsLoading(true);

    // Mock AI response
    setTimeout(() => {
      const aiMessage = {
        role: "ai" as const,
        content: `Echo: "${currentInput}" 🤖`,
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 md:px-8 pt-4 space-y-6 max-w-3xl w-full mx-auto">
        {/* Empty state */}
        {messages.length === 0 && !isLoading && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <h1 className="text-3xl font-bold mb-2 text-gray-800 dark:text-gray-100">
              AI Assistant
            </h1>
            <p className="text-gray-500 dark:text-gray-400">
              Type below to start chatting
            </p>
          </div>
        )}

        {/* Message list */}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-xl p-4 rounded-xl shadow-md ${
                msg.role === "user"
                  ? "bg-teal-600 text-white rounded-br-none"
                  : "bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 rounded-tl-none"
              }`}
            >
              <p className="font-semibold text-xs opacity-70 mb-1">
                {msg.role === "user" ? "You" : "Agent"}
              </p>
              <p>{msg.content}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="p-3 rounded-lg bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 animate-pulse">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <AnimatePresence initial={false}>
        <motion.div
          key={messages.length === 0 ? "center" : "bottom"}
          initial={{ y: messages.length === 0 ? 0 : 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: messages.length === 0 ? 0 : 100, opacity: 0 }}
          transition={{ duration: 0.4, ease: "easeInOut" }}
          className={`${
            messages.length === 0
              ? "absolute inset-0 flex items-center justify-center"
              : "sticky bottom-0 border-t border-gray-200 dark:border-gray-700"
          } bg-gray-50 dark:bg-gray-900 p-4`}
        >
          <form
            onSubmit={sendMessage}
            className="max-w-3xl w-full mx-auto flex items-end bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700"
          >
            {/* Auto-growing textarea */}
            <textarea
              value={input}
              onChange={(e) => {
                setInput(e.target.value);
                e.currentTarget.style.height = "auto";
                e.currentTarget.style.height = `${e.currentTarget.scrollHeight}px`;
              }}
              placeholder="Message your AI assistant..."
              rows={1}
              className="flex-1 resize-none p-4 bg-transparent focus:outline-none dark:text-gray-100 placeholder-gray-500 max-h-40 overflow-y-auto"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="p-3 m-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:bg-teal-400 transition-colors"
              disabled={isLoading || !input.trim()}
            >
              <PaperAirplaneIcon className="h-5 w-5 -rotate-45" />
            </button>
          </form>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

export default AiChatPage;
