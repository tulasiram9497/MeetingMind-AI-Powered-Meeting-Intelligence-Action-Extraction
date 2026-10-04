import { UploadCloud } from 'lucide-react';
import { useState } from 'react';
import { uploadMeeting } from '../services/api';

export default function UploadPage() {
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('Idle');
  const [error, setError] = useState('');

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setError('');
    setStatus('Uploading');
    try {
      const result = await uploadMeeting(file);
      setStatus(result.status || 'Completed');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Unable to upload the meeting.');
      setStatus('Failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl px-6 py-12">
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-semibold text-slate-900">Drop your meeting here</h1>
          <p className="mt-2 text-slate-600">MP3 / WAV / M4A / MP4 / WEBM</p>
        </div>

        <label className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-300 bg-slate-50 p-12 text-center transition hover:border-slate-400">
          <UploadCloud className="mb-4 h-12 w-12 text-slate-500" />
          <span className="text-lg font-medium text-slate-800">or Browse files</span>
          <input type="file" className="hidden" onChange={handleUpload} accept=".mp3,.wav,.m4a,.mp4,.webm" />
        </label>

        <div className="mt-8 space-y-3">
          <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
            <span>Upload</span>
            <span>{uploading ? 'in progress' : 'ready'}</span>
          </div>
          <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
            <span>Processing</span>
            <span>{status}</span>
          </div>
        </div>

        {error && <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}
      </div>
    </div>
  );
}
