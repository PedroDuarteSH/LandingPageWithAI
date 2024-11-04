import React, { useState, useEffect } from 'react';

export default function TypewriterEffect ({ text, setWriting }: { text: string, setWriting: (writing: boolean) => void }) {    
    const [displayedText, setDisplayedText] = useState('');
    const [index, setIndex] = useState(0);
    const wordList = text.split(" ");
    
    
    useEffect(() => {
        const typeWord = () => {   
            if (index < wordList.length) {
                if (index != wordList.length - 1)
                    setDisplayedText(prev => prev + wordList[index] + ' ');
                else
                    setDisplayedText(prev => prev + wordList[index]);
                setIndex(prev => prev + 1);
            } else {
                clearInterval(intervalId); // Clear interval when text is fully displayed
                setWriting(false);
            }
        };
        
        const intervalId = setInterval(typeWord, 200); // Adjust speed here (100ms per letter)


        return () => clearInterval(intervalId);
    }, [index, wordList, displayedText, setWriting]);

    return (
        <div>
            <p>{displayedText}</p>
        </div>
    );
};
