// =============================
// TEXT TO SPEECH
// =============================
function speak(text) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    synth.speak(utterance);
}


// =============================
// UNIVERSAL VOICE INPUT (for any input field)
// =============================
function startVoiceInput(inputId) {

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Please use Google Chrome for voice support.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.start();
    speak("Listening...");

    recognition.onresult = function(event) {
        const speech = event.results[0][0].transcript;
        document.getElementById(inputId).value = speech;
        speak("Recorded");
    };

    recognition.onerror = function(event) {
        alert("Voice Error: " + event.error);
    };
}


// =============================
// HOME PAGE VOICE NAVIGATION
// =============================
function startVoiceHome() {

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Use Google Chrome for voice support.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";

    recognition.start();
    speak("Say login or register");

    recognition.onresult = function(event) {
        let speech = event.results[0][0].transcript.toLowerCase();

        if (speech.includes("login")) {
            window.location.href = "/login";
        } 
        else if (speech.includes("register")) {
            window.location.href = "/register";
        } 
        else {
            speak("Please say login or register");
        }
    };
}


// =============================
// FULL VOICE LOGIN FLOW
// =============================
function enableVoiceLogin() {

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Use Google Chrome.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";

    let step = 1;

    speak("Voice login activated. Say your username.");
    recognition.start();

    recognition.onresult = function(event) {
        const speech = event.results[0][0].transcript;

        if (step === 1) {
            document.getElementById("username").value = speech;
            speak("Now say your password.");
            step = 2;
            recognition.start();
        }
        else {
            document.getElementById("password").value = speech;
            speak("Logging in.");
            document.getElementById("loginForm").submit();
        }
    };
}


// =============================
// REMINDER
// =============================
function addReminder() {
    let title = document.getElementById("reminderTitle").value;
    let time = document.getElementById("reminderTime").value;

    fetch("/add_reminder", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title: title, time: time})
    })
    .then(res => res.json())
    .then(data => {
        speak("Reminder added successfully");
        alert("Reminder added successfully!");
    });
}


// =============================
// AI ASSISTANT
// =============================
function askAI() {

    let question = document.getElementById("aiQuestion").value;

    fetch("/ask_ai", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question: question})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("aiResponse").innerText = data.answer;
        speak(data.answer);
    });
}
