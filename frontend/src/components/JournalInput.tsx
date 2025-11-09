// JournalInput.tsx
import { useState, useRef } from 'react';
import { Textarea } from './ui/textarea';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Sparkles, Mic, Square } from 'lucide-react';
import Recorder from 'recorder-js';
import { api } from '../services/api';

interface JournalInputProps {
  onSubmit: (dilemma: string) => void;
  isLoading?: boolean;
}

export function JournalInput({ onSubmit, isLoading = false }: JournalInputProps) {
  const [dilemma, setDilemma] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const audioContextRef = useRef<AudioContext | null>(null);
  const recorderRef = useRef<Recorder | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (dilemma.trim()) {
      onSubmit(dilemma);
    }
  };

  const handleRecordClick = async () => {
    if (!isRecording) {
      try {
        // 初始化 Recorder.js
        const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new Recorder(audioContext);
        await recorder.init(stream);

        recorderRef.current = recorder;
        audioContextRef.current = audioContext;

        await recorder.start();
        console.log('🎙️ 开始录音...');
        setIsRecording(true);
      } catch (err) {
        console.error('无法获取麦克风权限:', err);
      }
    } else {
      if (!recorderRef.current) return;
      console.log('⏹️ 停止录音...');
      const { blob } = await recorderRef.current.stop();
      setIsRecording(false);
      isLoading = true;

      console.log('🎧 录音完成，得到 wav Blob:', blob);
      // 这里是你要上传的 wav 文件
      const emos = ["neutral", "angry", "happy", "sad"]
      const voice =await api.getVoices(blob);
      const emo = await api.getEmotion(blob);
      console.log(`User voice analysis: Emotion is ${emos[emo.index]}, Predicted probabilities of emotions ${emos} are ${emo.probabilities}, Transcription is "${voice}"`);
      if (voice && voice.trim()) {
        setDilemma(voice);
        
        setTimeout(() => {
          if (voice.trim()) {
            onSubmit(voice);
          }
        }, 100);
      }
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
          <p className="text-sm text-slate-500">{dilemma.length} characters</p>

          <div className="flex items-center space-x-2">
            {/* 语音按钮 */}
            <Button
              type="button"
              variant="outline"
              onClick={handleRecordClick}
              disabled={isLoading}
              className={isRecording ? 'text-red-600 border-red-300' : ''}
            >
              {isRecording ? (
                <>
                  <Square className="w-4 h-4 mr-1" />
                  Stop
                </>
              ) : (
                <>
                  <Mic className="w-4 h-4 mr-1" />
                  Speak
                </>
              )}
            </Button>

            {/* Get Insights 按钮 */}
            <Button
              type="submit"
              disabled={!dilemma.trim() || isLoading}
              className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              {isLoading ? 'Getting Insights...' : 'Get Insights'}
            </Button>
          </div>
        </div>
      </form>
    </Card>
  );
}