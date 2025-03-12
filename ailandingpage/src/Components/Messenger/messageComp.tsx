import "./messageComp.css"
import { Message } from "@/pages/home"
import Image from "next/image";
import ReactMarkdown from "react-markdown";

export default function MessageComp({ message }: { message: Message }) {


    const image = message.role === "user" ? (
        <Image
            className="icon"
            src={"/assets/icons/user-icon.svg"}
            alt="User-icon"
            width={50}
            height={50}
        />
    ) : (
        <Image
            className="icon"
            src={"/assets/icons/ai-icon.svg"}
            alt="AI-icon"
            width={50}
            height={50}
        />
    );
    return (
        <div className={message.role === "user" ? "message user" : "message ai"}>
            <div className="iconbox">
                {image}
            </div>
            <div className="messagebox">
                <ReactMarkdown className="message_item">{message.content}</ReactMarkdown>
            </div>
        </div>

    );
}