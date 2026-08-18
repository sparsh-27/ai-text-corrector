import { useState, useEffect } from 'react'
import './index.css'

function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)
  const [modelUsed, setModelUsed] = useState('')
  const [copied, setCopied] = useState(false)
  const [apiStatus, setApiStatus] = useState('checking') // 'online' | 'offline' | 'checking'
  const [errorMessage, setErrorMessage] = useState('')

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const res = await fetch(`${apiUrl}/health`);
      if (res.ok) {
        setApiStatus('online');
      } else {
        setApiStatus('offline');
      }
    } catch {
      setApiStatus('offline');
    }
  };

  const sampleTexts = [
    "I am writting a leter to you",
    "He dont know nothing about it",
    "There house is over their",
    "Can you borow me some money"
  ];

  const handleCorrect = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setResult('');
    setModelUsed('');
    setErrorMessage('');

    try {
      const response = await fetch(`${apiUrl}/api/correct`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to correct text');
      }

      const data = await response.json();
      setResult(data.corrected_text);
      setModelUsed(data.model_used);
      setApiStatus('online');
    } catch (error) {
      setErrorMessage(error.message || 'Error connecting to backend API');
      setApiStatus('offline');
    }
    setLoading(false);
  };

  const handleCopy = () => {
    if (!result) return;
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleClear = () => {
    setText('');
    setResult('');
    setModelUsed('');
    setErrorMessage('');
  };

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const charCount = text.length;

  return (
    <div className="app-wrapper">
      {/* Background Decorators */}
      <div className="bg-glow bg-glow-1"></div>
      <div className="bg-glow bg-glow-2"></div>

      <header className="header">
        <div className="brand">
          <div className="logo-icon">✨</div>
          <div>
            <h1 className="title">Neural Correct</h1>
            <p className="subtitle">Hybrid Deep Learning & NLP Text Correction Engine</p>
          </div>
        </div>

        <div className={`status-pill status-${apiStatus}`} onClick={checkHealth} title="Click to re-check status">
          <span className="status-dot"></span>
          {apiStatus === 'online' && 'API Connected'}
          {apiStatus === 'offline' && 'API Offline'}
          {apiStatus === 'checking' && 'Checking API...'}
        </div>
      </header>

      {/* Preset Chips */}
      <section className="presets-container">
        <span className="presets-label">Try a sample:</span>
        <div className="chips">
          {sampleTexts.map((sample, idx) => (
            <button key={idx} className="chip-btn" onClick={() => setText(sample)}>
              "{sample}"
            </button>
          ))}
        </div>
      </section>

      {/* Main Workspace */}
      <main className="main-content">
        {/* Left Panel: Original Input */}
        <div className="panel">
          <div className="panel-header">
            <h2>Original Text</h2>
            <div className="stats">
              <span>{wordCount} words</span>
              <span className="divider">•</span>
              <span>{charCount} chars</span>
            </div>
          </div>
          <textarea
            placeholder="Type or paste text with spelling/grammar errors here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            maxLength={2000}
          />
          <div className="panel-footer">
            <button className="secondary-btn" onClick={handleClear} disabled={!text}>
              Clear
            </button>
            <span className="limit-hint">{2000 - charCount} chars remaining</span>
          </div>
        </div>

        {/* Right Panel: Corrected Result */}
        <div className="panel">
          <div className="panel-header">
            <h2>Corrected Result</h2>
            {modelUsed && (
              <span className="model-badge">⚡ {modelUsed}</span>
            )}
          </div>
          <div className="result-box">
            {errorMessage ? (
              <div className="error-alert">
                <span>⚠️ {errorMessage}</span>
                <button onClick={checkHealth} className="retry-btn">Retry Connection</button>
              </div>
            ) : result ? (
              <p className="result-text">{result}</p>
            ) : (
              <div className="placeholder-text">
                <span>Enhanced text will appear here after processing...</span>
              </div>
            )}
          </div>
          <div className="panel-footer">
            <button 
              className="secondary-btn copy-btn" 
              onClick={handleCopy} 
              disabled={!result}
            >
              {copied ? '✓ Copied!' : '📋 Copy Result'}
            </button>
          </div>
        </div>
      </main>

      {/* Action Controls */}
      <div className="controls">
        <button className="primary-btn" onClick={handleCorrect} disabled={loading || !text.trim()}>
          {loading ? (
            <>
              <div className="loader"></div> Processing with Neural Pipeline...
            </>
          ) : (
            <>Enhance Text ✨</>
          )}
        </button>
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>Powered by <strong>SymSpell</strong> (Spelling Engine) & <strong>T5 Transformer</strong> (Grammar Model)</p>
      </footer>
    </div>
  );
}

export default App;
