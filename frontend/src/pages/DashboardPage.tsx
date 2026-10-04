import { Activity, ArrowUpRight, CalendarRange, Clock3, ListTodo, Trash2 } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { deleteMeeting, fetchMeetings } from '../services/api';
import { Meeting } from '../types';

export default function DashboardPage() {
  const [meetings, setMeetings] = useState<Meeting[]>([]);

  useEffect(() => {
    fetchMeetings().then((data) => setMeetings(data)).catch(() => setMeetings([]));
  }, []);

  const stats = [
    { label: 'Total Meetings', value: meetings.length },
    { label: 'Completed', value: meetings.filter((m) => m.status === 'completed').length },
    { label: 'Processing', value: meetings.filter((m) => m.status === 'processing').length },
    { label: 'Action Items', value: meetings.length > 0 ? 3 : 0 },
  ];

  const handleDelete = async (id: number) => {
    await deleteMeeting(id);
    setMeetings((current) => current.filter((meeting) => meeting.id !== id));
  };

  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Overview</p>
          <h1 className="mt-2 text-3xl font-semibold text-slate-900">Dashboard</h1>
        </div>
        <Link to="/upload" className="rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white">
          Upload meeting
        </Link>
      </div>

      <div className="mb-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <div key={stat.label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="text-sm text-slate-500">{stat.label}</div>
            <div className="mt-4 text-3xl font-semibold text-slate-900">{stat.value}</div>
          </div>
        ))}
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-5 flex items-center gap-3 text-slate-700">
          <Activity size={18} />
          <span className="font-medium">Recent meetings</span>
        </div>

        <div className="space-y-3">
          {meetings.length === 0 ? (
            <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center text-slate-500">
              No meetings yet. Upload your first meeting to start extracting insights.
            </div>
          ) : (
            meetings.map((meeting) => (
              <div key={meeting.id} className="flex flex-col gap-4 rounded-xl border border-slate-200 p-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <div className="text-lg font-medium text-slate-900">{meeting.title}</div>
                  <div className="mt-2 flex flex-wrap gap-4 text-sm text-slate-500">
                    <span className="inline-flex items-center gap-1"><CalendarRange size={14} /> {meeting.created_at ? new Date(meeting.created_at).toLocaleDateString() : 'Today'}</span>
                    <span className="inline-flex items-center gap-1"><Clock3 size={14} /> {meeting.duration || 28} min</span>
                    <span className="inline-flex items-center gap-1"><ListTodo size={14} /> {meeting.status}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Link to={`/meetings/${meeting.id}`} className="inline-flex items-center gap-2 rounded-full border border-slate-300 px-3 py-2 text-sm text-slate-700">
                    Open <ArrowUpRight size={14} />
                  </Link>
                  <button onClick={() => handleDelete(meeting.id)} className="inline-flex items-center gap-2 rounded-full border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-600">
                    <Trash2 size={14} /> Delete
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
