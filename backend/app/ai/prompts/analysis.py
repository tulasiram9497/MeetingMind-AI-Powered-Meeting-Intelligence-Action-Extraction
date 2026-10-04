ANALYSIS_PROMPT = """
You are analyzing a meeting transcript. Only use information explicitly supported by the transcript.
If information is unavailable, say 'Not specified in the transcript.'
Do not invent names, decisions, deadlines, or commitments.
Return valid JSON with the following structure:
{
  'executive_summary': '',
  'detailed_summary': '',
  'key_points': [],
  'decisions': [],
  'action_items': [],
  'deadlines': [],
  'questions': [],
  'risks': [],
  'topics': [],
  'sentiment': {'overall': '', 'confidence': 0.0}
}
"""

EXTRACTION_PROMPT = """
Extract action items from the meeting transcript. Use evidence from the transcript only.
Return JSON with keys: task, assignee, deadline, priority, evidence.
If not specified, use 'Unassigned', 'Not specified', 'medium'.
"""

RAG_PROMPT = """
Answer ONLY from the supplied meeting context.
If the answer cannot be found in the context, say: 'I couldn't find that information in this meeting.'
Never invent information.
Include relevant source timestamps.
"""
