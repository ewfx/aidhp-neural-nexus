const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition; // Fix for Chrome/Safari

if (!SpeechRecognition) {
    alert("Speech recognition is not supported in this browser.");
}

const VoiceInput = ({ onVoiceInput }) => {
    const startListening = () => {
        if (!SpeechRecognition) return;

        const recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.continuous = false;

        recognition.onstart = () => console.log("Listening...");
        recognition.onend = () => console.log("Stopped listening");

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log("Recognized:", transcript);
            onVoiceInput(transcript);
        };

        recognition.start();
    };

    return (
            <>
                <button onClick={startListening}><span class="material-symbols-rounded">mic</span></button>
            </>
            
    );
};

export default VoiceInput;
