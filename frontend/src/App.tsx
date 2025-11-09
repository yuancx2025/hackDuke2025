import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { HomePage } from './components/HomePage';
import { JournalInput } from './components/JournalInput';
import { PersonaCard } from './components/PersonaCard';
import { ActionPlanCreator } from './components/ActionPlanCreator';
import { Dashboard } from './components/Dashboard';
import { EntryDetail } from './components/EntryDetail';
import { Button } from './components/ui/button';
import { JournalEntry, PersonaResponse } from './types';
import { Card } from './components/ui/card';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ArrowLeft } from 'lucide-react';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner';
import { api } from './services/api';

type View = 'home' | 'new-entry' | 'dashboard' | 'entry-detail';

export default function App() {
  const [currentView, setCurrentView] = useState<View>('home');
  const [journalEntries, setJournalEntries] = useState<JournalEntry[]>([]);
  const [currentEntry, setCurrentEntry] = useState<JournalEntry | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentResponses, setCurrentResponses] = useState<PersonaResponse[]>([]);
  const [currentDilemma, setCurrentDilemma] = useState('');
  const [currentSuggestedActions, setCurrentSuggestedActions] = useState<string[]>([]);
  const [selectedEntryId, setSelectedEntryId] = useState<string | null>(null);
  const [backendConnected, setBackendConnected] = useState<boolean | null>(null);

  // Check backend health on mount
  useEffect(() => {
    const checkBackend = async () => {
      const isHealthy = await api.checkHealth();
      setBackendConnected(isHealthy);
      if (isHealthy) {
        console.log('✅ Connected to PersonaReflect backend');
        toast.success('Connected to AI backend!');
      } else {
        console.log('⚠️ Backend not available, using mock data');
        toast.info('Backend not available. Using demo mode with sample data.');
      }
    };
    checkBackend();
  }, []);

  const handleStartJournal = () => {
    setCurrentView('new-entry');
    setCurrentEntry(null);
    setCurrentResponses([]);
    setCurrentDilemma('');
    setCurrentSuggestedActions([]);
  };

  const handleSubmitDilemma = async (dilemma: string) => {
    setIsGenerating(true);
    setCurrentDilemma(dilemma);
    
    try {
      // Use real API - it will automatically fall back to mock if backend unavailable
      const result = await api.getReflections(dilemma);
      setCurrentResponses(result.responses);
      setCurrentSuggestedActions(result.suggested_actions || []);
      setIsGenerating(false);
      
      toast.success('Insights generated! Review the perspectives from your AI coaches.');
    } catch (error) {
      console.error('Error getting reflections:', error);
      setIsGenerating(false);
      toast.error('Failed to get insights. Please try again.');
    }
  };

  const handleSaveActionPlan = (entryId: string, steps: string[]) => {
    const actionPlan = {
      id: `ap-${Date.now()}`,
      entryId,
      steps,
      createdAt: new Date().toISOString()
    };

    setJournalEntries((entries: JournalEntry[]) =>
      entries.map((entry: JournalEntry) =>
        entry.id === entryId
          ? { ...entry, actionPlan }
          : entry
      )
    );

    if (selectedEntryId) {
      const updatedEntry = journalEntries.find((e: JournalEntry) => e.id === selectedEntryId);
      if (updatedEntry) {
        setCurrentEntry({ ...updatedEntry, actionPlan });
      }
    }

    toast.success('Action plan saved successfully!');
  };

  const handleSaveWithoutActionPlan = () => {
    const newEntry: JournalEntry = {
      id: `entry-${Date.now()}`,
      date: new Date().toISOString(),
      dilemma: currentDilemma,
      responses: currentResponses,
      suggestedActions: currentSuggestedActions
    };

    setJournalEntries([newEntry, ...journalEntries]);
    toast.success('Journal entry saved!');
    setCurrentView('dashboard');
    setCurrentResponses([]);
    setCurrentDilemma('');
    setCurrentSuggestedActions([]);
  };

  const handleSelectEntry = (id: string) => {
    const entry = journalEntries.find((e: JournalEntry) => e.id === id);
    if (entry) {
      setCurrentEntry(entry);
      setSelectedEntryId(id);
      setCurrentView('entry-detail');
    }
  };

  const handleBackToDashboard = () => {
    setCurrentView('dashboard');
    setCurrentEntry(null);
    setSelectedEntryId(null);
  };

  const handleNavigate = (view: 'home' | 'new-entry' | 'dashboard') => {
    setCurrentView(view);
    if (view === 'new-entry') {
      handleStartJournal();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header currentView={currentView} onNavigate={handleNavigate} />
      
      <main className="max-w-6xl mx-auto px-4 py-8">
        {currentView === 'home' && (
          <HomePage onStartJournal={handleStartJournal} />
        )}

        {currentView === 'new-entry' && (
          <div className="space-y-8">
            {currentResponses.length === 0 ? (
              <>
                <div className="text-center space-y-2 mb-8">
                  <h2 className="text-slate-800">Share Your Dilemma</h2>
                  <p className="text-slate-600">
                    Be honest and detailed. The more context you provide, the more helpful the insights will be.
                  </p>
                </div>
                <JournalInput onSubmit={handleSubmitDilemma} isLoading={isGenerating} />
              </>
            ) : (
              <>
                <Button
                  onClick={() => {
                    setCurrentResponses([]);
                    setCurrentDilemma('');
                    setCurrentSuggestedActions([]);
                  }}
                  variant="ghost"
                  className="text-slate-600 hover:text-slate-800"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Start New Entry
                </Button>

                <div className="space-y-6">
                  <div>
                    <h2 className="text-slate-800 mb-4">Your Dilemma</h2>
                    <div className="p-6 bg-white/70 backdrop-blur-sm rounded-lg border border-slate-200">
                      <p className="text-slate-700 leading-relaxed">{currentDilemma}</p>
                    </div>
                  </div>

                          <div>
                            <h2 className="text-slate-800 mb-4">Insights from Your AI Coaches</h2>
                            <div className="grid gap-4 md:grid-cols-2">
                              {currentResponses.map((response: PersonaResponse, index: number) => (
                                <PersonaCard
                                  key={response.persona}
                                  response={response}
                                  delay={index * 0.1}
                                />
                              ))}
                            </div>
                          </div>

                          {currentSuggestedActions && currentSuggestedActions.length > 0 && (
                            <div className="mt-6">
                              <h2 className="text-slate-800 mb-4">Suggested Actions</h2>
                              <div className="grid gap-4 md:grid-cols-1">
                                <Card className="p-6 bg-gradient-to-br from-white to-slate-50 border-slate-200">
                                  <div className="text-slate-700 leading-relaxed prose prose-sm">
                                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                      {currentSuggestedActions.map((s) => `- ${s}`).join('\n')}
                                    </ReactMarkdown>
                                  </div>
                                </Card>
                              </div>
                            </div>
                          )}

                  <div className="flex justify-center mt-6">
                    <Button
                      onClick={handleSaveWithoutActionPlan}
                      className="bg-primary text-white hover:bg-primary/90"
                    >
                      Save Journal Entry
                    </Button>
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {currentView === 'dashboard' && (
          <Dashboard
            entries={journalEntries}
            onSelectEntry={handleSelectEntry}
          />
        )}

        {currentView === 'entry-detail' && currentEntry && (
          <EntryDetail
            entry={currentEntry}
            onBack={handleBackToDashboard}
            onSaveActionPlan={handleSaveActionPlan}
          />
        )}
      </main>

      <Toaster position="bottom-right" />
    </div>
  );
}
