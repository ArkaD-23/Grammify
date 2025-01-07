"use client";
import { useState, useRef, useEffect } from "react";
import { IoMdSend } from "react-icons/io";

const Home = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! How can I help you?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false); 
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (input.trim() === "") return; 
    const userMessage = { id: Date.now(), text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsSending(true); 

    try {
      console.log("Sending message:", input); 

      const response = await fetch("/api/copilotkit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ input }),
      });

      if (!response.ok) {
        console.error("Failed to fetch response from the server. Status:", response.status); 
        throw new Error("Failed to fetch response from the server.");
      }

      const { reply } = await response.json();
      console.log("Received reply from server:", reply); // Debugging: log the reply received

      const botMessage = { id: Date.now() + 1, text: reply, sender: "bot" };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error in handleSend:", error); 
      const errorMessage = {
        id: Date.now() + 1,
        text: "Something went wrong. Please try again.",
        sender: "bot",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsSending(false); 
    }
  };

  return (
    <div className="h-screen bg-gray-600 flex flex-col items-center justify-center">
      <div className="w-full max-w-md h-full flex flex-col bg-gray-800 shadow-lg">
        <div className="flex items-center justify-between px-4 py-2 bg-gray-700 text-white shadow">
          <h1 className="text-lg font-semibold">Chat Application</h1>
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
            disabled={isSending} 
          >
            <IoMdSend className="h-5 w-5" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default Home;
