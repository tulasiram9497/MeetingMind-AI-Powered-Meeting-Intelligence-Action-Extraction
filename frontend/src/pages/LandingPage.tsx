import { ArrowRight, Bot, BrainCircuit, FileText, Search, Sparkles, Target } from 'lucide-react';
import { Link } from 'react-router-dom';

const features = [
  { icon: Sparkles, title: 'AI Summaries', text: 'Turn raw transcripts into executive summaries and structured insights.' },
  { icon: Target, title: 'Action Items', text: 'Extract tasks, owners, deadlines, and follow-ups with context.' },
  { icon: FileText, title: 'Decision Tracking', text: 'Capture decisions, risks, and open questions with traceable timestamps.' },
  { icon: Search, title: 'Semantic Search', text: 'Search meetings by meaning, not just keyword matches.' },
  { icon: Bot, title: 'Ask Your Meeting', text: 'Chat with the transcript using grounded retrieval and citation-backed answers.' },
  { icon: BrainCircuit, title: 'Meeting Analytics', text: 'Understand sentiment, topics, and outcomes from every conversation.' },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <main className="mx-auto max-w-6xl px-6 py-20">
        <div className="grid items-center gap-12 lg:grid-cols-[1.2fr_0.8fr]">
          <div>
            <div className="mb-6 inline-flex items-center rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-medium text-slate-700">
              Demo mode enabled
            </div>
            <h1 className="max-w-xl text-5xl font-semibold tracking-tight text-slate-950">
              Turn conversations into decisions.
            </h1>
            <p className="mt-5 max-w-lg text-lg text-slate-600">
              Upload a meeting. Extract the summary, action items, decisions, and knowledge you can actually act on.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link to="/upload" className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-5 py-3 text-sm font-medium text-white">
                Analyze a Meeting
                <ArrowRight size={16} />
              </Link>
              <Link to="/dashboard" className="rounded-full border border-slate-300 bg-white px-5 py-3 text-sm font-medium text-slate-700">
                View dashboard
              </Link>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
            <div className="space-y-4">
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                <div className="text-xs uppercase tracking-widest text-slate-500">Capture</div>
                <div className="mt-2 text-lg font-medium">Audio and transcript intake</div>
              </div>
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                <div className="text-xs uppercase tracking-widest text-slate-500">Understand</div>
                <div className="mt-2 text-lg font-medium">AI summaries and semantic retrieval</div>
              </div>
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                <div className="text-xs uppercase tracking-widest text-slate-500">Act</div>
                <div className="mt-2 text-lg font-medium">Action items, decisions, and next steps</div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-20 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          {features.map(({ icon: Icon, title, text }) => (
            <div key={title} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-slate-100 text-slate-900">
                <Icon size={18} />
              </div>
              <h3 className="text-xl font-medium text-slate-900">{title}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-600">{text}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
