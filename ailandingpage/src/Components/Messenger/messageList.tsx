import MessageComp from "./messageComp";
import "./messageList.css"
import { Message } from "@/pages/home";


export default function MessageList({ messages }: { messages: Message[] }) {
    return (
        <div className="message-list">
            {messages.map((msg, index) => 
                msg.show ? <MessageComp key={index} message={msg} /> : null
            )}
        </div>
    );
}