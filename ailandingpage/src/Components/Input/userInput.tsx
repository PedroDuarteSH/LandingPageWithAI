import React, { useState } from "react";
import { BsArrowRight } from "react-icons/bs";
import "./userInput.css"

export default function UserInput ({ writing, handleSubmit }: { writing: boolean, handleSubmit: () => void }){
    const [question, setQuestion] = useState<string>("");

    const changeQuestion = (e: React.ChangeEvent<HTMLInputElement>) => {
        setQuestion(e.target.value);
    };

    const onKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        // Shift + Enter does not add a new line
        if (e.key === "Enter") {
            e.preventDefault(); // Prevent the default Enter key behavior (which inserts a new line)
            handleSubmit(); // Call the submit function
        }
    };
    return (
        <div className="llm-input">
            <input
                className="llm-input-textarea"
                value={question}
                onChange={changeQuestion}
                onKeyDown={onKeyPress}
                disabled={writing}
                placeholder="Ask a question..."
            />
                <button
                    className="llm-input-button"
                    onClick={handleSubmit}
                    disabled={writing}
                >
                    <BsArrowRight />
                </button>
        </div>
    );
};
