import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface Model {
  name: string;
  type: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState('llama3.2');
  const [availableModels, setAvailableModels] = useState<Model[]>([]);
  const [activeTab, setActiveTab] = useState<'chat' | 'image' | 'code'>('chat');
  const [sessionId, setSessionId] = useState<string>('');

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchModels();
    const newSessionId = generateSessionId();
    setSessionId(newSessionId);
  }, []);

  const generateSessionId = () => {
    return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  };

  const fetchModels = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/models`);
      const chatModels = response.data.chat.map((name: string) => ({ name, type: 'chat' }));
      setAvailableModels(chatModels);
    } catch (error) {
      console.error('Failed to fetch models:', error);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/chat`, {
        message: input,
        model: selectedModel,
        session_id: sessionId,
        temperature: 0.7,
        max_tokens: 2048
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        timestamp: response.data.timestamp
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">
      <div className="sidebar">
        <h1>AI Assistant</h1>
        <div className="tabs">
          <button 
            className={activeTab === 'chat' ? 'active' : ''}
            onClick={() => setActiveTab('chat')}
          >
            Chat
          </button>
          <button 
            className={activeTab === 'image' ? 'active' : ''}
            onClick={() => setActiveTab('image')}
          >
            Image
          </button>
          <button 
            className={activeTab === 'code' ? 'active' : ''}
            onClick={() => setActiveTab('code')}
          >
            Code
          </button>
        </div>
        <div className="model-selector">
          <label>Model:</label>
          <select 
            value={selectedModel} 
            onChange={(e) => setSelectedModel(e.target.value)}
          >
            {availableModels.map(model => (
              <option key={model.name} value={model.name}>
                {model.name}
              </option>
            ))}
          </select>
        </div>
      </div>
      
      <div className="main-content">
        <div className="chat-container">
          <div className="messages">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.role}`}>
                <div className="message-content">
                  {message.content}
                </div>
                <div className="message-time">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message assistant">
                <div className="loading">Thinking...</div>
              </div>
            )}
          </div>
          
          <div className="input-container">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={loading}
            />
            <button onClick={sendMessage} disabled={loading || !input.trim()}>
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;