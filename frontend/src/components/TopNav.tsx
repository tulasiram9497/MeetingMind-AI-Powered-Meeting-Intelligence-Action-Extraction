import { ArrowRight, BrainCircuit, Menu } from 'lucide-react';
import { Link } from 'react-router-dom';

export function TopNav() {
  return (
    <header className="border-b border-slate-200 bg-white/80 backdrop-blur-sm">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link to="/" className="flex items-center gap-3 font-semibold text-slate-900">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-900 text-white">
            <BrainCircuit size={18} />
          </span>
          MeetingMind
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-slate-600 md:flex">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/upload">Upload</Link>
          <Link to="/demo">Demo</Link>
        </nav>
        <Link to="/upload" className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white">
          Analyze a Meeting
          <ArrowRight size={16} />
        </Link>
      </div>
    </header>
  );
}
