import OpenAI from "openai";
import { NextResponse } from "next/server";

const openai = new OpenAI({
  baseURL: "https://models.inference.ai.azure.com",
  apiKey: process.env.OPENAI_API_KEY,
});

export const POST = async (req) => {
  try {
    const { input } = await req.json();

    //console.log("Received input:", input); 
    const openaiResponse = await openai.chat.completions.create({
      messages: [
        { role: "system", content: "" },
        { role: "user", content: input || "What is the capital of France?" },
      ],
      model: "gpt-4o", 
      temperature: 1,
      max_tokens: 4096,
      top_p: 1,
    });
    const openaiReply = openaiResponse.choices[0]?.message?.content || "No response from OpenAI.";

    //console.log("Response from OpenAI:", openaiReply); 
    return new NextResponse(
      JSON.stringify({ reply: openaiReply }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("Error handling request:", error.message || error); 

    return new NextResponse(
      JSON.stringify({ reply: "An error occurred. Please try again later." }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
};
