import React, { useState } from "react";
import "./userInput.css"
import Image from "next/image";
export default function UserInput({ modelGenerating, handleSubmit }: { modelGenerating: boolean, handleSubmit: (question: string) => void }) {
    const [question, setQuestion] = useState<string>("");
    const changeQuestion = (e: React.ChangeEvent<HTMLInputElement>) => {
        setQuestion(e.target.value);
    };

    const resetAndSubmit = () => {
        if (modelGenerating){
            handleSubmit("")
        }


        if(question.length == 0){
            return
        }

        handleSubmit(question.slice()) 
        setQuestion("") 
    }
    

    return (
        <div className="llm-input">
            <input
                className="llm-input-textarea"
                value={question}
                onChange={changeQuestion}
                disabled={modelGenerating}
                placeholder="Ask a question..."
            />
            <button
                className="llm-input-button"
                onClick={resetAndSubmit}
            >
                {(!modelGenerating) ? <Image
                    src={"/assets/icons/send-icon.svg"}
                    alt="Git Hub logo"
                    width={30}
                    height={30}
                /> : <Image
                    src={"/assets/icons/stop-icon.svg"}
                    alt="Stop-icon"
                    width={30}
                    height={30}
                />}


            </button>
        </div>
    );
};
