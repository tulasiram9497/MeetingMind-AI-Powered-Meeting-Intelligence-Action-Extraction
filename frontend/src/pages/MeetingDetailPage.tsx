import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchMeeting } from '../services/api';
import { Meeting } from '../types';

export default function MeetingDetailPage() {
  const { id } = useParams();
  const [meeting, setMeeting] = useState<Meeting | null>(null);

  useEffect(() => {
    if (!id) return;
    fetchMeeting(Number(id)).then((data) => setMeeting(data)).catch(() => setMeeting(null));
  }, [id]);

  if (!meeting) return <div className="p-10 text-center text-slate-500">Loading meeting...</div>;

  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Meeting</p>
            <h1 className="mt-2 text-3xl font-semibold text-slate-900">{meeting.title}</h1>
          </div>
          <div className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm text-slate-700">{meeting.status}</div>
        </div>
        <div className="mt-6 flex flex-wrap gap-4 text-sm text-slate-600">
          <span>Date: {meeting.created_at ? new Date(meeting.created_at).toLocaleDateString() : 'Today'}</span>
          <span>Duration: {meeting.duration || 28} min</span>
          <span>Status: {meeting.status}</span>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold text-slate-900">Executive summary</h2>
          <p className="text-slate-700">{meeting.summary || 'Meeting summary is currently being generated.'}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold text-slate-900">Key points</h2>
          <ul className="list-disc space-y-2 pl-5 text-slate-700">
            <li>Launch planning remains a top priority.</li>
            <li>Stakeholder review is required before final confirmation.</li>
            <li>Team ownership and follow-up tasks are tracking well.</li>
          </ul>
        </div>
      </div>

      <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">Transcript</h2>
        <div className="space-y-4 text-slate-700">
          <div><strong>Speaker 1</strong><div className="mt-1">We need to prepare the product launch plan for the upcoming release.</div></div>
          <div><strong>Speaker 2</strong><div className="mt-1">We agreed to finalize the proposal by Friday and confirm the timeline with stakeholders.</div></div>
        </div>
      </div>
    </div>
  );
}
