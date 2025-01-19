"use client";

import { useState, useEffect } from "react";
import { CopilotChat } from "@copilotkit/react-ui";

const Home = () => {
  const [questions, setQuestions] = useState([]);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("api/copilotkit/data");
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        setQuestions(data.questions || []);
        setResources(data.resources || []);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unknown error occurred");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="flex flex-col md:flex-row min-h-screen">
      <div className="flex-1 bg-white p-4 border-l border-gray-200">
        <h2 className="text-lg font-semibold mb-4">New Panel</h2>
        <p className="text-gray-600">
          This is the content for the new panel. You can add anything here, such
          as a dashboard, form, or any other content.
        </p>
      </div>
      <div className="flex-1 bg-gray-100 p-4">
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="text-red-500">Error: {error}</p>
        ) : (
          <>
            <h2 className="text-lg font-semibold mb-4">Agent Data</h2>
            <div className="mb-6">
              <h3 className="text-md font-semibold">Questions:</h3>
              <ul className="list-disc list-inside text-gray-700">
                {questions.length > 0 ? (
                  questions.map((q, index) => <li key={index}>{q}</li>)
                ) : (
                  <p>No questions available.</p>
                )}
              </ul>
            </div>
            <div>
              <h3 className="text-md font-semibold">Resources:</h3>
              <ul className="list-disc list-inside text-gray-700">
                {resources.length > 0 ? (
                  resources.map((r, index) => <li key={index}>{r}</li>)
                ) : (
                  <p>No resources available.</p>
                )}
              </ul>
            </div>
          </>
        )}
        <div className="mt-6">
          <CopilotChat
            instructions="You are assisting the user as best as you can. Answer in the best way possible given the data you have."
            labels={{
              title: "Your Assistant",
              initial: "Hi! 👋 How can I assist you today?",
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
