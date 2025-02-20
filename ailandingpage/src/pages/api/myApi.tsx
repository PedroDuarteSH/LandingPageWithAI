import { NextApiRequest, NextApiResponse } from "next";



export function processChunk(chunk : string){
    
    const  individual_chunks = chunk.split("data: ").splice(1);
    let gathered_content = "";
    console.log(individual_chunks)
    for(const c of individual_chunks){
        console.log(c)
        const chunkJson = JSON.parse(c);
        if(chunkJson["delta"]["content"]){
            gathered_content += chunkJson["delta"]["content"]
        }
    }
    
    return gathered_content;
}


export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== "POST") {
        return res.status(405).json({ success: false, message: "Method not allowed" });
    }

    try {
        const response = await fetch("http://localhost:5000/stream", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(req.body)
        })
        if (!response.ok) {
            throw new Error("Failed to get completions from the external API");
        }

        
        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");
        
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (reader) {
            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    break;
                }
                const chunk = decoder.decode(value, { stream: true });
                res.write(processChunk(chunk));
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