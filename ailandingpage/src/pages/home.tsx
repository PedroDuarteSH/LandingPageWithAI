"use client"
import React, { useState, useCallback, useRef, useEffect } from "react";
import "./home.css";
import { initialMessages } from "@/docs/initialMessages";
import UserInput from "@/Components/Input/userInput";
import MessageList from "@/Components/Messenger/messageList";
import BoxTitle from "@/Components/MessagerTitle/boxtitle";

export interface Message {
    role: "user" | "assistant" | "system" | "context";
    content: string;
    show: boolean;
}


export default function Home() {
    const [userMessageSignal, setUserMessageSignal] = useState<boolean>(false); //False when user sent a message, true when it sends -> Goes to false if user wants to stop the generation
    const [modelGenerating, setModelGenerating] = useState<boolean>(false)
    const [messages, setMessages] = useState<Message[]>(initialMessages);


    const userMessageSignalRef = useRef(userMessageSignal);

    useEffect(() => {
        userMessageSignalRef.current = userMessageSignal;
    }, [userMessageSignal]);

    const handleClick = useCallback(async (question: string) => {
        try {
            if (userMessageSignal) {
                setUserMessageSignal(false);
                return;
            };

            //Start Processing
            setUserMessageSignal(true);
            setModelGenerating(true);
            const new_Message_set : Message[] = [{ role: "user", content: question, show: true }, ...messages]
            //Add User Message
            setMessages(new_Message_set);
            console.log(new_Message_set)

            const response = await fetch("/api/huggingFace", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                /*
                body: JSON.stringify({
                    model: "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
                    messages: messages.slice().reverse(),
                    max_tokens: 512,
                    provider: "hf-inference",
                }),*/
                body: JSON.stringify({
                    model: "meta-llama/Llama-3.2-3B-Instruct",
                    messages: new_Message_set.slice(0).reverse(),
                    max_tokens: 512,
                    stream: true,
                    provider: "hf-inference",
                }),

            })

            if (!response.ok) {
                throw new Error("Failed to fetch response");
            }
            console.log("Response ok")


            const reader = response.body?.getReader();
            if (!reader) {
                throw new Error("Failed to read stream");
            }
            console.log("Reader Loaded")

            let accumulatedContent = ""
            while (true) {
                console.log(userMessageSignalRef.current)
                if (userMessageSignalRef.current === false) {
                    reader.cancel()
                    break
                }


                const { done, value } = await reader.read();
                if (done) break;

                const chunk = new TextDecoder().decode(value);
                accumulatedContent += chunk;

                // Update the assistant's message in the chat history
                setMessages((prev) => {
                    if (prev.length > 0 && prev[0].role === "assistant") {
                        return [
                            { ...prev[0], content: accumulatedContent, show: true },
                            ...prev.slice(1),
                        ];
                    }
                    return [{ role: "assistant", content: accumulatedContent, show: true }, ...prev];
                });
            }
        } catch (error) {
            console.error("Error calling API:", error);
        } finally {
            setUserMessageSignal(false);
            setModelGenerating(false)
        }
    }, [userMessageSignal]);



    return (
        <div className="home-container">
            <BoxTitle />
            <MessageList messages={messages} />
            <UserInput modelGenerating={modelGenerating} handleSubmit={handleClick} />
        </div>
    );
}
