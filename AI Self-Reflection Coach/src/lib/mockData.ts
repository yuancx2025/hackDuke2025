import { JournalEntry } from '../types';

export const mockJournalEntries: JournalEntry[] = [
  {
    id: '1',
    date: '2025-11-07T14:30:00',
    dilemma: 'I keep procrastinating on my presentation for next week. Every time I sit down to work on it, I find myself scrolling through social media or doing other less important tasks. I feel anxious about it but can\'t seem to start.',
    responses: [
      {
        persona: 'cognitive-behavioral',
        name: 'Dr. Chen',
        icon: '🧠',
        response: 'Your procrastination pattern suggests you might be experiencing performance anxiety. Let\'s break this down: What specific thoughts come up when you think about starting the presentation? Often, we procrastinate when we set unrealistic standards for ourselves. Try the "5-minute rule" - commit to working on just one slide for 5 minutes. Usually, starting is the hardest part, and you\'ll find momentum once you begin.'
      },
      {
        persona: 'empathetic-friend',
        name: 'Maya',
        icon: '💙',
        response: 'I hear you, and I want you to know that what you\'re feeling is completely valid. Procrastination often comes from a place of fear or overwhelm, not laziness. It\'s okay to feel anxious about important tasks. Remember that you\'ve successfully completed presentations before, and you have the skills to do this. Be gentle with yourself - you\'re doing your best, and that\'s enough.'
      },
      {
        persona: 'rational-analyst',
        name: 'Alex',
        icon: '📊',
        response: 'Let\'s approach this systematically. You have approximately 7 days until your presentation. Break it into manageable chunks: Day 1-2 for research and outlining, Day 3-4 for creating slides, Day 5 for rehearsal, Days 6-7 as buffer time. Schedule these blocks in your calendar right now. Eliminate distractions by using website blockers during work sessions. What\'s the first concrete step you can take today?'
      },
      {
        persona: 'mindfulness-mentor',
        name: 'Sage',
        icon: '🧘',
        response: 'Notice how you\'re experiencing anxiety about the presentation, but instead of moving through it, you\'re avoiding it with distractions. This creates more anxiety. Try this: Take three deep breaths. Acknowledge the discomfort without judgment. When you sit down to work, observe the urge to check social media without acting on it. Return your attention gently to the present task. The work will feel less overwhelming when you\'re fully present with it.'
      }
    ],
    actionPlan: {
      id: 'ap1',
      entryId: '1',
      steps: [
        'Use the 5-minute rule to start working on one slide today',
        'Block out specific times in calendar for presentation work (2 hours each for next 3 days)',
        'Install website blocker during work sessions',
        'Practice mindful breathing when feeling the urge to procrastinate',
        'Be compassionate with myself throughout the process'
      ],
      createdAt: '2025-11-07T15:00:00'
    }
  },
  {
    id: '2',
    date: '2025-11-05T09:15:00',
    dilemma: 'I\'m struggling to set boundaries with my manager who keeps assigning me work after hours. I want to maintain a good relationship but I\'m burning out.',
    responses: [
      {
        persona: 'cognitive-behavioral',
        name: 'Dr. Chen',
        icon: '🧠',
        response: 'Setting boundaries doesn\'t mean you\'re being difficult - it means you\'re being sustainable. Reframe your thinking: saying no to after-hours work isn\'t saying no to your manager, it\'s saying yes to your wellbeing and long-term productivity. Practice assertive communication: "I\'m committed to delivering quality work during business hours. For urgent matters, let\'s discuss prioritization so I can manage my workload effectively."'
      },
      {
        persona: 'empathetic-friend',
        name: 'Maya',
        icon: '💙',
        response: 'It takes courage to recognize you need boundaries, and I\'m proud of you for acknowledging this. Burnout is real, and your feelings are important. You deserve to have personal time to recharge. Remember, you can be a dedicated professional AND protect your wellbeing - these aren\'t mutually exclusive. Your manager will respect you more when you respect yourself.'
      },
      {
        persona: 'rational-analyst',
        name: 'Alex',
        icon: '📊',
        response: 'Document the pattern: track how many after-hours requests you receive weekly and their actual urgency level. Prepare specific data for your conversation. Schedule a formal meeting to discuss workload and boundaries. Propose concrete solutions: setting core collaboration hours, using urgent vs. non-urgent tags, or having a rotating on-call schedule if truly needed. Come with solutions, not just problems.'
      },
      {
        persona: 'mindfulness-mentor',
        name: 'Sage',
        icon: '🧘',
        response: 'Notice the tension between your need for approval and your need for rest. Both are valid, but one is being honored at the expense of the other. Practice being present with the discomfort of potentially disappointing others. Your worth is not determined by your availability. Create a ritual to transition from work to personal time - perhaps a short meditation or a walk - to honor this boundary internally first.'
      }
    ]
  }
];

export function generatePersonaResponses(dilemma: string): PersonaResponse[] {
  // In a real app, this would call an AI API
  // For now, return contextual mock responses
  return [
    {
      persona: 'cognitive-behavioral',
      name: 'Dr. Chen',
      icon: '🧠',
      response: `Looking at your situation through a cognitive-behavioral lens, I notice patterns in your thinking that might be contributing to this challenge. Let's identify the specific thoughts and beliefs that arise when you face this dilemma. Often, our automatic thoughts can create barriers. What would happen if you challenged these thoughts? What evidence do you have for and against them? I'd suggest starting with small, concrete actions that can help you build momentum and prove to yourself that change is possible.`
    },
    {
      persona: 'empathetic-friend',
      name: 'Maya',
      icon: '💙',
      response: `Thank you for sharing this with me. I can sense how much this is weighing on you, and I want you to know that your feelings are completely valid. It's not easy to face challenges like this, and the fact that you're reflecting on it shows real strength and self-awareness. Remember that you don't have to have everything figured out right now. Be patient and kind with yourself as you work through this. You're not alone, and it's okay to take things one step at a time.`
    },
    {
      persona: 'rational-analyst',
      name: 'Alex',
      icon: '📊',
      response: `Let's break this down into manageable components. What are the key factors contributing to this situation? What resources and constraints are we working with? I'd suggest creating a structured approach: First, clearly define your desired outcome. Second, identify 2-3 specific actions you can take this week. Third, set measurable milestones so you can track progress. What metrics would indicate you're moving in the right direction? Time-box your efforts and reassess weekly to ensure you're staying on track.`
    },
    {
      persona: 'mindfulness-mentor',
      name: 'Sage',
      icon: '🧘',
      response: `Take a moment to simply notice what arises as you sit with this dilemma. What sensations do you feel in your body? What emotions are present? There's wisdom in not rushing to solve or fix, but rather in being fully present with what is. Your dilemma is pointing you toward something important - perhaps a value that's being compromised, or a need that's asking to be met. When you move from a place of presence rather than reactivity, the path forward often becomes clearer. What would it be like to approach this situation with curiosity rather than judgment?`
    }
  ];
}
