// API Service for connecting to PersonaReflect backend
// Place this file at: src/services/api.ts

import { PersonaResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface DilemmaRequest {
  user_id?: string;
  dilemma: string;
  context?: Record<string, any>;
}

export interface DilemmaResponse {
  id: string;
  timestamp: string;
  dilemma: string;
  responses: PersonaResponse[];
  suggested_actions: string[];
}

export interface ActionPlanRequest {
  entry_id: string;
  responses: PersonaResponse[];
  user_preferences?: Record<string, any>;
}

export interface ActionPlan {
  id: string;
  entry_id: string;
  steps: string[];
  created_at: string;
}

// === Added: Type definitions for calendar scheduling ===
export interface CalendarSlot {
  label: string;     // Human-readable label (e.g. "Morning session")
  start: string;     // Start time in ISO format
  end: string;       // End time in ISO format
  date?: string;     // Optional date string (YYYY-MM-DD)
  time?: string;     // Optional time string (HH:mm)
}

export interface AlexScheduleResponse {
  alex: string;      // Textual reasoning from Alex (Rational Analyst)
  slots: CalendarSlot[];
}

export interface BookEventResponse {
  success: boolean;
  id: string;
  htmlLink: string;  // Link to the created event in Google Calendar
}



class PersonaReflectAPI {
  private baseUrl: string;
  private isBackendAvailable: boolean = false;

  constructor() {
    this.baseUrl = API_BASE_URL;
    this.checkBackendHealth();
  }

  private async checkBackendHealth(): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/`, {
        method: 'GET',
        signal: AbortSignal.timeout(3000), // 3 second timeout
      });
      this.isBackendAvailable = response.ok;
      if (this.isBackendAvailable) {
        console.log('✅ Backend API connected');
      }
    } catch (error) {
      console.log('⚠️ Backend API not available, using mock data');
      this.isBackendAvailable = false;
    }
  }

  async checkHealth(): Promise<boolean> {
    await this.checkBackendHealth();
    return this.isBackendAvailable;
  }

  async getReflections(dilemma: string, userId: string = 'default_user'): Promise<DilemmaResponse> {
    // Check if backend is available
    if (!this.isBackendAvailable) {
      // Fall back to mock data
      return this.getMockReflections(dilemma);
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/reflect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          dilemma,
          context: {},
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get reflections');
      }

      return response.json();
    } catch (error) {
      console.error('API Error:', error);
      // Fall back to mock data
      return this.getMockReflections(dilemma);
    }
  }

  async getVoices(blob: Blob): Promise<string | void> {
    const formData = new FormData();
    formData.append('file', blob, 'record.wav');

    try {
      const res = await fetch('http://127.0.0.1:9000/transcribe', {
        method: 'POST',
        headers: {
          // 不要手动设置 Content-Type, fetch 会自动为 FormData 设置 multipart/form-data 边界
          accept: 'application/json',
        },
        body: formData,
      });

      const data = await res.json();
      console.log('服务器返回:', data);
      console.log(data.text);
      return data.text
    } catch (err) {
      console.error('上传失败:', err);
    }
  }

  async getEmotion(blob: Blob): Promise<any> {
    const formData = new FormData();
    formData.append('file', blob, 'record.wav');

    try {
      const res = await fetch('http://127.0.0.1:9000/emotion', {
        method: 'POST',
        headers: {
          // 不要手动设置 Content-Type, fetch 会自动为 FormData 设置 multipart/form-data 边界
          accept: 'application/json',
        },
        body: formData,
      });

      const data = await res.json();
      console.log('服务器返回:', data);
      return data;
    } catch (err) {
      console.error('上传失败:', err);
    }
  }

  private getMockReflections(dilemma: string): DilemmaResponse {
    // Import the mock generator function
    const { generatePersonaResponses } = require('../lib/mockData');
    const responses = generatePersonaResponses(dilemma);

    return {
      id: `entry-${Date.now()}`,
      timestamp: new Date().toISOString(),
      dilemma,
      responses,
      suggested_actions: [
        'Start with a 5-minute meditation to center yourself',
        'Write down three specific concerns and address them one by one',
        'Schedule dedicated time blocks for focused work',
        'Practice self-compassion and acknowledge your progress',
        'Seek support from a trusted friend or mentor',
      ],
    };
  }

  async createActionPlan(
    entryId: string,
    responses: PersonaResponse[],
    preferences: Record<string, any> = {}
  ): Promise<ActionPlan> {
    if (!this.isBackendAvailable) {
      // Return mock action plan
      return {
        id: `ap-${Date.now()}`,
        entry_id: entryId,
        steps: [
          'Begin with 5-minute daily mindfulness practice',
          'Identify and challenge one negative thought pattern',
          'Create a structured daily schedule with time blocks',
          'Practice one act of self-compassion each day',
          'Track progress in a journal for accountability',
        ],
        created_at: new Date().toISOString(),
      };
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/action-plan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          entry_id: entryId,
          responses,
          user_preferences: preferences,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create action plan');
      }

      return response.json();
    } catch (error) {
      console.error('API Error:', error);
      // Return mock action plan
      return {
        id: `ap-${Date.now()}`,
        entry_id: entryId,
        steps: [
          'Begin with 5-minute daily mindfulness practice',
          'Identify and challenge one negative thought pattern',
          'Create a structured daily schedule with time blocks',
          'Practice one act of self-compassion each day',
          'Track progress in a journal for accountability',
        ],
        created_at: new Date().toISOString(),
      };
    }
  }

  async getPersonas() {
    if (!this.isBackendAvailable) {
      return {
        personas: [
          {
            id: 'cognitive-behavioral',
            name: 'Dr. Chen',
            icon: '🧠',
            title: 'Cognitive-Behavioral Coach',
            description: 'Helps identify thought patterns and develop practical strategies',
          },
          {
            id: 'empathetic-friend',
            name: 'Maya',
            icon: '💙',
            title: 'Empathetic Friend',
            description: 'Provides emotional support and validation',
          },
          {
            id: 'rational-analyst',
            name: 'Alex',
            icon: '📊',
            title: 'Rational Analyst',
            description: 'Offers structured, data-driven approaches',
          },
          {
            id: 'mindfulness-mentor',
            name: 'Sage',
            icon: '🧘',
            title: 'Mindfulness Mentor',
            description: 'Guides toward present-moment awareness',
          },
        ],
      };
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/personas`);

      if (!response.ok) {
        throw new Error('Failed to get personas');
      }

      return response.json();
    } catch (error) {
      // Return default personas
      return {
        personas: [
          {
            id: 'cognitive-behavioral',
            name: 'Dr. Chen',
            icon: '🧠',
            title: 'Cognitive-Behavioral Coach',
            description: 'Helps identify thought patterns and develop practical strategies',
          },
          {
            id: 'empathetic-friend',
            name: 'Maya',
            icon: '💙',
            title: 'Empathetic Friend',
            description: 'Provides emotional support and validation',
          },
          {
            id: 'rational-analyst',
            name: 'Alex',
            icon: '📊',
            title: 'Rational Analyst',
            description: 'Offers structured, data-driven approaches',
          },
          {
            id: 'mindfulness-mentor',
            name: 'Sage',
            icon: '🧘',
            title: 'Mindfulness Mentor',
            description: 'Guides toward present-moment awareness',
          },
        ],
      };
    }
  }

  // === Add these methods inside class PersonaReflectAPI ===
  async alexSchedule(
    dilemma: string,
    opts: { days?: number; duration?: number; startHour?: number; endHour?: number; topk?: number } = {}
  ): Promise<AlexScheduleResponse> {
    const { days = 3, duration = 60, startHour = 9, endHour = 18, topk = 3 } = opts;

    // If backend is unavailable, return mock response
    if (!this.isBackendAvailable) {
      return {
        alex: `Rational analysis (mock):\n- Goal → schedule ${duration}min blocks over ${days} days.`,
        slots: [
          { label: "Morning session", start: new Date().toISOString(), end: new Date(Date.now() + duration * 60000).toISOString() },
        ],
      };
    }

    // Build request URL with query parameters
    const url = new URL(`${this.baseUrl}/api/alex/schedule`);
    url.searchParams.set("dilemma", dilemma);
    url.searchParams.set("days", String(days));
    url.searchParams.set("duration", String(duration));
    url.searchParams.set("start_hour", String(startHour));
    url.searchParams.set("end_hour", String(endHour));
    url.searchParams.set("topk", String(topk));

    const res = await fetch(url.toString(), { method: "POST" });
    if (!res.ok) throw new Error("Failed to fetch Alex schedule");
    return res.json();
  }

  async alexBookEvent(
    title: string,
    startIso: string,
    duration: number,
    description = ""
  ): Promise<BookEventResponse> {
    // If backend is unavailable, return mock success
    if (!this.isBackendAvailable) {
      return {
        success: true,
        id: `evt-${Date.now()}`,
        htmlLink: "https://calendar.google.com/",
      };
    }

    const url = new URL(`${this.baseUrl}/api/alex/book`);
    url.searchParams.set("title", title);
    url.searchParams.set("start_iso", startIso);
    url.searchParams.set("duration", String(duration));
    if (description) url.searchParams.set("description", description);

    const res = await fetch(url.toString(), { method: "POST" });
    if (!res.ok) throw new Error("Failed to create calendar event");
    return res.json();
  }

  // Optional: explicitly trigger Google OAuth authorization flow
  async calendarAuth(): Promise<{ ok: boolean; message?: string }> {
    const res = await fetch(`${this.baseUrl}/api/calendar/auth`);
    if (!res.ok) throw new Error("Calendar authentication failed");
    return res.json();
  }

  // Optional: check whether a valid calendar token already exists
  async calendarStatus(): Promise<{ token_exists: boolean }> {
    const res = await fetch(`${this.baseUrl}/api/calendar/status`);
    if (!res.ok) throw new Error("Failed to get calendar token status");
    return res.json();
  }


}

export const api = new PersonaReflectAPI();
