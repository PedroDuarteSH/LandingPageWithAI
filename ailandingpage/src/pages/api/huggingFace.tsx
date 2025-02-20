import { HfInference } from "@huggingface/inference";
import { NextApiRequest, NextApiResponse } from "next";

const HF_TOKEN = process.env.MY_SECRET_API_KEY; 

const inference = new HfInference(HF_TOKEN);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== "POST") {
        return res.status(405).json({ success: false, message: "Method not allowed" });
    }

    try {

        const stream = inference.chatCompletionStream(req.body);
        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");
        
        for await (const chunk of stream) {
            if (chunk.choices && chunk.choices.length > 0) {
                const newContent = chunk.choices[0].delta.content;
                console.log(newContent)
                res.write(newContent);
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                (res as any).flush();
            }
        }

        res.end();
    } catch (error) {
        console.error("Error in handler:", error);
        res.status(500).json({ success: false, message: "Failed to load model output" });
    }
}