import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader2, Cpu, ShieldCheck, WifiOff } from 'lucide-react';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am your local AI agent. How can I help you today?' }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(null);
  const [worker, setWorker] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Initialize the worker
    const aiWorker = new Worker(new URL('./worker.js', import.meta.url), {
      type: 'module'
    });

    aiWorker.onmessage = (event) => {
      const { status, output, error, progress: p, file } = event.data;

      if (status === 'progress') {
        setProgress({ file, progress: p });
      } else if (status === 'update') {
        // Partial update for streaming-like feel
        setMessages(prev => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage.role === 'assistant') {
            return [...prev.slice(0, -1), { role: 'assistant', content: output }];
          }
          return [...prev, { role: 'assistant', content: output }];
        });
      } else if (status === 'complete') {
        setIsLoading(false);
        setProgress(null);
        setMessages(prev => {
          const lastMessage = prev[prev.length - 1];
           if (lastMessage.role === 'assistant') {
            return [...prev.slice(0, -1), { role: 'assistant', content: output }];
          }
          return [...prev, { role: 'assistant', content: output }];
        });
      } else if (status === 'error') {
        setIsLoading(false);
        setProgress(null);
        setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${error}` }]);
      }
    };

    setWorker(aiWorker);

    return () => {
      aiWorker.terminate();
    };
  }, []);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    worker.postMessage({
      type: 'generate',
      text: input
    });
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 py-4 px-6 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bot className="w-8 h-8 text-blue-600" />
          <h1 className="text-xl font-bold text-gray-800">LocalAI Agent</h1>
        </div>
        <div className="flex gap-4">
            <div className="flex items-center gap-1 text-sm text-green-600 bg-green-50 px-3 py-1 rounded-full">
                <ShieldCheck className="w-4 h-4" />
                <span>Private</span>
            </div>
            <div className="flex items-center gap-1 text-sm text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                <WifiOff className="w-4 h-4" />
                <span>Offline</span>
            </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-4 ${
              msg.role === 'user'
                ? 'bg-blue-600 text-white rounded-tr-none'
                : 'bg-white border border-gray-200 text-gray-800 rounded-tl-none shadow-sm'
            }`}>
              <div className="flex items-center gap-2 mb-1">
                {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                <span className="text-xs font-semibold uppercase tracking-wider">
                  {msg.role === 'user' ? 'You' : 'AI Agent'}
                </span>
              </div>
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && progress && (
          <div className="flex justify-start">
             <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-none p-4 shadow-sm w-full max-w-md">
                <div className="flex items-center gap-2 mb-2 text-blue-600">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm font-medium">Loading Model...</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2">
                    <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${progress.progress || 0}%` }}
                    ></div>
                </div>
                <p className="text-[10px] text-gray-500 mt-1 uppercase tracking-tighter truncate">
                    {progress.file}
                </p>
             </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Input Area */}
      <footer className="p-4 bg-white border-t border-gray-200">
        <div className="max-w-4xl mx-auto flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your message here..."
            className="flex-1 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 text-white p-3 rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Send className="w-6 h-6" />}
          </button>
        </div>
        <div className="text-center mt-2 text-[10px] text-gray-400 flex items-center justify-center gap-4">
            <span className="flex items-center gap-1"><Cpu className="w-3 h-3" /> Local Processing</span>
            <span>Running: LaMini-Flan-T5-78M</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
