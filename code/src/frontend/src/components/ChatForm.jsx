import React, { useRef } from "react";
import VoiceInput from "./Voice";

const ChatForm = ({ chatHistory, setChatHistory }) => {
  const inputRef = useRef();

  const handleVoiceInput = (text) => {
    console.log("User said:", text);
    if (inputRef.current) {
      inputRef.current.value = text;
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    const userMessage = inputRef.current.value.trim();
    if (!userMessage) return;
    inputRef.current.value = "";

    setChatHistory((history) => [
      ...history,
      { role: "user", text: userMessage },
      { role: "model", text: "Thinking..." }, 
    ]);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userMessage }),
      });

      const data = await response.json();

      setChatHistory((history) =>
        history.map((msg, index) =>
          index === history.length - 1 ? { role: "model", text: data.prediction } : msg
        )
      );
    } catch (error) {
      console.error("Error fetching prediction:", error);
      setChatHistory((history) =>
        history.map((msg, index) =>
          index === history.length - 1 ? { role: "model", text: "Error generating response." } : msg
        )
      );
    }
  };

  return (
    <>
      <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
        <input
          ref={inputRef}
          type="text"
          className="message-input"
          placeholder="Message....."
          required
        />

        <button>
          <span className="material-symbols-rounded">send</span>
        </button>
        <VoiceInput onVoiceInput={handleVoiceInput} />
      </form>
    </>
  );
};

export default ChatForm;
