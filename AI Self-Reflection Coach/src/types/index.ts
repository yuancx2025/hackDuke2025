export interface JournalEntry {
  id: string;
  date: string;
  dilemma: string;
  responses: PersonaResponse[];
  actionPlan?: ActionPlan;
}

export interface PersonaResponse {
  persona: 'cognitive-behavioral' | 'empathetic-friend' | 'rational-analyst' | 'mindfulness-mentor';
  name: string;
  response: string;
  icon: string;
}

export interface ActionPlan {
  id: string;
  entryId: string;
  steps: string[];
  createdAt: string;
}
