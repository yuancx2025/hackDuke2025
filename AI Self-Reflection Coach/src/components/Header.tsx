import { Button } from './ui/button';
import { Sparkles, BookOpen, Home } from 'lucide-react';

interface HeaderProps {
  currentView: 'home' | 'new-entry' | 'dashboard' | 'entry-detail';
  onNavigate: (view: 'home' | 'new-entry' | 'dashboard') => void;
}

export function Header({ currentView, onNavigate }: HeaderProps) {
  return (
    <header className="border-b border-slate-200 bg-white/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <button
            onClick={() => onNavigate('home')}
            className="flex items-center space-x-2 group"
          >
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center group-hover:scale-105 transition-transform">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div className="text-left">
              <h1 className="text-slate-800">PersonaReflect</h1>
              <p className="text-sm text-slate-500">Your AI Self-Reflection Coach</p>
            </div>
          </button>

          <nav className="flex items-center space-x-2">
            <Button
              variant={currentView === 'home' ? 'default' : 'ghost'}
              onClick={() => onNavigate('home')}
              className={currentView === 'home' ? 'bg-gradient-to-r from-blue-500 to-purple-500' : ''}
            >
              <Home className="w-4 h-4 mr-2" />
              Home
            </Button>
            <Button
              variant={currentView === 'dashboard' ? 'default' : 'ghost'}
              onClick={() => onNavigate('dashboard')}
              className={currentView === 'dashboard' ? 'bg-gradient-to-r from-blue-500 to-purple-500' : ''}
            >
              <BookOpen className="w-4 h-4 mr-2" />
              Dashboard
            </Button>
          </nav>
        </div>
      </div>
    </header>
  );
}
