import { useState } from "react";
import { LogOut } from "lucide-react";

// Import your existing Dashboard components
import Hero from "./components/Hero";
import AgentFlow from "./components/AgentFlow";
import Dashboard from "./components/Dashboard";
import { mockData } from "./data/mockReport";

// Import Auth Components
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";

function App() {
  const [view, setView] = useState("auth-login"); 
  const [data, setData] = useState(null);
  const [flowFinished, setFlowFinished] = useState(false);

  // --- Handlers ---
  const handleLoginSuccess = () => setView("hero");
  const handleRegisterSuccess = () => setView("hero");

  const handleSearch = async (topic) => {
    setView("loading");
    setFlowFinished(false);
    try {
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic })
      });
      const result = await response.json();
      setData(result);
      
      // Tell AgentFlow to jump to completion state
      setFlowFinished(true);
      // Wait a moment for the green checkmarks to show before sliding in the Dashboard
      setTimeout(() => setView("results"), 1200);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to connect to Python Server. Using Mock Data.");
      setData(mockData); 
      setFlowFinished(true);
      setTimeout(() => setView("results"), 1200);
    }
  };

  // --- RENDER LOGIC ---
  if (view === "auth-login") {
    return <Login 
      onSwitchToRegister={() => setView("auth-register")} 
      onLoginSuccess={handleLoginSuccess} 
    />;
  }

  if (view === "auth-register") {
    return <Register 
      onSwitchToLogin={() => setView("auth-login")} 
      onRegisterSuccess={handleRegisterSuccess} 
    />;
  }

  // --- MAIN APP (HERO / DASHBOARD) ---
  return (
    <div className="min-h-screen font-sans selection:bg-indigo-500/30 overflow-x-hidden">
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-slate-950/80 backdrop-blur-xl shadow-lg">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          
          {/* LOGO */}
          <div className="flex items-center gap-3 cursor-pointer group" onClick={() => setView('hero')}>
            <div className="w-9 h-9 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20 group-hover:shadow-indigo-500/40 transition-all duration-300">
              N
            </div>
            <span className="font-bold text-xl tracking-tight text-white group-hover:text-indigo-200 transition-colors">Neural Conductor</span>
          </div>

          {/* NEW GOD-LEVEL SIGN OUT BUTTON */}
          <button 
            onClick={() => setView("auth-login")}
            className="group flex items-center gap-2 px-4 py-2 rounded-lg glass-card text-slate-400 hover:text-rose-400 hover:border-rose-500/30 hover:bg-rose-500/10 transition-all duration-300 backdrop-blur-md"
          >
            <span className="text-sm font-medium">Sign Out</span>
            <LogOut size={16} className="group-hover:translate-x-0.5 transition-transform" />
          </button>

        </div>
      </nav>

      <main className="pt-24 pb-12">
        {view === "hero" && <Hero onSearch={handleSearch} />}
        {view === "loading" && <AgentFlow isFinished={flowFinished} />}
        {view === "results" && <Dashboard data={data} />}
      </main>
    </div>
  );
}

export default App;