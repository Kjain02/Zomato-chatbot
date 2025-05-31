import React, { useState, useRef, useEffect } from "react";
import "./App.css";
import { Typewriter } from "react-simple-typewriter";
import botAvatar from "../src/bot.png";

// Pattern to detect when the bot doesn't know the answer or needs clarification
const NEGATIVE_RESPONSE_PATTERN =
  /(sorry|don't have|do not have|couldn't find|could not find|cannot find|can't find|no information|not available|not found|please clarify|could you clarify|do you mean|can you specify)/i;

function App() {
  // Initial message state with a greeting from the bot
  const [messages, setMessages] = useState([
    {
      from: "bot",
      text: "👋 Hi! I'm Zomato Bot. What would you like to know?",
    },
  ]);

  // State for user input
  const [input, setInput] = useState("");
  // Loading state to show typing animation
  const [loading, setLoading] = useState(false);
  // Bot's current typing text
  const [botTypingText, setBotTypingText] = useState("");
  // Ref to scroll to the bottom of the messages
  const messagesEndRef = useRef(null);

  // States for collecting additional info (restaurant name/location)
  const [collectingInfo, setCollectingInfo] = useState(false);
  const [restaurantName, setRestaurantName] = useState("");
  const [restaurantLocation, setRestaurantLocation] = useState("");
  const [currentQuestion, setCurrentQuestion] = useState("");

  // Scroll chat to bottom on new message or typing event
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Trigger scroll when messages or typing status updates
  useEffect(() => {
    scrollToBottom();
  }, [messages, loading, botTypingText]);

  // Cancel info collection if user wants to stop
  useEffect(() => {
    if (
      collectingInfo &&
      input
        .trim()
        .toLowerCase()
        .match(/cancel|stop|quit|exit|never mind/)
    ) {
      setCollectingInfo(false);
      setCurrentQuestion("");
      setRestaurantName("");
      setRestaurantLocation("");
      setTimeout(() => {
        setBotTypingText(
          "No problem! I've canceled the information collection. How else can I help you?"
        );
        setInput("");
        setLoading(false);
      }, 500);
    }
  }, [input, collectingInfo]);

  // Save restaurant info (name + location) to backend
  const saveRestaurantInfoToQueries = async (location) => {
    try {
      const restaurantInfo = {
        restaurant_name: restaurantName.trim(),
        location: location.trim(),
      };

      const res = await fetch("http://127.0.0.1:8000/save_query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(restaurantInfo),
      });

      const data = await res.json();

      setCollectingInfo(false);
      setRestaurantName("");
      setRestaurantLocation("");
      setCurrentQuestion("");

      setTimeout(() => {
        setBotTypingText(
          "Thank you for providing that information!. Is there any specific question regrading the above mentioned restaurant?"
        );
        setLoading(false);
      }, 1000);
    } catch (err) {
      console.error("Error saving restaurant info:", err);
      setLoading(false);
      setBotTypingText(
        "I'm having trouble saving that information. Please try again later."
      );
    }
  };

  // Ask follow-up questions to collect restaurant name and location
  const handleFollowUpResponse = (extractedName = "") => {
    if (!currentQuestion) {
      setCurrentQuestion("name");
      setTimeout(() => {
        setBotTypingText(
          `Could you please confirm the exact name of the restaurant`
        );
        setLoading(false);
      }, 1000);
    } else if (currentQuestion === "name") {
      const name = input;
      setRestaurantName(name);
      setInput("");
      setCurrentQuestion("location");
      setTimeout(() => {
        setBotTypingText(
          "Great! Now, could you please specify the location of the restaurant?"
        );
        setLoading(false);
      }, 1000);
    } else if (currentQuestion === "location") {
      const location = input;
      setRestaurantLocation(location);
      setInput("");
      setLoading(true);
      setTimeout(() => {
        saveRestaurantInfoToQueries(location);
      }, 500);
    }
  };

  // Main function that handles sending a message
  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user's message to chat
    const userMessage = { from: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setBotTypingText("thinking");

    // If we're already collecting info, go through follow-up questions
    if (collectingInfo) {
      handleFollowUpResponse();
      return;
    }

    try {
      // Send message to backend API
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input }),
      });

      const data = await res.json();

      // If the bot can't answer, trigger info collection
      if (NEGATIVE_RESPONSE_PATTERN.test(data.answer)) {
        const potentialRestaurantName = input.replace(
          /what is|what's|where is|address of|menu|item|price|rating|review|tell me about/gi,
          ""
        ).trim();

        setCollectingInfo(true);
        setTimeout(() => {
          setBotTypingText(data.answer);
          setLoading(false);
          setTimeout(() => {
            handleFollowUpResponse(potentialRestaurantName);
          }, 2000);
        }, 1000);
      } else {
        // Bot gives a valid answer
        setTimeout(() => {
          setBotTypingText(data.answer);
          setLoading(false);
        }, 1000);
      }

      setInput("");
    } catch (err) {
      console.error(err);
      setLoading(false);
      setBotTypingText(
        "Sorry, I'm having trouble connecting to the server. Please try again later."
      );
    }
  };

  // Send message on pressing Enter
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      {/* Chat Header with Bot Avatar and Online Status */}
      <div className="chat-header">
        <div className="profile">
          <div className="avatar">
            <img src={botAvatar} alt="Bot avatar" />
          </div>
          <div className="info">
            <h3>Zomato Bot</h3>
            <span className="status">
              <span className="status-dot"></span> We're online!
            </span>
          </div>
        </div>
      </div>

      {/* Messages Section */}
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`message-wrapper ${msg.from === "bot" ? "bot" : "user"}`}
          >
            {msg.from === "bot" && (
              <div className="bot-avatar">
                <img src={botAvatar} alt="Bot" />
              </div>
            )}
            <div className={`message ${msg.from}`}>
              <span>{msg.text}</span>
            </div>
          </div>
        ))}

        {/* Typing animation while bot is "thinking" */}
        {loading && (
          <div className="message-wrapper bot">
            <div className="bot-avatar">
              <img src={botAvatar} alt="Bot" />
            </div>
            <div className="message bot typing">
              <span className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </span>
            </div>
          </div>
        )}

        {/* Display bot's message using a typewriter effect */}
        {botTypingText && !loading && (
          <div className="message-wrapper bot">
            <div className="bot-avatar">
              <img src={botAvatar} alt="Bot" />
            </div>
            <div className="message bot">
              <span className="typewriter">
                <Typewriter
                  words={[botTypingText]}
                  loop={1}
                  cursor
                  typeSpeed={40}
                  deleteSpeed={9999}
                  delaySpeed={1000}
                  onLoopDone={() => {
                    setMessages((prev) => [
                      ...prev,
                      { from: "bot", text: botTypingText },
                    ]);
                    setBotTypingText("");
                  }}
                />
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Chat Footer - Input Field and Send Button */}
      <div className="chat-footer">
        <div className="input-wrapper">
          <button className="emoji-button">😊</button>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Enter your message..."
          />
          <button
            className="send-button"
            onClick={sendMessage}
            disabled={!input.trim()}
          >
            <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path>
            </svg>
          </button>
        </div>
        <div className="powered-by">
          POWERED BY <strong>ZOMATO</strong>
        </div>
      </div>
    </div>
  );
}

export default App;
