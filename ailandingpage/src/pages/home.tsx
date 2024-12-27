"use client";
import React, { useState } from "react";
import { APIResponse } from "./api/llm";
import "./home.css";
import TypewriterEffect from "@/Components/Effects/typewritereffect";

import UserInput from "@/Components/Input/userInput";

export default function Home() {
    const [response, setResponse] = useState<string>("");
    const [question, setQuestion] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [writing, setWriting] = useState<boolean>(false);
   

    const processResponse = (data: APIResponse) => {
        data.answer ? setResponse(data.answer) : setResponse("No answer found");
    };

    const handleClick = async () => {
        try {
            setWriting(true);
            setLoading(true);
            setQuestion("");
            const res = await fetch("/api/llm", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    context:
                        "Pedro Henriques is from Coimbra, Portugal. He is a software engineer and a student at the University of Coimbra. He is currently working on a personal website using AI.",
                    question: question,
                }),
            });

            const data = await res.json();
            processResponse(data);
            setLoading(false);
        } catch (error) {
            console.error("Error calling API:", error);
            setResponse("Error fetching data");
            setLoading(false);
        }
    };

    return (
        <div className="home-container">
            <div className="llm">            
                {loading ? null : (
                    <div className="llm-response">
                        <TypewriterEffect text={response} setWriting={setWriting}/>
                    </div>
                )}
                 <UserInput writing={writing} handleSubmit={handleClick} /> 
            </div>
        </div>
    );
}
