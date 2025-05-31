import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { motion } from 'framer-motion';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { from: 'bot', text: "Hi there! 👋 What information are you looking for?" },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { from: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input }),
      });
      const data = await res.json();

      setTimeout(() => {
        setIsTyping(false);
        setMessages((prev) => [...prev, { from: 'bot', text: data.answer }]);
      }, 1000); // Simulate typing delay
    } catch (err) {
      setIsTyping(false);
      setMessages((prev) => [...prev, { from: 'bot', text: 'Something went wrong. Please try again.' }]);
    }
  };

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  return (
    <div className="fixed bottom-6 right-6 z-50 font-sans">
      {!isOpen && (
        <button onClick={() => setIsOpen(true)} className="bg-purple-600 hover:bg-purple-700 text-white p-4 rounded-full shadow-lg">
          <Bot />
        </button>
      )}

      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-80 h-[500px] bg-white rounded-2xl shadow-lg flex flex-col"
        >
          <div className="bg-purple-600 text-white px-4 py-3 rounded-t-2xl flex justify-between items-center">
            <div className="flex gap-2 items-center">
              <Bot className="w-5 h-5" />
              <span className="font-semibold">ZomatoBot</span>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-white hover:text-gray-200">×</button>
          </div>

          <div ref={chatRef} className="flex-1 overflow-y-auto p-3 space-y-4 bg-gray-50">
            {messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-xs px-4 py-2 rounded-xl text-sm ${msg.from === 'user' ? 'bg-purple-100 text-right' : 'bg-white border'}`}>
                  {msg.text}
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-white border px-4 py-2 rounded-xl text-sm italic text-gray-500">Typing...</div>
              </div>
            )}
          </div>

          <div className="p-3 border-t flex gap-2">
            <input
              type="text"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              className="flex-1 border rounded-full px-4 py-2 text-sm outline-purple-400"
            />
            <button onClick={sendMessage} className="text-purple-600 hover:text-purple-800">
              <Send className="w-5 h-5" />
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Chatbot;
