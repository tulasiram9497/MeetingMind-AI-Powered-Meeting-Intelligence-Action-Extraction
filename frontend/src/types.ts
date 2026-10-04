export type MeetingStatus = 'uploaded' | 'processing' | 'transcribing' | 'analyzing' | 'completed' | 'failed';

export interface Meeting {
  id: number;
  title: string;
  original_filename: string;
  file_type: string;
  duration: number;
  status: MeetingStatus;
  created_at?: string;
  updated_at?: string;
  transcript?: string;
  summary?: string;
  detailed_summary?: string;
  sentiment?: string;
}

export interface ActionItem {
  id?: number;
  description: string;
  assignee: string;
  deadline: string;
  priority: 'low' | 'medium' | 'high';
  status: 'open' | 'in_progress' | 'completed';
  source_segment_id?: number | null;
}

export interface DecisionItem {
  id?: number;
  decision: string;
  context: string;
  source_segment_id?: number | null;
  timestamp: number;
}
