import type { NextApiRequest, NextApiResponse } from 'next';

// API base URL
//const API_BASE_URL = 'https://api.ai21.com/studio/v1/answer';

export interface APIResponse{
    id: string;
    answerInContext: boolean;
    answer: string;
}

let count = 0;

export function get_API() {
    return {
        "id": "8f12737c-11f6-4b84-43c7-e73f712aa80b",
        "answerInContext": true,
        "answer": "Pedro Henriques is from Coimbra, Portugal. " + count++,
        
      };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    try {
        console.log(req.body)
        res.status(200).json({
            "id": "8f12737c-11f6-4b84-43c7-e73f712aa80b",
            "answerInContext": true,
            "answer": "Pedro Henriques is from Coimbra, Portugal." + count++
          });

        /*
        // Retrieve the API key from environment variables
        console.log("Here   1")
        const apiKey = process.env.MY_SECRET_API_KEY;

        if (!apiKey) {
            throw new Error('API key is missing');
        }

        // Make the request to the external API
        const response = await fetch(API_BASE_URL, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(req.body)  // Forward client request body
        });

        // Check if response is ok
        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }

        const data = await response.json();
        res.status(response.status).json(data);*/
    } catch (error) {
        console.error('Error in API proxy:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
}

