import { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Checkbox } from './ui/checkbox';
import { Download, Plus, Trash2, CheckCircle2 } from 'lucide-react';
import { ActionPlan } from '../types';
import { motion } from 'motion/react';

interface ActionPlanCreatorProps {
  entryId: string;
  existingPlan?: ActionPlan;
  onSave: (steps: string[]) => void;
}

export function ActionPlanCreator({ entryId, existingPlan, onSave }: ActionPlanCreatorProps) {
  const [steps, setSteps] = useState<string[]>(existingPlan?.steps || ['']);
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());

  const addStep = () => {
    setSteps([...steps, '']);
  };

  const updateStep = (index: number, value: string) => {
    const newSteps = [...steps];
    newSteps[index] = value;
    setSteps(newSteps);
  };

  const removeStep = (index: number) => {
    setSteps(steps.filter((_, i) => i !== index));
    const newCompleted = new Set(completedSteps);
    newCompleted.delete(index);
    setCompletedSteps(newCompleted);
  };

  const toggleStep = (index: number) => {
    const newCompleted = new Set(completedSteps);
    if (newCompleted.has(index)) {
      newCompleted.delete(index);
    } else {
      newCompleted.add(index);
    }
    setCompletedSteps(newCompleted);
  };

  const handleSave = () => {
    const validSteps = steps.filter(step => step.trim() !== '');
    if (validSteps.length > 0) {
      onSave(validSteps);
    }
  };

  const handleExportPDF = () => {
    // Mock PDF export functionality
    const content = `
PERSONAREFLECT ACTION PLAN
Generated: ${new Date().toLocaleDateString()}

Your Action Steps:
${steps.map((step, i) => `${i + 1}. ${step}`).join('\n')}
    `.trim();

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `action-plan-${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Card className="p-6 bg-gradient-to-br from-indigo-50 to-purple-50 border-2 border-indigo-200">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <CheckCircle2 className="w-6 h-6 text-indigo-600" />
          <h2 className="text-slate-800">Your Action Plan</h2>
        </div>
        {existingPlan && (
          <Button
            onClick={handleExportPDF}
            variant="outline"
            size="sm"
            className="border-indigo-300 text-indigo-700 hover:bg-indigo-100"
          >
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
        )}
      </div>

      <div className="space-y-3 mb-4">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-start space-x-3"
          >
            {existingPlan && (
              <Checkbox
                checked={completedSteps.has(index)}
                onCheckedChange={() => toggleStep(index)}
                className="mt-3"
              />
            )}
            <div className="flex-1">
              <Input
                value={step}
                onChange={(e) => updateStep(index, e.target.value)}
                placeholder={`Step ${index + 1}: What action will you take?`}
                className="bg-white border-indigo-200 focus:border-indigo-400"
                disabled={existingPlan !== undefined}
              />
            </div>
            {!existingPlan && steps.length > 1 && (
              <Button
                onClick={() => removeStep(index)}
                variant="ghost"
                size="icon"
                className="text-slate-400 hover:text-red-500"
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            )}
          </motion.div>
        ))}
      </div>

      {!existingPlan && (
        <div className="flex space-x-2">
          <Button
            onClick={addStep}
            variant="outline"
            className="flex-1 border-indigo-300 text-indigo-700 hover:bg-indigo-100"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Step
          </Button>
          <Button
            onClick={handleSave}
            disabled={steps.every(s => s.trim() === '')}
            className="flex-1 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600"
          >
            Save Action Plan
          </Button>
        </div>
      )}

      {existingPlan && completedSteps.size > 0 && (
        <div className="mt-4 p-3 bg-white/50 rounded-lg">
          <p className="text-sm text-slate-600">
            Progress: {completedSteps.size} of {steps.length} steps completed
          </p>
          <div className="mt-2 h-2 bg-slate-200 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${(completedSteps.size / steps.length) * 100}%` }}
              className="h-full bg-gradient-to-r from-indigo-500 to-purple-500"
            />
          </div>
        </div>
      )}
    </Card>
  );
}
