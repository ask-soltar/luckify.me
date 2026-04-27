export type MainQuestUnderstandFlow = {
  gate: number;
  line: number;
  gateLine: string;

  intro: {
    questName: string;
    openingStatement: string;
    evidence: string[];
    limitation: string;
    purpose: string;
  };

  understandFlow: {
    patternExpansion: {
      title: string;
      body: string[];
      recognitionLines: string[];
      exploreCtaLabel: string;
      skipCtaLabel: string;
    };

    realLifeExamples: {
      title: string;
      examples: string[];
      closingLines: string[];
      buttons: {
        id: 'i_do_this' | 'sometimes' | 'not_really_me';
        label: string;
      }[];
    };

    responseReflection: {
      i_do_this: {
        title: string;
        body: string[];
        ctaLabel: string;
      };
      sometimes: {
        title: string;
        body: string[];
        ctaLabel: string;
      };
      not_really_me: {
        title: string;
        body: string[];
        ctaLabel: string;
      };
    };

    recognitionProgressionTree: {
      title: string;
      introLine: string;
      levels: {
        level: number;
        universalName:
          | 'The Gift'
          | 'The Afterglow'
          | 'The Catch'
          | 'The Shift'
          | 'The Embodiment';
        questName: string;
        body: string[];
      }[];
      finalCompletion: {
        badge: string;
        title: string;
        body: string[];
        cta: {
          label: string;
          enabled: boolean;
          nextScreen: 'practice';
        };
        secondaryAction: {
          label: string;
          targetScreen: 'intro';
        };
      };
    };
  };
};

export const mainQuestUnderstandSeed = {
  gate: 59,
  line: 2,
  gateLine: '59.2',

  intro: {
    questName: 'Transformative Connection',
    openingStatement: "You're naturally good at creating connection.",
    evidence: [
      'Things open quickly around you.',
      'People respond to you.',
      'Opportunities show up.',
    ],
    limitation: 'But you tend to keep things comfortable instead of letting them become real.',
    purpose: 'Your purpose is to let those moments actually go somewhere.',
  },

  understandFlow: {
    patternExpansion: {
      title: 'What this means',
      body: [
        'You create connection easily.',
        'People open up.',
        'Conversations warm up.',
        'Opportunities start naturally.',
      ],
      recognitionLines: [
        'But this is where it usually stops.',
        'You keep things comfortable instead of letting them become real.',
      ],
      exploreCtaLabel: 'Explore the Pattern in Detail',
      skipCtaLabel: 'Skip to Growth Path',
    },

    realLifeExamples: {
      title: 'Where this shows up',
      examples: [
        'A conversation gets personal, then you change the tone.',
        'Someone opens up, but you don\u2019t respond honestly.',
        'An opportunity appears, but you don\u2019t take the next step.',
        'Something meaningful starts, but you leave it there.',
      ],
      closingLines: ['Nothing goes wrong.', 'It just doesn\u2019t go anywhere.'],
      buttons: [
        { id: 'i_do_this', label: 'I do this' },
        { id: 'sometimes', label: 'Sometimes' },
        { id: 'not_really_me', label: 'Not really me' },
      ],
    },

    responseReflection: {
      i_do_this: {
        title: "You've seen it",
        body: [
          "That's the pattern.",
          "You don't struggle to create connection.",
          'You just stop it before it becomes real.',
          'This is where your quest lives.',
          "You'll start noticing this faster now.",
        ],
        ctaLabel: 'Show my growth path',
      },
      sometimes: {
        title: 'This shows up more than you think',
        body: [
          "It's subtle.",
          'It often feels like keeping things smooth or keeping things easy.',
          'But those are the moments that could have gone further.',
          "You'll start noticing this faster now.",
        ],
        ctaLabel: 'Show my growth path',
      },
      not_really_me: {
        title: 'It may look different for you',
        body: [
          "This pattern isn't always obvious.",
          'But the core is the same:',
          'Something opens, and it doesn\u2019t get taken further.',
          'Watch for that.',
          "You'll start noticing this faster now.",
        ],
        ctaLabel: 'Show my growth path',
      },
    },

    recognitionProgressionTree: {
      title: 'Your Growth Path',
      introLine: "You'll start noticing this faster now.",
      levels: [
        {
          level: 1,
          universalName: 'The Gift',
          questName: 'Natural Connection',
          body: [
            'Connection happens easily.',
            'People open up.',
            'Things begin without effort.',
            'This is where you already have the gift.',
          ],
        },
        {
          level: 2,
          universalName: 'The Afterglow',
          questName: 'Catching It After',
          body: [
            "You notice it after it's over.",
            'You think: \u201cI could have said something there.\u201d',
            'You think: \u201cThat could have gone somewhere.\u201d',
            'The moment is gone, but you start seeing the pattern.',
          ],
        },
        {
          level: 3,
          universalName: 'The Catch',
          questName: 'Catching It In The Moment',
          body: [
            "You notice it while it's happening.",
            'You feel the moment opening, and you hesitate.',
            'This is the turning point.',
          ],
        },
        {
          level: 4,
          universalName: 'The Shift',
          questName: 'Taking The Step',
          body: [
            'You start acting in the moment.',
            'You say it.',
            'You follow up.',
            'You stay instead of leaving.',
            'Things begin to move.',
          ],
        },
        {
          level: 5,
          universalName: 'The Embodiment',
          questName: 'Transformative Presence',
          body: [
            "You don't stop it anymore.",
            'Connection becomes real.',
            'Things move forward.',
            'Moments change outcomes.',
          ],
        },
      ],
      finalCompletion: {
        badge: 'Path Revealed',
        title: "You've seen the full progression.",
        body: [
          "You've seen how this quest develops.",
          'The next step is using it in real life.',
          "When something opens, don't stop it early.",
        ],
        cta: {
          label: 'Start Live Quest',
          enabled: false,
          nextScreen: 'practice',
        },
        secondaryAction: {
          label: 'Return to Quest Brief',
          targetScreen: 'intro',
        },
      },
    },
  },
} satisfies MainQuestUnderstandFlow;
