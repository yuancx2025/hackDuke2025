import { useState } from 'react';
import { Textarea } from './ui/textarea';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Sparkles } from 'lucide-react';

interface JournalInputProps {
  onSubmit: (dilemma: string) => void;
  isLoading?: boolean;
}

export function JournalInput({ onSubmit, isLoading = false }: JournalInputProps) {
  const [dilemma, setDilemma] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (dilemma.trim()) {
      onSubmit(dilemma);
    }
  };

  return (
    <Card className="p-6 bg-white/50 backdrop-blur-sm border-slate-200">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="dilemma" className="block text-slate-700">
            What's on your mind?
          </label>
          <Textarea
            id="dilemma"
            placeholder="Share your dilemma or challenge. Be as detailed as you'd like - the more context you provide, the more personalized insights you'll receive..."
            value={dilemma}
            onChange={(e) => setDilemma(e.target.value)}
            className="min-h-[200px] resize-none bg-white border-slate-200 focus:border-blue-300 focus:ring-blue-200"
            disabled={isLoading}
          />
        </div>
        <div className="flex items-center justify-between">
          <p className="text-sm text-slate-500">
            {dilemma.length} characters
          </p>
          <Button
            type="submit"
            disabled={!dilemma.trim() || isLoading}
            className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
          >
            <Sparkles className="w-4 h-4 mr-2" />
            {isLoading ? 'Getting Insights...' : 'Get Insights'}
          </Button>
        </div>
      </form>
    </Card>
  );
}
