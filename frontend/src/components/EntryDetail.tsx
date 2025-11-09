import { Card } from './ui/card';
import { Button } from './ui/button';
import { JournalEntry } from '../types';
import { PersonaCard } from './PersonaCard';
import { ActionPlanCreator } from './ActionPlanCreator';
import { ArrowLeft, Calendar } from 'lucide-react';
import { motion } from 'motion/react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface EntryDetailProps {
  entry: JournalEntry;
  onBack: () => void;
  onSaveActionPlan: (entryId: string, steps: string[]) => void;
}

export function EntryDetail({ entry, onBack, onSaveActionPlan }: EntryDetailProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    }).format(date);
  };

  return (
    <div className="space-y-6">
      <Button
        onClick={onBack}
        variant="ghost"
        className="text-slate-600 hover:text-slate-800"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back to Dashboard
      </Button>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <Card className="p-6 bg-white/70 backdrop-blur-sm border-slate-200">
          <div className="flex items-center space-x-2 text-sm text-slate-500 mb-4">
            <Calendar className="w-4 h-4" />
            <span>{formatDate(entry.date)}</span>
          </div>
          <h2 className="text-slate-800 mb-2">Your Dilemma</h2>
          <p className="text-slate-700 leading-relaxed">{entry.dilemma}</p>
        </Card>
      </motion.div>

      <div>
        <h2 className="text-slate-800 mb-4">Insights from Your AI Coaches</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {entry.responses.map((response, index) => (
            <PersonaCard
              key={response.persona}
              response={response}
              delay={index * 0.1}
            />
          ))}
        </div>
      </div>

      {entry.suggestedActions && entry.suggestedActions.length > 0 && (
        <div className="mt-6">
          <h2 className="text-slate-800 mb-4">Suggested Actions</h2>
          <Card className="p-6 bg-gradient-to-br from-white to-slate-50 border-slate-200">
            <div className="text-slate-700 leading-relaxed prose prose-sm">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {entry.suggestedActions.map((s) => `- ${s}`).join('\n')}
              </ReactMarkdown>
            </div>
          </Card>
        </div>
      )}

      <div>
        <h2 className="text-slate-800 mb-4">
          {entry.actionPlan ? 'Your Action Plan' : 'Create Your Action Plan'}
        </h2>
        <ActionPlanCreator
          entryId={entry.id}
          existingPlan={entry.actionPlan}
          onSave={(steps) => onSaveActionPlan(entry.id, steps)}
        />
      </div>
    </div>
  );
}
