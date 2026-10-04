import { Route, Routes } from 'react-router-dom';
import { TopNav } from './components/TopNav';
import DashboardPage from './pages/DashboardPage';
import LandingPage from './pages/LandingPage';
import MeetingDetailPage from './pages/MeetingDetailPage';
import UploadPage from './pages/UploadPage';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100">
      <TopNav />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/meetings/:id" element={<MeetingDetailPage />} />
        <Route path="/demo" element={<DashboardPage />} />
      </Routes>
    </div>
  );
}
