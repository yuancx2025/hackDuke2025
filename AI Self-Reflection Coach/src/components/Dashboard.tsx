import { Card } from './ui/card';
import { Button } from './ui/button';
import { JournalEntry } from '../types';
import { Calendar, MessageSquare, CheckCircle2, ArrowRight } from 'lucide-react';
import { motion } from 'motion/react';

interface DashboardProps {
  entries: JournalEntry[];
  onSelectEntry: (id: string) => void;
}

export function Dashboard({ entries, onSelectEntry }: DashboardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    }).format(date);
  };

  const truncateDilemma = (text: string, maxLength: number = 120) => {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength) + '...';
  };

  if (entries.length === 0) {
    return (
      <Card className="p-12 text-center bg-white/50 backdrop-blur-sm border-slate-200">
        <div className="max-w-md mx-auto space-y-4">
          <div className="w-16 h-16 mx-auto bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center">
            <MessageSquare className="w-8 h-8 text-blue-600" />
          </div>
          <h3 className="text-slate-800">No Journal Entries Yet</h3>
          <p className="text-slate-600">
            Start your self-reflection journey by sharing your first dilemma. Our AI personas are ready to provide diverse insights to help you grow.
          </p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-slate-800">Your Reflections</h2>
          <p className="text-slate-600">
            {entries.length} {entries.length === 1 ? 'entry' : 'entries'}
          </p>
        </div>
      </div>

      <div className="grid gap-4">
        {entries.map((entry, index) => (
          <motion.div
            key={entry.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="p-6 bg-white/70 backdrop-blur-sm border-slate-200 hover:border-blue-300 transition-colors cursor-pointer group">
              <div onClick={() => onSelectEntry(entry.id)}>
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-2 text-sm text-slate-500">
                    <Calendar className="w-4 h-4" />
                    <span>{formatDate(entry.date)}</span>
                  </div>
                  {entry.actionPlan && (
                    <div className="flex items-center space-x-1 text-sm text-emerald-600">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>Action Plan Created</span>
                    </div>
                  )}
                </div>

                <p className="text-slate-700 mb-4 leading-relaxed">
                  {truncateDilemma(entry.dilemma)}
                </p>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="flex -space-x-2">
                      {entry.responses.map((response, i) => (
                        <div
                          key={i}
                          className="w-8 h-8 rounded-full bg-white border-2 border-slate-200 flex items-center justify-center text-sm"
                          title={response.name}
                        >
                          {response.icon}
                        </div>
                      ))}
                    </div>
                    <span className="text-sm text-slate-600">
                      {entry.responses.length} perspectives
                    </span>
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-blue-600 group-hover:text-blue-700"
                  >
                    View Details
                    <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
