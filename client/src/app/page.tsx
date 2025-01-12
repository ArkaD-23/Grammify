"use client";
import { CopilotChat } from "@copilotkit/react-ui";

const Home = () => {
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
        <CopilotChat
          instructions="You are assisting the user as best as you can. Answer in the best way possible given the data you have."
          labels={{
            title: "Your Assistant",
            initial: "Hi! 👋 How can I assist you today?",
          }}
        />
      </div>
    </div>
  );
};

export default Home;
