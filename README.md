# Grammify

Grammify is an intelligent agentic chat application designed for learning and practicing languages. The application leverages cutting-edge technologies like FastAPI, LangGraph, and CopilotKit for building dynamic agents, combined with a modern frontend built using Next.js.

## Features

- Interactive chat-based language learning.
- Intelligent agents powered by LangGraph workflows.
- Seamless integration with CopilotKit for enhanced agent capabilities.
- Responsive and user-friendly frontend built with Next.js.
- Scalable backend powered by FastAPI.

## Installation

To get started with Grammify, follow these steps:

### Prerequisites

- Python 3.8 or later
- Node.js 16 or later
- npm or yarn

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/grammify.git
   cd grammify
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install backend dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies:**

   ```bash
   cd client
   npm install
   ```

5. **Start the development servers:**

   - **Backend:**
     ```bash
     uvicorn agent.main:app --reload
     ```

   - **Frontend:**
     ```bash
     cd client
     npm run dev
     ```

## Technologies Used

### Backend
- **FastAPI**: A modern, fast web framework for building APIs.
- **LangGraph**: Manages workflows for intelligent agent behavior.
- **CopilotKit**: Simplifies the creation of robust AI agents.

### Frontend
- **Next.js**: A React-based framework for building user interfaces.
- **Tailwind CSS**: For responsive and modern styling.

## Contributing

Contributions are welcome! Feel free to fork the repository, submit issues, or create pull requests.

## License

Grammify is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- The creators of FastAPI, LangGraph, CopilotKit, and Next.js.
- The open-source community for their contributions to modern development tools.

Happy learning with Grammify! 🌟

