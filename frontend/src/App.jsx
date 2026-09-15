import { useState } from 'react';
import axios from 'axios';

export default function App() {
  const [tweet, setTweet] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const processTicket = async () => {
    if (!tweet.trim()) return;
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('http://127.0.0.1:8080/api/process-ticket', {
        customer_tweet: tweet
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while processing the ticket.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto space-y-8">
        
        <header className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h1 className="text-3xl font-bold text-gray-900">Hiver AI Support Agent</h1>
          <p className="text-gray-500 mt-2">Automated intent classification and response generation for @AskAmex</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 space-y-4">
            <h2 className="text-xl font-semibold text-gray-800">Incoming Customer Tweet</h2>
            <textarea
              className="w-full h-40 p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              placeholder="Paste a customer tweet here..."
              value={tweet}
              onChange={(e) => setTweet(e.target.value)}
            />
            <button
              onClick={processTicket}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:bg-blue-300"
            >
              {loading ? 'Analyzing...' : 'Process Ticket'}
            </button>
            {error && <div className="p-4 bg-red-50 text-red-700 rounded-lg">{error}</div>}
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 space-y-6">
            <h2 className="text-xl font-semibold text-gray-800">Agent Reasoning Dashboard</h2>
            
            {!result && !loading && (
              <div className="h-full flex items-center justify-center text-gray-400 pb-12">
                Waiting for incoming ticket...
              </div>
            )}

            {loading && (
              <div className="animate-pulse space-y-4">
                <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                <div className="h-10 bg-gray-200 rounded"></div>
                <div className="h-24 bg-gray-200 rounded"></div>
              </div>
            )}

            {result && (
              <div className="space-y-6">
                <div className="flex space-x-4">
                  <div className="flex-1 bg-gray-50 p-4 rounded-lg border border-gray-100">
                    <p className="text-sm text-gray-500 font-medium">Detected Intent</p>
                    <p className="text-lg font-bold text-blue-600 mt-1 uppercase tracking-wide">
                      {result.intent}
                    </p>
                  </div>
                  <div className={`flex-1 p-4 rounded-lg border ${result.escalate ? 'bg-red-50 border-red-100' : 'bg-green-50 border-green-100'}`}>
                    <p className="text-sm font-medium focus:outline-none">Action Required</p>
                    <p className={`text-lg font-bold mt-1 ${result.escalate ? 'text-red-700' : 'text-green-700'}`}>
                      {result.escalate ? 'HUMAN ESCALATION' : 'AUTO-HANDLE'}
                    </p>
                  </div>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg border border-blue-100 relative">
                  <p className="text-sm text-blue-800 font-medium mb-2">Drafted Grounded Reply</p>
                  <p className="text-gray-800">"{result.drafted_reply}"</p>
                  <div className="absolute top-4 right-4 text-xs text-blue-400 font-medium">
                    {result.drafted_reply.length} / 280
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}