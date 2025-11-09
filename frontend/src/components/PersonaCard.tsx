import { Card } from './ui/card';
import { PersonaResponse } from '../types';
import { motion } from 'motion/react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface PersonaCardProps {
  response: PersonaResponse;
  delay?: number;
}

const personaColors = {
  'cognitive-behavioral': 'from-blue-50 to-blue-100 border-blue-200',
  'empathetic-friend': 'from-pink-50 to-rose-100 border-pink-200',
  'rational-analyst': 'from-emerald-50 to-teal-100 border-emerald-200',
  'mindfulness-mentor': 'from-purple-50 to-indigo-100 border-purple-200'
};

const personaTitles = {
  'cognitive-behavioral': 'Cognitive-Behavioral Coach',
  'empathetic-friend': 'Empathetic Friend',
  'rational-analyst': 'Rational Analyst',
  'mindfulness-mentor': 'Mindfulness Mentor'
};

export function PersonaCard({ response, delay = 0 }: PersonaCardProps) {
  const colorClass = personaColors[response.persona];
  const title = personaTitles[response.persona];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
    >
      <Card className={`p-6 bg-gradient-to-br ${colorClass} border-2`}>
        <div className="flex items-start space-x-3 mb-4">
          <div className="text-3xl">{response.icon}</div>
          <div>
            <h3 className="text-slate-800">{response.name}</h3>
            <p className="text-sm text-slate-600">{title}</p>
          </div>
        </div>
        <div className="text-slate-700 leading-relaxed prose prose-sm">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{response.response}</ReactMarkdown>
        </div>
      </Card>
    </motion.div>
  );
}
