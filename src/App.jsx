import React, { useState } from 'react';
import { Sun, Moon, Search, MapPin, ExternalLink, GraduationCap, Calendar, AlertCircle } from 'lucide-react';
import initialPrograms from '../discovered_programs.json';

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRegion, setSelectedRegion] = useState("All");

  const filteredPrograms = initialPrograms.filter(program => {
    const matchesSearch = program.program.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          program.university.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRegion = selectedRegion === "All" || program.region === selectedRegion;
    return matchesSearch && matchesRegion;
  });

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-slate-50 dark:bg-zinc-900 text-slate-800 dark:text-zinc-100 transition-colors">
        <header className="sticky top-0 z-50 bg-emerald-600 text-white p-4 shadow flex justify-between items-center">
          <h1 className="font-black text-xl">Estudar<span className="text-amber-300">BR</span></h1>
          <button onClick={() => setDarkMode(!darkMode)} className="p-2 rounded-full bg-emerald-700">
            {darkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </header>
        <main className="max-w-md mx-auto px-4 py-6">
          <input 
            type="text" placeholder="Search courses..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full p-3 rounded-xl border mb-4 bg-white dark:bg-zinc-800 text-slate-900 dark:text-white"
          />
          <div className="space-y-4">
            {filteredPrograms.map(p => (
              <div key={p.id} className="bg-white dark:bg-zinc-800 p-4 rounded-2xl shadow-sm border-l-4 border-emerald-500">
                <h4 className="font-bold text-base flex items-center gap-2"><GraduationCap size={18}/>{p.program}</h4>
                <p className="text-xs text-slate-500">{p.university} ({p.state})</p>
                <a href={p.link} target="_blank" rel="noreferrer" className="mt-3 block text-center bg-slate-900 text-white py-2 rounded-xl text-xs font-bold">Open Portal</a>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
