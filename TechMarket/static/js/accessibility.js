console.log("Accessibility script loaded."); // testing is the js loaded

// Text-to-Speech funtion (if text is hightlighted)
function readSelection() {
    console.log("Read Selection activated."); 
    const selectedText = window.getSelection().toString().trim();
    if (selectedText.length > 0) {
        console.log("Selected text found:", selectedText);
        if (typeof responsiveVoice !== 'undefined' && responsiveVoice.voiceSupport()) { // Checks if ResposviseVoice has loaded 
            console.log("Attempting to speak selection..."); 
            responsiveVoice.cancel(); // Cancel current speech
            responsiveVoice.speak(selectedText, "UK English Female"); //Use UK English Female voice
        } else { // if nothting is highlited print one of these:
            console.error("ResponsiveVoice library not loaded/supported.");
        }
    } else {
        console.log("No text selected."); 
    }
}

//Text-to-Speech (Read on TAB/click)  
function TabHighlight(event) {
    if (typeof responsiveVoice === 'undefined' || !responsiveVoice.voiceSupport()) {
        return; // Silently ignore if voice is not ready
    }

    const focusedElement = event.target;
    let textToRead = '';

    // Prioritize aria-label, then innerText, textcontent
    textToRead = focusedElement.getAttribute('aria-label') || focusedElement.innerText || focusedElement.textContent || '';
    textToRead = textToRead.trim();

    // Avoid reading out large chunks of non-interactive text focus on button, link or feild
    if (focusedElement.matches('a, button, input, textarea, [role="button"], [role="link"], [tabindex]:not([tabindex="-1"])')) {
         if (textToRead) {
            console.log("detected Speaking:", textToRead);
            responsiveVoice.cancel(); // Stop previous speech
            responsiveVoice.speak(textToRead, "UK English Female");
        }
    }
}

// Speech recognition API (Web Speech)set up
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;
let activeVoiceButton = null;
let targetInputElement = null;

// Initialise Recognition if supported
if (SpeechRecognition) { 
    recognition = new SpeechRecognition();
    recognition.continuous = false; 
    recognition.lang = 'en-GB';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('Voice result:', transcript);
        if (targetInputElement) {
            targetInputElement.value = transcript;
            console.log(`Set value of input ${targetInputElement.id} to: ${transcript}`);
        } else {
            console.error("No where to put result.");
        }
    };
    //error handling
    recognition.onerror = (event) => {
        console.error(`Voice recognition error: ${event.error}`);
        alert(`Voice input failed: ${event.error}`);
    };
    // errors during activation od speech       
    recognition.onend = () => {
        console.log("Voice recognition ended.");
        if (activeVoiceButton) {
            activeVoiceButton.classList.remove('btn-danger', 'listening');
            activeVoiceButton.classList.add('btn-outline-secondary');
            activeVoiceButton.disabled = false;
            const originalTitle = activeVoiceButton.getAttribute('data-original-title') || 'Activate voice input';
            activeVoiceButton.title = originalTitle;
        }
        activeVoiceButton = null;
        targetInputElement = null;
    };

} else {
    console.warn("Speech Recognition API is not supported by this browser.");
}

// Function to start voice input for a specific field
function startVoiceInput(buttonElement, inputElement) {
    if (!recognition) {
        alert("Speech recognition not available.");
        return;
    }

    if (activeVoiceButton && activeVoiceButton !== buttonElement) {
         recognition.stop();
    }

    targetInputElement = inputElement;
    activeVoiceButton = buttonElement;

    console.log(`Starting voice input for: ${inputElement.id}`);
    try {
        recognition.start();
        if (!buttonElement.hasAttribute('data-original-title')) {
             buttonElement.setAttribute('data-original-title', buttonElement.title);
        }
        buttonElement.classList.remove('btn-outline-secondary');
        buttonElement.classList.add('btn-danger', 'listening');
        buttonElement.title = "Listening...";
        buttonElement.disabled = true;
    } catch (e) {
        console.error("Could not start voice recognition:", e);
        if (activeVoiceButton) {
            activeVoiceButton.classList.remove('btn-danger', 'listening');
            activeVoiceButton.classList.add('btn-outline-secondary');
             const originalTitle = activeVoiceButton.getAttribute('data-original-title') || 'Activate voice input';
            activeVoiceButton.title = originalTitle;
            activeVoiceButton.disabled = false;
        }
        activeVoiceButton = null;
        targetInputElement = null;
        alert("Could not start voice recognition.");
    }
}

//Event Listeners for search 
document.addEventListener('DOMContentLoaded', function() {
    // Enable search mic button and setup dynamic buttons if speech recognition is supported
    if (recognition) {
        const searchMicButton = document.getElementById('mic-button');
        if (searchMicButton) {
            searchMicButton.disabled = false;
            searchMicButton.classList.add('voice-input-button');
            searchMicButton.setAttribute('data-target-input', '#search-input');
            console.log("Search mic button enabled.");
        }
    }

    // Attach the listener for the 'Read on Focus' feature
    document.body.addEventListener('focusin', TabHighlight); //
    console.log("'Read on Focus' listener attached.");

    // Delegated event listener for all voice input buttons
    document.body.addEventListener('click', function(event) {
        const button = event.target.closest('.voice-input-button');
        if (button && recognition) {
            event.preventDefault();
            // Find target input using the name selector stored in data-target-input
            const targetInputSelector = button.getAttribute('data-target-input');
            const targetInput = targetInputSelector ? document.querySelector(targetInputSelector) : null;
            if (targetInput) {
                startVoiceInput(button, targetInput);
            } else {
                console.error(`Could not find target input element for selector: ${targetInputSelector}`);
                alert('Could not find the associated input field.');
            }
        } else if (button && !recognition) {
             alert("Speech recognition not available in this browser.");
        }
    });
    console.log("Delegated click listener for voice buttons attached.");
}); 