"use client";
import { useState, useRef, useEffect } from "react";
import { IoMdSend } from "react-icons/io";
import { MdSettings } from "react-icons/md";

const Home = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! How can I help you?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (input.trim() === "") return;

    const userMessage = { id: Date.now(), text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    setTimeout(() => {
      const botMessage = {
        id: Date.now() + 1,
        text: `You said: "${input}"`,
        sender: "bot",
      };
      setMessages((prev) => [...prev, botMessage]);
    }, 1000);
  };

  return (
    <div className="h-screen bg-gray-600 flex flex-col items-center justify-center">
      <div className="w-full max-w-md h-full flex flex-col bg-gray-800 shadow-lg"><div className="flex items-center justify-between px-4 py-2 bg-gray-700 text-white shadow">
          <h1 className="text-lg font-semibold">Chat Application</h1>
          <button className="p-2 rounded-full hover:bg-gray-600">
            <MdSettings className="h-6 w-6 text-white" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto px-4 py-2 bg-gray-900">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              } mb-2`}
            >
              <p
                className={`px-4 py-2 rounded-lg ${
                  msg.sender === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-700 text-white"
                }`}
              >
                {msg.text}
              </p>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <form
          onSubmit={handleSend}
          className="flex items-center px-4 py-2 bg-gray-800 border-t border-gray-700"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="ml-2 p-2 rounded-full bg-blue-600 text-white hover:bg-blue-700"
          >
            <IoMdSend className="h-5 w-5" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default Home;
