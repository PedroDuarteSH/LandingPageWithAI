import { HfInference } from "@huggingface/inference";
import { NextApiRequest, NextApiResponse } from "next";
import admin from "firebase-admin";
// Initialize Firebase Admin (Singleton pattern to prevent multiple initializations)
if (!admin.apps.length) {
    const serviceAccount = JSON.parse(process.env.FIREBASE_CREDENTIALS as string);
    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount),
    });
}

const HF_TOKEN = process.env.MY_SECRET_API_KEY; 

const inference = new HfInference(HF_TOKEN);

const db = admin.firestore();


export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== "POST") {
        return res.status(405).json({ success: false, message: "Method not allowed" });
    }

    try {
        const timestamp = new Date().toISOString();
        console.log(`\n--- New Request at ${timestamp} ---`);
        
        // Save request details in Firestore
        const logRef = await db.collection("chat_logs").add({
            timestamp,
            headers: req.headers,
            requestBody: req.body,
            responseBody: "",
        });

        let completeResponse = "";
        const stream = inference.chatCompletionStream(req.body);
        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");
        
        for await (const chunk of stream) {
            if (chunk.choices && chunk.choices.length > 0) {
                const newContent = chunk.choices[0].delta.content;
                console.log(newContent)
                res.write(newContent);
                completeResponse += newContent;
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                //(res as any).flush();
                await new Promise(resolve => setTimeout(resolve, 10));
            }
        }
        await logRef.update({ responseBody: completeResponse });
        res.end();
    } catch (error) {
        console.error("Error in handler:", error);
        res.status(500).json({ success: false, message: "Failed to load model output" });
    }
}