import React, { useState } from 'react';
import { Sun, Moon, Search, MapPin, ExternalLink, GraduationCap, Calendar, AlertCircle } from 'lucide-react';

// Connect the live scraper JSON output data channel directly to the template matrix
import initialPrograms from '../discovered_programs.json';

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRegion, setSelectedRegion] = useState("All");

  const filteredPrograms = initialPrograms.filter(program => {
    const matchesSearch = 
      program.program.toLowerCase().includes(searchTerm.toLowerCase()) ||
      program.university.toLowerCase().includes(searchTerm.toLowerCase()) ||
      program.state.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesRegion = selectedRegion === "All" || program.region === selectedRegion;
    
    return matchesSearch && matchesRegion;
  });

  const getStatusStyles = (status) => {
    switch (status) {
      case 'Open':
        return 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-900/60';
      case 'Closed':
        return 'bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-900/60';
      default:
        return 'bg-slate-100 dark:bg-zinc-800 text-slate-600 dark:text-zinc-400 border-slate-200 dark:border-zinc-700';
    }
  };

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-slate-50 dark:bg-zinc-900 text-slate-800 dark:text-zinc-100 transition-colors duration-300">
        
        {/* HEADER */}
        <header className="sticky top-0 z-50 bg-emerald-600 dark:bg-emerald-800 text-white shadow-md border-b-4 border-amber-400 transition-colors">
          <div className="max-w-md mx-auto px-4 py-3 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🇧🇷</span>
              <h1 className="font-black text-xl tracking-tight">Estudar<span className="text-amber-300">BR</span></h1>
            </div>
            <button 
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-full bg-emerald-700 dark:bg-emerald-900 hover:bg-emerald-500 transition-colors"
              aria-label="Toggle Theme"
            >
              {darkMode ? <Sun size={20} className="text-amber-300" /> : <Moon size={20} />}
            </button>
          </div>
        </header>

        {/* MAIN CONTAINER */}
        <main className="max-w-md mx-auto px-4 py-6 pb-24">
          
          {/* HERO SECTION */}
          <div className="mb-6">
            <h2 className="text-2xl font-extrabold mb-1 bg-gradient-to-r from-emerald-600 to-teal-500 dark:from-emerald-400 dark:to-teal-300 bg-clip-text text-transparent">
              Live Admission Tracker
            </h2>
            <p className="text-sm text-slate-500 dark:text-zinc-400">
              Monitored applications for Brazilian higher education programs.
            </p>
          </div>

          {/* SEARCH BAR */}
          <div className="relative mb-5">
            <Search className="absolute left-3 top-3.5 text-slate-400 dark:text-zinc-500" size={18} />
            <input 
              type="text" 
              placeholder="Search active courses or universities..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 font-medium transition-all"
            />
          </div>

          {/* REGIONAL FILTERS */}
          <div className="mb-6">
            <div className="flex gap-2 overflow-x-auto no-scrollbar pb-1">
              {["All", "Norte", "Nordeste", "Sudeste", "Sul"].map((region) => (
                <button
                  key={region}
                  onClick={() => setSelectedRegion(region)}
                  className={`px-4 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all border ${
                    selectedRegion === region
                      ? "bg-amber-400 text-slate-900 border-amber-400 shadow-sm font-extrabold scale-105"
                      : "bg-white dark:bg-zinc-800 text-slate-600 dark:text-zinc-400 border-slate-200 dark:border-zinc-700 hover:border-emerald-500"
                  }`}
                >
                  {region}
                </button>
              ))}
            </div>
          </div>

          {/* RESULTS */}
          <div className="space-y-4">
            {filteredPrograms.length > 0 ? (
              filteredPrograms.map((program) => (
                <div 
                  key={program.id}
                  className="bg-white dark:bg-zinc-800 border border-slate-100 dark:border-zinc-700/60 rounded-2xl p-4 shadow-sm hover:shadow-md transition-all border-l-4 border-l-emerald-500 dark:border-l-emerald-400 flex flex-col justify-between"
                >
                  <div>
                    {/* TOP BADGE BAR */}
                    <div className="flex justify-between items-center gap-2 mb-3">
                      <span className={`text-[10px] font-black uppercase tracking-wider px-2.5 py-1 rounded-md border ${getStatusStyles(program.status)}`}>
                        ● {program.status}
                      </span>
                      <div className="flex items-center gap-1 text-xs font-bold text-slate-500 dark:text-zinc-400 bg-slate-100 dark:bg-zinc-700/60 px-2 py-0.5 rounded-full">
                        <MapPin size={12} className="text-amber-500" />
                        {program.state}
                      </div>
                    </div>
                    
                    {/* PROGRAM INFO */}
                    <h4 className="font-bold text-base text-slate-900 dark:text-zinc-100 mb-1 leading-tight flex items-start gap-1.5">
                      <GraduationCap size={18} className="text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                      {program.program}
                    </h4>
                    
                    <p className="text-xs font-medium text-slate-500 dark:text-zinc-400 mb-3 pl-6">
                      {program.university}
                    </p>

                    {/* DYNAMIC TIMELINE META */}
                    <div className="flex items-center gap-2 pl-6 mb-4 text-xs font-semibold text-slate-400 dark:text-zinc-500">
                      <Calendar size={14} className="shrink-0" />
                      <span>Deadline: <strong className="text-slate-600 dark:text-zinc-300 font-bold">{program.deadline}</strong></span>
                    </div>
                  </div>

                  {/* ACTION BUTTON */}
                  <a 
                    href={program.link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="w-full py-2.5 px-4 bg-slate-900 dark:bg-zinc-700 hover:bg-emerald-600 dark:hover:bg-emerald-600 text-white font-bold text-xs rounded-xl flex items-center justify-center gap-2 transition-all group"
                  >
                    Open Application Link
                    <ExternalLink size={14} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                  </a>
                </div>
              ))
            ) : (
              <div className="text-center py-12 bg-white dark:bg-zinc-800 rounded-2xl border border-dashed border-slate-200 dark:border-zinc-700">
                <AlertCircle className="mx-auto text-slate-300 mb-2" size={28} />
                <p className="text-sm font-semibold text-slate-400 dark:text-zinc-500">No programs match your filters.</p>
              </div>
            )}
          </div>
        </main>

      </div>
    </div>
  );
}