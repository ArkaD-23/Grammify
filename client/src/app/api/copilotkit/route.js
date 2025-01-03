import {
    CopilotRuntime,
    OpenAIAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
    langGraphPlatformEndpoint, 
    copilotKitEndpoint,
  } from "@copilotkit/runtime";
  import OpenAI from "openai";

  const openai = new OpenAI({
    baseURL: "https://models.inference.ai.azure.com",
    apiKey: process.env.OPENAI_API_KEY
  })
  const llmAdapter = new OpenAIAdapter({ openai });
  const langsmithApiKey = process.env.LANGSMITH_API_KEY;
  
  export const POST = async (req) => {
    const searchParams = req.nextUrl.searchParams;
    const deploymentUrl = searchParams.get('lgcDeploymentUrl') || process.env.LGC_DEPLOYMENT_URL;
  
    const remoteEndpoint = deploymentUrl ? langGraphPlatformEndpoint({
      deploymentUrl,
      langsmithApiKey,
      agents: [
        {
          name: "research_agent",
          description: "Research agent",
        },
        {
          name: "research_agent_google_genai",
          description: "Research agent",
          assistantId: "9dc0ca3b-1aa6-547d-93f0-e21597d2011c",
        },
      ],
    }) : copilotKitEndpoint({
      url: process.env.REMOTE_ACTION_URL || "http://localhost:8000/copilotkit",
    });
  
    const runtime = new CopilotRuntime({
      remoteEndpoints: [remoteEndpoint],
    });
  
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
      runtime,
      serviceAdapter: llmAdapter,
      endpoint: "/api/copilotkit",
    });
  
    return handleRequest(req);
  };
  