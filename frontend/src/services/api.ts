import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
});

export async function fetchMeetings() {
  const response = await api.get('/meetings');
  return response.data;
}

export async function uploadMeeting(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post('http://localhost:8000/meetings/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
}

export async function fetchMeeting(id: number) {
  const response = await api.get(`/meetings/${id}`);
  return response.data;
}

export async function updateActionItem(id: number, payload: Record<string, string>) {
  const response = await api.patch(`/action-items/${id}`, payload);
  return response.data;
}

export async function deleteMeeting(id: number) {
  const response = await api.delete(`/meetings/${id}`);
  return response.data;
}

export async function askMeeting(id: number, question: string) {
  const response = await api.post(`/meetings/${id}/ask`, { question });
  return response.data;
}

export default api;
