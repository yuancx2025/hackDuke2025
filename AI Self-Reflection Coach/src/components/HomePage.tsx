import { Button } from './ui/button';
import { Card } from './ui/card';
import { Sparkles, Brain, Heart, Target, Flower2 } from 'lucide-react';
import { motion } from 'motion/react';

interface HomePageProps {
  onStartJournal: () => void;
}

export function HomePage({ onStartJournal }: HomePageProps) {
  const personas = [
    {
      icon: <Brain className="w-8 h-8" />,
      name: 'Dr. Chen',
      title: 'Cognitive-Behavioral Coach',
      description: 'Helps you identify thought patterns and develop practical strategies for change',
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: <Heart className="w-8 h-8" />,
      name: 'Maya',
      title: 'Empathetic Friend',
      description: 'Provides emotional support and validation as you navigate challenges',
      color: 'from-pink-500 to-rose-600'
    },
    {
      icon: <Target className="w-8 h-8" />,
      name: 'Alex',
      title: 'Rational Analyst',
      description: 'Offers structured, data-driven approaches to problem-solving',
      color: 'from-emerald-500 to-teal-600'
    },
    {
      icon: <Flower2 className="w-8 h-8" />,
      name: 'Sage',
      title: 'Mindfulness Mentor',
      description: 'Guides you toward present-moment awareness and inner wisdom',
      color: 'from-purple-500 to-indigo-600'
    }
  ];

  return (
    <div className="space-y-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-6 py-12"
      >
        <div className="flex justify-center">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl flex items-center justify-center">
            <Sparkles className="w-12 h-12 text-white" />
          </div>
        </div>
        <div className="space-y-2">
          <h1 className="text-slate-800">Get Diverse Insights on Personal Dilemmas</h1>
          <p className="text-slate-600 max-w-2xl mx-auto">
            Share your challenges and receive personalized guidance from four distinct AI personas. 
            Combine their wisdom into actionable steps for personal growth.
          </p>
        </div>
        <Button
          onClick={onStartJournal}
          size="lg"
          className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
        >
          <Sparkles className="w-5 h-5 mr-2" />
          Start Your Reflection
        </Button>
      </motion.div>

      <div>
        <h2 className="text-slate-800 text-center mb-8">Meet Your AI Coaches</h2>
        <div className="grid gap-6 md:grid-cols-2">
          {personas.map((persona, index) => (
            <motion.div
              key={persona.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + index * 0.1 }}
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-slate-200 hover:border-blue-300 transition-colors">
                <div className="flex items-start space-x-4">
                  <div className={`w-14 h-14 bg-gradient-to-br ${persona.color} rounded-xl flex items-center justify-center text-white flex-shrink-0`}>
                    {persona.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-slate-800 mb-1">{persona.name}</h3>
                    <p className="text-sm text-slate-600 mb-2">{persona.title}</p>
                    <p className="text-sm text-slate-600">{persona.description}</p>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <Card className="p-8 bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200">
          <div className="text-center space-y-4">
            <h2 className="text-slate-800">How It Works</h2>
            <div className="grid gap-6 md:grid-cols-3 text-left">
              <div className="space-y-2">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center text-white">
                  1
                </div>
                <h3 className="text-slate-800">Share Your Dilemma</h3>
                <p className="text-sm text-slate-600">
                  Write about a challenge, decision, or situation you're facing
                </p>
              </div>
              <div className="space-y-2">
                <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg flex items-center justify-center text-white">
                  2
                </div>
                <h3 className="text-slate-800">Receive Diverse Insights</h3>
                <p className="text-sm text-slate-600">
                  Get personalized responses from four unique AI perspectives
                </p>
              </div>
              <div className="space-y-2">
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-lg flex items-center justify-center text-white">
                  3
                </div>
                <h3 className="text-slate-800">Create Your Action Plan</h3>
                <p className="text-sm text-slate-600">
                  Synthesize insights into concrete steps and track your progress
                </p>
              </div>
            </div>
          </div>
        </Card>
      </motion.div>
    </div>
  );
}
