import React, { useState } from "react";
import ChatbotIcon from "./ChatbotIcon";
import "./Chat.css";
import ChatForm from "./ChatForm";
import ChatMessage from "./ChatMessage";

const Chatbot = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const generateBotResponse = (history) => {
    console.log(history);
  };
  return (
    <div>
      <div className="container show-chatbot">
      {/* <button onClick={()=>{setShowChatbot(prev => !prev)}} id="chatbot-toggler">
      <span class="material-symbols-rounded">mode_comment</span>
      <span class="material-symbols-rounded">close</span>
      </button> */}
        <div className="chatbot-popup">
          <div className="chat-header">
            <div className="header-info">
              <ChatbotIcon />
              <h2 className="logo-text">ChatBot</h2>
            </div>            
          </div>
          <div className="chat-body">
            <div className="message bot-message">
              <ChatbotIcon />
              <p className="message-text">Hey! How can i help you!</p>
            </div>
            {chatHistory.map((chat, index) => (
              <ChatMessage key={index} chat={chat} />
            ))}
          </div>
          <div className="chat-footer">
            <ChatForm
              chatHistory={chatHistory}
              setChatHistory={setChatHistory}
              generateBotResponse={generateBotResponse}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
