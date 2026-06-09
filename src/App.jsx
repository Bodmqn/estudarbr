import React, { useState, useMemo } from 'react';
import { Sun, Moon, Search, MapPin, ExternalLink, GraduationCap, Calendar, AlertCircle, Award, CheckCircle, XCircle, Grid, SlidersHorizontal } from 'lucide-react';

import initialPrograms from '../discovered_programs.json';

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRegion, setSelectedRegion] = useState("All");
  const [statusFilter, setStatusFilter] = useState("All");

  const stats = useMemo(() => {
    const total = initialPrograms.length;
    const open = initialPrograms.filter(p => p.status === 'Open').length;
    const closed = initialPrograms.filter(p => p.status === 'Closed').length;
    return { total, open, closed };
  }, []);

  const filteredPrograms = useMemo(() => {
    return initialPrograms.filter(program => {
      const matchesSearch = 
        program.program.toLowerCase().includes(searchTerm.toLowerCase()) ||
        program.university.toLowerCase().includes(searchTerm.toLowerCase()) ||
        program.state.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesRegion = selectedRegion === "All" || program.region === selectedRegion;
      const matchesStatus = statusFilter === "All" || program.status === statusFilter;
      
      return matchesSearch && matchesRegion && matchesStatus;
    });
  }, [searchTerm, selectedRegion, statusFilter]);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Open':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-400 border border-emerald-200/60 dark:border-emerald-800/50 shadow-sm">
            <CheckCircle size={12} /> Open
          </span>
        );
      case 'Closed':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-50 dark:bg-rose-950/30 text-rose-700 dark:text-rose-400 border border-rose-200/60 dark:border-rose-800/50">
            <XCircle size={12} /> Closed
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-400 border border-amber-200/60 dark:border-amber-800/50">
            <AlertCircle size={12} /> Check Portal
          </span>
        );
    }
  };

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-slate-50/60 dark:bg-zinc-950 text-slate-800 dark:text-zinc-100 font-sans transition-colors duration-300">
        
        <header className="sticky top-0 z-50 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-md shadow-sm border-b border-slate-200/80 dark:border-zinc-800 transition-colors">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center shadow-md shadow-emerald-500/20 text-white font-serif font-black text-xl">E</div>
              <div>
                <h1 className="font-serif font-black text-2xl tracking-tight bg-gradient-to-r from-slate-900 via-emerald-800 to-slate-900 dark:from-white dark:via-emerald-400 dark:to-white bg-clip-text text-transparent">
                  Estudar<span className="font-sans font-light text-emerald-600 dark:text-emerald-400">BR</span>
                </h1>
                <p className="text-[10px] uppercase font-bold tracking-widest text-slate-400 dark:text-zinc-500">National Academic Registry</p>
              </div>
            </div>
            <button 
              onClick={() => setDarkMode(!darkMode)}
              className="p-2.5 rounded-xl border border-slate-200 dark:border-zinc-800 bg-slate-50 dark:bg-zinc-900 text-slate-500 dark:text-zinc-400 transition-all"
            >
              {darkMode ? <Sun size={18} className="text-amber-400" /> : <Moon size={18} />}
            </button>
          </div>
        </header>

        <div className="bg-gradient-to-b from-slate-100 to-transparent dark:from-zinc-900/40 py-10 border-b border-slate-100 dark:border-zinc-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center sm:text-left">
            <h2 className="font-serif font-bold text-3xl sm:text-4xl text-slate-900 dark:text-white leading-tight">Higher Education Admissions Portal</h2>
            <p className="mt-2 text-base text-slate-500 dark:text-zinc-400 max-w-2xl font-medium">
              Real-time monitoring system cross-referencing enrollment window statuses across federal, state, and regional Brazilian universities.
            </p>
          </div>
        </div>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <section className="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-10">
            <div className="bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-slate-200/60 dark:border-zinc-800 shadow-sm flex items-center gap-4">
              <div className="p-3 rounded-xl bg-slate-50 dark:bg-zinc-800 text-slate-600 dark:text-zinc-400 shadow-sm"><Grid size={22}/></div>
              <div>
                <p className="text-xs font-bold text-slate-400 dark:text-zinc-500 uppercase tracking-wider">Monitored Portals</p>
                <p className="text-2xl font-black text-slate-900 dark:text-white mt-0.5">{stats.total}</p>
              </div>
            </div>
            <div className="bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-slate-200/60 dark:border-zinc-800 shadow-sm flex items-center gap-4">
              <div className="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/20 text-emerald-600 dark:text-emerald-400 shadow-sm"><Award size={22}/></div>
              <div>
                <p className="text-xs font-bold text-slate-400 dark:text-zinc-500 uppercase tracking-wider">Active Windows</p>
                <p className="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-0.5">{stats.open}</p>
              </div>
            </div>
            <div className="bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-slate-200/60 dark:border-zinc-800 shadow-sm flex items-center gap-4">
              <div className="p-3 rounded-xl bg-rose-50 dark:bg-rose-950/20 text-rose-600 dark:text-rose-400 shadow-sm"><XCircle size={22}/></div>
              <div>
                <p className="text-xs font-bold text-slate-400 dark:text-zinc-500 uppercase tracking-wider">Closed Windows</p>
                <p className="text-2xl font-black text-rose-600 dark:text-rose-400 mt-0.5">{stats.closed}</p>
              </div>
            </div>
          </section>

          <section className="bg-white dark:bg-zinc-900 p-6 rounded-2xl border border-slate-200/80 dark:border-zinc-800 shadow-sm space-y-6 mb-8">
            <div className="flex flex-col md:flex-row gap-4 items-stretch md:items-center justify-between">
              <div className="relative flex-1">
                <Search className="absolute left-4 top-3.5 text-slate-400 dark:text-zinc-500" size={18} />
                <input 
                  type="text" 
                  placeholder="Filter by program name, institution acronym, or state..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 dark:border-zinc-800 bg-slate-50 dark:bg-zinc-950 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none text-sm shadow-inner"
                />
              </div>
              <div className="flex items-center gap-2 border-l border-slate-100 dark:border-zinc-800 pl-0 md:pl-4">
                <SlidersHorizontal size={16} className="text-slate-400" />
                <select 
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="bg-slate-50 dark:bg-zinc-950 border border-slate-200 dark:border-zinc-800 text-xs font-bold p-3 rounded-xl focus:outline-none text-slate-700 dark:text-zinc-300 cursor-pointer"
                >
                  <option value="All">All Application Statuses</option>
                  <option value="Open">Status: Open Only</option>
                  <option value="Closed">Status: Closed Only</option>
                  <option value="Check Portal">Status: Manual Check</option>
                </select>
              </div>
            </div>

            <div className="border-t border-slate-100 dark:border-zinc-800/60 pt-4 flex flex-wrap items-center gap-2">
              <span className="text-xs font-bold text-slate-400 dark:text-zinc-500 uppercase tracking-wider mr-2">Region Filter:</span>
              {["All", "Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"].map((region) => (
                <button
                  key={region}
                  onClick={() => setSelectedRegion(region)}
                  className={`px-4 py-2 rounded-xl text-xs font-bold border transition-all ${
                    selectedRegion === region
                      ? "bg-slate-900 dark:bg-white text-white dark:text-slate-900 border-slate-900 dark:border-white shadow-sm font-extrabold"
                      : "bg-slate-50 dark:bg-zinc-950 text-slate-600 dark:text-zinc-400 border-slate-200 dark:border-zinc-800"
                  }`}
                >
                  {region}
                </button>
              ))}
            </div>
          </section>

          <section>
            {filteredPrograms.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredPrograms.map((program) => (
                  <article 
                    key={program.id}
                    className="bg-white dark:bg-zinc-900 border border-slate-200/50 dark:border-zinc-800/60 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all flex flex-col justify-between group relative overflow-hidden"
                  >
                    <div>
                      <div className="flex justify-between items-start gap-2 mb-4">
                        {getStatusBadge(program.status)}
                        <div className="flex items-center gap-1 text-[11px] font-black tracking-wider text-slate-500 dark:text-zinc-400 bg-slate-100 dark:bg-zinc-800 px-2.5 py-1 rounded-md border border-slate-200/30 dark:border-zinc-700/30">
                          <MapPin size={11} className="text-emerald-600 dark:text-emerald-400" />
                          {program.state} • {program.region}
                        </div>
                      </div>
                      
                      <h3 className="font-serif font-bold text-lg text-slate-900 dark:text-zinc-100 mb-1.5 group-hover:text-emerald-700 dark:group-hover:text-emerald-400 transition-colors leading-snug flex items-start gap-2">
                        <GraduationCap size={20} className="text-slate-400 shrink-0 mt-0.5" />
                        {program.program}
                      </h3>
                      
                      <p className="text-xs font-semibold text-slate-500 dark:text-zinc-400 mb-4 pl-7">
                        {program.university}
                      </p>
                    </div>

                    <div>
                      <div className="border-t border-slate-100 dark:border-zinc-800/60 pt-3.5 mt-2 mb-4 flex items-center justify-between text-xs pl-1">
                        <span className="flex items-center gap-1.5 font-medium text-slate-400 dark:text-zinc-500">
                          <Calendar size={14} /> Deadline Info
                        </span>
                        <strong className="text-slate-700 dark:text-zinc-300 font-bold bg-slate-50 dark:bg-zinc-950 px-2 py-0.5 rounded border border-slate-100 dark:border-zinc-800">
                          {program.deadline}
                        </strong>
                      </div>

                      <a 
                        href={program.link} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="w-full py-3 px-4 bg-slate-50 dark:bg-zinc-950 group-hover:bg-emerald-600 text-slate-700 dark:text-zinc-300 group-hover:text-white font-bold text-xs rounded-xl flex items-center justify-center gap-2 border border-slate-200 dark:border-zinc-800 transition-all shadow-sm"
                      >
                        Access Examination Portal
                        <ExternalLink size={14} className="opacity-60 group-hover:opacity-100" />
                      </a>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <div className="text-center py-20 bg-white dark:bg-zinc-900 rounded-3xl border border-dashed border-slate-200 dark:border-zinc-800 max-w-lg mx-auto">
                <div className="w-12 h-12 rounded-full bg-slate-50 dark:bg-zinc-950 border border-slate-100 dark:border-zinc-800 flex items-center justify-center mx-auto mb-4 text-slate-400">
                  <AlertCircle size={24} />
                </div>
                <h4 className="text-base font-bold text-slate-900 dark:text-white mb-1">No Academic Listings Located</h4>
                <p className="text-xs font-medium text-slate-400 dark:text-zinc-500 px-6">
                  There are no active admissions paths fitting your applied search parameters.
                </p>
              </div>
            )}
          </section>
        </main>

        <footer className="bg-white dark:bg-zinc-900 border-t border-slate-200/80 dark:border-zinc-800 mt-20 text-center py-6 text-xs font-semibold text-slate-400 dark:text-zinc-500 tracking-tight">
          © {new Date().getFullYear()} EstudarBR Portal • Dynamic Automation Engine Enabled
        </footer>

      </div>
    </div>
  );
}
