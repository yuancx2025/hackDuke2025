import { useState } from 'react';
import { Header } from './components/Header';
import { HomePage } from './components/HomePage';
import { JournalInput } from './components/JournalInput';
import { PersonaCard } from './components/PersonaCard';
import { ActionPlanCreator } from './components/ActionPlanCreator';
import { Dashboard } from './components/Dashboard';
import { EntryDetail } from './components/EntryDetail';
import { Button } from './components/ui/button';
import { mockJournalEntries, generatePersonaResponses } from './lib/mockData';
import { JournalEntry, PersonaResponse } from './types';
import { ArrowLeft } from 'lucide-react';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner@2.0.3';

type View = 'home' | 'new-entry' | 'dashboard' | 'entry-detail';

export default function App() {
  const [currentView, setCurrentView] = useState<View>('home');
  const [journalEntries, setJournalEntries] = useState<JournalEntry[]>(mockJournalEntries);
  const [currentEntry, setCurrentEntry] = useState<JournalEntry | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentResponses, setCurrentResponses] = useState<PersonaResponse[]>([]);
  const [currentDilemma, setCurrentDilemma] = useState('');
  const [selectedEntryId, setSelectedEntryId] = useState<string | null>(null);

  const handleStartJournal = () => {
    setCurrentView('new-entry');
    setCurrentEntry(null);
    setCurrentResponses([]);
    setCurrentDilemma('');
  };

  const handleSubmitDilemma = async (dilemma: string) => {
    setIsGenerating(true);
    setCurrentDilemma(dilemma);
    
    // Simulate AI response generation
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const responses = generatePersonaResponses(dilemma);
    setCurrentResponses(responses);
    setIsGenerating(false);
    
    toast.success('Insights generated! Review the perspectives from your AI coaches.');
  };

  const handleSaveActionPlan = (entryId: string, steps: string[]) => {
    const actionPlan = {
      id: `ap-${Date.now()}`,
      entryId,
      steps,
      createdAt: new Date().toISOString()
    };

    setJournalEntries(entries =>
      entries.map(entry =>
        entry.id === entryId
          ? { ...entry, actionPlan }
          : entry
      )
    );

    if (selectedEntryId) {
      const updatedEntry = journalEntries.find(e => e.id === selectedEntryId);
      if (updatedEntry) {
        setCurrentEntry({ ...updatedEntry, actionPlan });
      }
    }

    toast.success('Action plan saved successfully!');
  };

  const handleCreateActionPlanForNew = (steps: string[]) => {
    const newEntry: JournalEntry = {
      id: `entry-${Date.now()}`,
      date: new Date().toISOString(),
      dilemma: currentDilemma,
      responses: currentResponses,
      actionPlan: {
        id: `ap-${Date.now()}`,
        entryId: `entry-${Date.now()}`,
        steps,
        createdAt: new Date().toISOString()
      }
    };

    setJournalEntries([newEntry, ...journalEntries]);
    toast.success('Journal entry and action plan saved!');
    setCurrentView('dashboard');
    setCurrentResponses([]);
    setCurrentDilemma('');
  };

  const handleSaveWithoutActionPlan = () => {
    const newEntry: JournalEntry = {
      id: `entry-${Date.now()}`,
      date: new Date().toISOString(),
      dilemma: currentDilemma,
      responses: currentResponses
    };

    setJournalEntries([newEntry, ...journalEntries]);
    toast.success('Journal entry saved!');
    setCurrentView('dashboard');
    setCurrentResponses([]);
    setCurrentDilemma('');
  };

  const handleSelectEntry = (id: string) => {
    const entry = journalEntries.find(e => e.id === id);
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
                      {currentResponses.map((response, index) => (
                        <PersonaCard
                          key={response.persona}
                          response={response}
                          delay={index * 0.1}
                        />
                      ))}
                    </div>
                  </div>

                  <div>
                    <h2 className="text-slate-800 mb-4">Create Your Action Plan</h2>
                    <ActionPlanCreator
                      entryId="new"
                      onSave={handleCreateActionPlanForNew}
                    />
                  </div>

                  <div className="flex justify-center">
                    <Button
                      onClick={handleSaveWithoutActionPlan}
                      variant="outline"
                      className="border-slate-300 text-slate-700"
                    >
                      Save Entry Without Action Plan
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
