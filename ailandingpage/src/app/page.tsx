import React from "react";
import Image from "next/image";
import Home from "../pages/home";
import "./page.css";
export default function Page() {
  return (
    <div className="homepage">
      
      <div className="background-images">
        <div className="background-image-container">
          <Image
            className="background-image-audi"
            src={"/nextjs-github-pages/assets/images/bk/A3.png"}
            alt="AudiBackground"
            sizes="(orientation: portrait) 100vw, (orientation: landscape) 100vh"
            fill
            priority
          />
        </div>
        <div className="separator" />
        <div className="background-image-container">
          <Image
            className="background-image-code"
            src={"/nextjs-github-pages/assets/images/bk/Code.jpg"}
            alt="CodeBackground"
            sizes="(orientation: portrait) 100vw, (orientation: landscape) 100vh"
            fill
            priority
          />
        </div>
      </div>
      <Home />
      <div className="footer">
        <a
          href="https://www.linkedin.com/in/pedroduartesh"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            className="footer-logo"
            src={"/assets/icons/github-mark-white.svg"}
            alt="Git Hub logo"
            width={35}
            height={35}
          />
        </a>
        <a
          href="https://www.linkedin.com/in/pedroduartesh"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            className="footer-logo"
            src={"/assets/icons/iconmonstr-linkedin-3.svg"}
            alt="Linked"
            width={35}
            height={35}
          />
        </a>
      </div>
    </div>
  );
}
