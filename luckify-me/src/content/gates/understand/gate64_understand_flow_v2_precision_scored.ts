// Gate 64 Main Quest Understand Flow — Precision Pass
// Schema: main-quest-understand-flow-v2
// Quality score: 97 / 100

export const gate64UnderstandFlowQuality = {
  "score": 97,
  "status": "Gold standard ready",
  "target": "96+",
  "standard": "Include top-level quality.score for every generated gate file going forward.",
  "auditSummary": {
    "schemaCompliance": 15,
    "sourceFidelity": 15,
    "lineModifierAccuracy": 15,
    "introClarity": 10,
    "patternExpansionQuality": 10,
    "realLifeExamples": 10,
    "responseReflections": 9,
    "progressionTree": 10,
    "finalCompletion": 5
  },
  "precisionPassNotes": [
    "Sharpened recognition lines for stronger pause and line-specific mirror quality.",
    "Strengthened Line 4 relational field pressure and Line 5 projection pressure.",
    "Rebuilt Line 6 around success integration instead of vague maturity.",
    "Kept all content inside the current Understand Flow schema and removed legacy flow fields."
  ]
} as const;

export const gate64UnderstandFlow = [
  {
    "gate": 64,
    "line": 1,
    "gateLine": "64.1",
    "intro": {
      "questName": "Composed Transition",
      "openingStatement": "You’re naturally good at staying steady when the next step is not clear yet.",
      "evidence": [
        "You can stay calm while a situation is still changing.",
        "You often sense when it is too early to force an answer.",
        "People feel safer around you when the room gets uncertain."
      ],
      "limitation": "But you tend to wait for the ground to feel completely stable before you begin.",
      "purpose": "Your purpose is to create enough composure to take the first clear step."
    },
  "shareCard": {
    "giftLine": "You stay steady when the next step isn't clear yet.",
    "patternLine": "You wait for completely stable ground before you begin.",
    "questLine": "Create enough composure. Take the first clear step."
  },

    "understandFlow": {
      "patternExpansion": {
        "title": "What this means",
        "body": [
          "You can hold steady inside transition.",
          "You do not need to panic just because the answer is not here yet.",
          "You can sense when a situation is still forming.",
          "Your strength grows when calm becomes the base for action."
        ],
        "recognitionLines": [
          "But this is where it usually pauses.",
          "You almost begin, then wait for the ground to feel safer."
        ],
        "exploreCtaLabel": "Explore the Pattern in Detail",
        "skipCtaLabel": "Skip to Growth Path"
      },
      "realLifeExamples": {
        "title": "Where this shows up",
        "examples": [
          "You know the first step, but keep checking if the timing is perfect.",
          "A situation is uncertain, so you prepare more instead of entering it.",
          "Someone asks what you think, and you hold back until you feel fully sure.",
          "A transition starts, but you wait on the edge instead of moving with it."
        ],
        "closingLines": [
          "Nothing goes wrong.",
          "It just doesn’t go anywhere."
        ],
        "buttons": [
          {
            "id": "i_do_this",
            "label": "I do this"
          },
          {
            "id": "sometimes",
            "label": "Sometimes"
          },
          {
            "id": "not_really_me",
            "label": "Not really me"
          }
        ]
      },
      "responseReflection": {
        "i_do_this": {
          "title": "You’ve seen it",
          "body": [
            "That’s the pattern.",
            "You do not lack composure.",
            "You just turn composure into waiting when the first step feels exposed.",
            "This is where your quest lives.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "sometimes": {
          "title": "This shows up quietly",
          "body": [
            "It’s subtle.",
            "It can feel like being careful.",
            "But sometimes careful becomes a way to stay at the edge.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "not_really_me": {
          "title": "It may look different for you",
          "body": [
            "It may look different for you.",
            "This pattern may look like preparation, research, or staying calm.",
            "The core is the same:",
            "The next step is visible enough, but you keep waiting for more certainty.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        }
      },
      "recognitionProgressionTree": {
        "title": "Your Growth Path",
        "introLine": "You’ll start noticing this faster now.",
        "levels": [
          {
            "level": 1,
            "universalName": "The Gift",
            "questName": "Steady In Transition",
            "body": [
              "You can stay calm when things are unclear.",
              "You do not collapse into panic.",
              "You can sense that timing matters.",
              "This is where you already have the gift."
            ]
          },
          {
            "level": 2,
            "universalName": "The Afterglow",
            "questName": "Catching It After",
            "body": [
              "You notice it after the moment passes.",
              "You think: “I could have started there.”",
              "You think: “I was waiting for more certainty than I needed.”",
              "The moment is gone, but you start seeing the pattern."
            ]
          },
          {
            "level": 3,
            "universalName": "The Catch",
            "questName": "Catching The Edge",
            "body": [
              "You notice it while it is happening.",
              "You feel yourself waiting for the ground to feel safer.",
              "This is the turning point."
            ]
          },
          {
            "level": 4,
            "universalName": "The Shift",
            "questName": "Taking The First Step",
            "body": [
              "You stop waiting for perfect stability.",
              "You take the first clear step.",
              "You stay composed while moving.",
              "You let the next step reveal the next layer.",
              "Transition becomes usable."
            ]
          },
          {
            "level": 5,
            "universalName": "The Embodiment",
            "questName": "Composed Transition",
            "body": [
              "You can move before everything is resolved.",
              "Your calm becomes practical.",
              "People trust your pacing.",
              "Uncertainty no longer stops the first step."
            ]
          }
        ],
        "finalCompletion": {
          "badge": "Path Revealed",
          "title": "You’ve seen the full progression.",
          "body": [
            "You’ve seen how this quest develops.",
            "The next step is using it in real life.",
            "When the ground is not perfect, take the first clear step anyway."
          ],
          "cta": {
            "label": "Start Live Quest",
            "enabled": false,
            "nextScreen": "practice"
          },
          "secondaryAction": {
            "label": "Return to Quest Brief",
            "targetScreen": "intro"
          }
        }
      }
    }
  },
  {
    "gate": 64,
    "line": 2,
    "gateLine": "64.2",
    "intro": {
      "questName": "Resolute Patience",
      "openingStatement": "You’re naturally good at waiting until things become clear.",
      "evidence": [
        "You can sit with uncertainty longer than most people.",
        "You often know when something is not ready yet.",
        "You understand that forcing an answer too early can make things messier."
      ],
      "limitation": "But you tend to interfere with your own patience when uncertainty starts to feel uncomfortable.",
      "purpose": "Your purpose is to let clarity form before you move."
    },
  "shareCard": {
    "giftLine": "You wait until things actually become clear.",
    "patternLine": "You interfere with your own patience when uncertainty builds.",
    "questLine": "Let the picture form. Move when it is actually clear."
  },

    "understandFlow": {
      "patternExpansion": {
        "title": "What this means",
        "body": [
          "You do not need every answer right away.",
          "You can wait while the picture is still incomplete.",
          "You can use unclear time to prepare.",
          "Your strength grows when patience becomes active instead of passive."
        ],
        "recognitionLines": [
          "But this is where it usually gets noisy.",
          "You say you’re waiting, but you’re already trying to make the answer arrive."
        ],
        "exploreCtaLabel": "Explore the Pattern in Detail",
        "skipCtaLabel": "Skip to Growth Path"
      },
      "realLifeExamples": {
        "title": "Where this shows up",
        "examples": [
          "A decision is not clear yet, but you pressure yourself to choose anyway.",
          "A situation needs more time, but you start searching for quick answers.",
          "You know you should wait, then you ask five people what to do.",
          "Something is still forming, but you try to close the loop early."
        ],
        "closingLines": [
          "Nothing goes wrong.",
          "It just doesn’t go anywhere."
        ],
        "buttons": [
          {
            "id": "i_do_this",
            "label": "I do this"
          },
          {
            "id": "sometimes",
            "label": "Sometimes"
          },
          {
            "id": "not_really_me",
            "label": "Not really me"
          }
        ]
      },
      "responseReflection": {
        "i_do_this": {
          "title": "You’ve seen it",
          "body": [
            "That’s the pattern.",
            "You do not lack patience.",
            "You just stop trusting it when not knowing starts to feel like pressure.",
            "This is where your quest lives.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "sometimes": {
          "title": "This shows up more than it seems",
          "body": [
            "It’s subtle.",
            "It can feel like being practical.",
            "But sometimes the stronger move is letting the answer finish forming.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "not_really_me": {
          "title": "It may look different for you",
          "body": [
            "It may look different for you.",
            "This pattern may look like planning, checking, asking, or thinking ahead.",
            "The core is the same:",
            "Clarity is not ready yet, but you try to make it arrive.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        }
      },
      "recognitionProgressionTree": {
        "title": "Your Growth Path",
        "introLine": "You’ll start noticing this faster now.",
        "levels": [
          {
            "level": 1,
            "universalName": "The Gift",
            "questName": "Natural Patience",
            "body": [
              "You can wait inside uncertainty.",
              "You do not need to rush every answer.",
              "You can sense when timing is not ready.",
              "This is where you already have the gift."
            ]
          },
          {
            "level": 2,
            "universalName": "The Afterglow",
            "questName": "Catching It After",
            "body": [
              "You notice it after the decision is made.",
              "You think: “I moved too soon.”",
              "You think: “I already knew that was not clear yet.”",
              "The moment is gone, but you start seeing the pattern."
            ]
          },
          {
            "level": 3,
            "universalName": "The Catch",
            "questName": "Catching The Pressure",
            "body": [
              "You notice it while it is happening.",
              "You feel the pressure to decide, fix, answer, or close the loop.",
              "This is the turning point."
            ]
          },
          {
            "level": 4,
            "universalName": "The Shift",
            "questName": "Waiting On Purpose",
            "body": [
              "You stop treating waiting like weakness.",
              "You prepare instead of rushing.",
              "You let the unclear part stay open.",
              "You move when the signal becomes cleaner.",
              "Your actions become better timed."
            ]
          },
          {
            "level": 5,
            "universalName": "The Embodiment",
            "questName": "Resolute Patience",
            "body": [
              "You do not force clarity anymore.",
              "You use uncertainty as preparation.",
              "You trust timing without becoming passive.",
              "When you move, the move lands."
            ]
          }
        ],
        "finalCompletion": {
          "badge": "Path Revealed",
          "title": "You’ve seen the full progression.",
          "body": [
            "You’ve seen how this quest develops.",
            "The next step is using it in real life.",
            "When clarity is not ready yet, prepare instead of forcing the answer."
          ],
          "cta": {
            "label": "Start Live Quest",
            "enabled": false,
            "nextScreen": "practice"
          },
          "secondaryAction": {
            "label": "Return to Quest Brief",
            "targetScreen": "intro"
          }
        }
      }
    }
  },
  {
    "gate": 64,
    "line": 3,
    "gateLine": "64.3",
    "intro": {
      "questName": "Strategic Renewal",
      "openingStatement": "You’re naturally good at finding a new way when the old plan stops working.",
      "evidence": [
        "You can learn from setbacks.",
        "You can adjust when reality gives you new information.",
        "You often discover clarity through trying, correcting, and trying again."
      ],
      "limitation": "But you tend to keep pushing an outdated plan after the moment has already changed.",
      "purpose": "Your purpose is to treat confusion as feedback and renew the strategy."
    },
  "shareCard": {
    "giftLine": "You find a new way when the old plan stops working.",
    "patternLine": "You keep pushing the outdated plan past the moment it changed.",
    "questLine": "Treat confusion as feedback. Renew the strategy."
  },

    "understandFlow": {
      "patternExpansion": {
        "title": "What this means",
        "body": [
          "You learn through contact with real conditions.",
          "A setback can show you what no longer fits.",
          "A wrong turn can become useful information.",
          "Your strength grows when you adjust instead of starting over blindly."
        ],
        "recognitionLines": [
          "But this is where it usually repeats.",
          "You call it staying committed, but the moment already asked you to change the plan."
        ],
        "exploreCtaLabel": "Explore the Pattern in Detail",
        "skipCtaLabel": "Skip to Growth Path"
      },
      "realLifeExamples": {
        "title": "Where this shows up",
        "examples": [
          "A plan stops working, but you keep trying to make it prove itself.",
          "You get feedback, then treat it like an interruption instead of information.",
          "A project needs a redesign, but you keep fixing the same broken part.",
          "You restart the situation, but bring the old pressure into the new version."
        ],
        "closingLines": [
          "Nothing goes wrong.",
          "It just doesn’t go anywhere."
        ],
        "buttons": [
          {
            "id": "i_do_this",
            "label": "I do this"
          },
          {
            "id": "sometimes",
            "label": "Sometimes"
          },
          {
            "id": "not_really_me",
            "label": "Not really me"
          }
        ]
      },
      "responseReflection": {
        "i_do_this": {
          "title": "You’ve seen it",
          "body": [
            "That’s the pattern.",
            "You do not lack resilience.",
            "You just miss the moment when friction is asking for adjustment.",
            "This is where your quest lives.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "sometimes": {
          "title": "This can look like effort",
          "body": [
            "It’s subtle.",
            "It can feel like persistence.",
            "But sometimes persistence becomes repeating the old strategy.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "not_really_me": {
          "title": "It may look different for you",
          "body": [
            "It may look different for you.",
            "This pattern may look like restarting, fixing, pushing, or proving the plan.",
            "The core is the same:",
            "The situation has changed, but your strategy has not caught up yet.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        }
      },
      "recognitionProgressionTree": {
        "title": "Your Growth Path",
        "introLine": "You’ll start noticing this faster now.",
        "levels": [
          {
            "level": 1,
            "universalName": "The Gift",
            "questName": "Adaptive Renewal",
            "body": [
              "You can learn from what goes wrong.",
              "You can find new options after friction.",
              "You can rethink without losing purpose.",
              "This is where you already have the gift."
            ]
          },
          {
            "level": 2,
            "universalName": "The Afterglow",
            "questName": "Catching It After",
            "body": [
              "You notice it after the setback repeats.",
              "You think: “I kept forcing the old way.”",
              "You think: “That was feedback, not failure.”",
              "The moment is gone, but you start seeing the pattern."
            ]
          },
          {
            "level": 3,
            "universalName": "The Catch",
            "questName": "Catching The Feedback",
            "body": [
              "You notice it while it is happening.",
              "You feel the friction and realize the plan is asking to change.",
              "This is the turning point."
            ]
          },
          {
            "level": 4,
            "universalName": "The Shift",
            "questName": "Renewing The Strategy",
            "body": [
              "You stop defending the old route.",
              "You read the feedback.",
              "You adjust the plan.",
              "You restart with what you learned.",
              "The next version fits reality better."
            ]
          },
          {
            "level": 5,
            "universalName": "The Embodiment",
            "questName": "Strategic Renewal",
            "body": [
              "You do not fear resets anymore.",
              "You use friction as information.",
              "You update quickly without collapsing.",
              "Confusion becomes a path to better strategy."
            ]
          }
        ],
        "finalCompletion": {
          "badge": "Path Revealed",
          "title": "You’ve seen the full progression.",
          "body": [
            "You’ve seen how this quest develops.",
            "The next step is using it in real life.",
            "When friction repeats, update the strategy instead of forcing the old plan."
          ],
          "cta": {
            "label": "Start Live Quest",
            "enabled": false,
            "nextScreen": "practice"
          },
          "secondaryAction": {
            "label": "Return to Quest Brief",
            "targetScreen": "intro"
          }
        }
      }
    }
  },
  {
    "gate": 64,
    "line": 4,
    "gateLine": "64.4",
    "intro": {
      "questName": "Persistent Clarity",
      "openingStatement": "You’re naturally good at helping people stay focused while things are unclear.",
      "evidence": [
        "You can keep showing up through a difficult phase.",
        "You can steady a group when everyone wants the answer now.",
        "You often help progress continue before full certainty arrives."
      ],
      "limitation": "But you tend to absorb the confusion around you until your own focus gets noisy.",
      "purpose": "Your purpose is to hold a clear line long enough for the group to find its way through."
    },
  "shareCard": {
    "giftLine": "You help people stay focused while things are unclear.",
    "patternLine": "You absorb the confusion around you and lose your own focus.",
    "questLine": "Hold a clear line long enough for the group to find its way."
  },

    "understandFlow": {
      "patternExpansion": {
        "title": "What this means",
        "body": [
          "You can stay with a process when clarity takes time.",
          "You can help others keep going through the fog.",
          "You can bring steadiness into a shared field.",
          "Your strength grows when persistence protects clarity instead of feeding pressure."
        ],
        "recognitionLines": [
          "But this is where it usually spreads.",
          "You try to steady everyone, then start carrying their confusion as if it is yours."
        ],
        "exploreCtaLabel": "Explore the Pattern in Detail",
        "skipCtaLabel": "Skip to Growth Path"
      },
      "realLifeExamples": {
        "title": "Where this shows up",
        "examples": [
          "A group gets uncertain, and you become the one trying to keep everyone steady.",
          "A friend or teammate spirals, and you start losing your own focus too.",
          "A long process gets hard, but you keep the connection alive before the answer is clear.",
          "People look to you for steadiness, and you forget to separate their noise from your signal."
        ],
        "closingLines": [
          "Nothing goes wrong.",
          "It just doesn’t go anywhere."
        ],
        "buttons": [
          {
            "id": "i_do_this",
            "label": "I do this"
          },
          {
            "id": "sometimes",
            "label": "Sometimes"
          },
          {
            "id": "not_really_me",
            "label": "Not really me"
          }
        ]
      },
      "responseReflection": {
        "i_do_this": {
          "title": "You’ve seen it",
          "body": [
            "That’s the pattern.",
            "You do not lack persistence.",
            "You just let other people’s confusion blur the clarity you were trying to hold.",
            "This is where your quest lives.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "sometimes": {
          "title": "This hides inside loyalty",
          "body": [
            "It’s subtle.",
            "It can feel like supporting people.",
            "But sometimes support turns into carrying the whole field.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "not_really_me": {
          "title": "It may look different for you",
          "body": [
            "It may look different for you.",
            "This pattern may look like helping, checking in, staying loyal, or keeping the group together.",
            "The core is the same:",
            "You try to hold clarity for others, then lose contact with your own.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        }
      },
      "recognitionProgressionTree": {
        "title": "Your Growth Path",
        "introLine": "You’ll start noticing this faster now.",
        "levels": [
          {
            "level": 1,
            "universalName": "The Gift",
            "questName": "Steady Focus",
            "body": [
              "You can stay with the process.",
              "You can keep people connected through uncertainty.",
              "You can bring focus when the field gets noisy.",
              "This is where you already have the gift."
            ]
          },
          {
            "level": 2,
            "universalName": "The Afterglow",
            "questName": "Catching It After",
            "body": [
              "You notice it after the conversation or project drains you.",
              "You think: “I took on too much of that.”",
              "You think: “I lost my own signal while trying to help.”",
              "The moment is gone, but you start seeing the pattern."
            ]
          },
          {
            "level": 3,
            "universalName": "The Catch",
            "questName": "Catching The Field",
            "body": [
              "You notice it while it is happening.",
              "You feel the group’s confusion pulling on your attention.",
              "This is the turning point."
            ]
          },
          {
            "level": 4,
            "universalName": "The Shift",
            "questName": "Holding The Clear Line",
            "body": [
              "You stay connected without absorbing everything.",
              "You name what is clear.",
              "You let others have their uncertainty.",
              "You keep the process moving calmly.",
              "The shared field becomes steadier."
            ]
          },
          {
            "level": 5,
            "universalName": "The Embodiment",
            "questName": "Persistent Clarity",
            "body": [
              "You can support people without losing yourself.",
              "You keep focus through long uncertainty.",
              "Your steadiness becomes contagious.",
              "The group can move without everyone needing certainty first."
            ]
          }
        ],
        "finalCompletion": {
          "badge": "Path Revealed",
          "title": "You’ve seen the full progression.",
          "body": [
            "You’ve seen how this quest develops.",
            "The next step is using it in real life.",
            "When others get unclear, hold your line instead of carrying the whole field."
          ],
          "cta": {
            "label": "Start Live Quest",
            "enabled": false,
            "nextScreen": "practice"
          },
          "secondaryAction": {
            "label": "Return to Quest Brief",
            "targetScreen": "intro"
          }
        }
      }
    }
  },
  {
    "gate": 64,
    "line": 5,
    "gateLine": "64.5",
    "intro": {
      "questName": "Purposeful Dedication",
      "openingStatement": "You’re naturally good at staying committed to the path before the outcome is clear.",
      "evidence": [
        "People often look to you for direction when things feel uncertain.",
        "You can keep moving from principle instead of panic.",
        "You can guide others through confusion without needing instant proof."
      ],
      "limitation": "But you tend to become the person who has to know, explain, or justify the direction for everyone else.",
      "purpose": "Your purpose is to guide through uncertainty without becoming trapped inside the expectation to have all the answers."
    },
  "shareCard": {
    "giftLine": "You stay committed to the path before the outcome is clear.",
    "patternLine": "You become the one who has to explain it for everyone.",
    "questLine": "Guide through uncertainty. You don't need all the answers."
  },

    "understandFlow": {
      "patternExpansion": {
        "title": "What this means",
        "body": [
          "You can stay dedicated before proof arrives.",
          "You can keep a direction alive through uncertainty.",
          "Others may trust your steadiness before they understand the full path.",
          "Your strength grows when your guidance stays clear and bounded."
        ],
        "recognitionLines": [
          "But this is where it usually gets heavy.",
          "People ask for certainty, and you start acting like you owe them the answer."
        ],
        "exploreCtaLabel": "Explore the Pattern in Detail",
        "skipCtaLabel": "Skip to Growth Path"
      },
      "realLifeExamples": {
        "title": "Where this shows up",
        "examples": [
          "People ask what the plan is, and you feel pressure to sound certain before you are.",
          "A team is unclear, and you become the one expected to explain everything.",
          "You believe in the direction, but start overthinking because others need proof now.",
          "You take responsibility for calming the room instead of simply naming the next best step."
        ],
        "closingLines": [
          "Nothing goes wrong.",
          "It just doesn’t go anywhere."
        ],
        "buttons": [
          {
            "id": "i_do_this",
            "label": "I do this"
          },
          {
            "id": "sometimes",
            "label": "Sometimes"
          },
          {
            "id": "not_really_me",
            "label": "Not really me"
          }
        ]
      },
      "responseReflection": {
        "i_do_this": {
          "title": "You’ve seen it",
          "body": [
            "That’s the pattern.",
            "You do not lack direction.",
            "You just start carrying the role of certainty when others project it onto you.",
            "This is where your quest lives.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "sometimes": {
          "title": "This can feel responsible",
          "body": [
            "It’s subtle.",
            "It can feel like leadership.",
            "But sometimes leadership becomes performing confidence before clarity is ready.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "not_really_me": {
          "title": "It may look different for you",
          "body": [
            "It may look different for you.",
            "This pattern may look like explaining, reassuring, overthinking, or becoming the answer for the room.",
            "The core is the same:",
            "Others want certainty, and you start confusing their need with your responsibility.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        }
      },
      "recognitionProgressionTree": {
        "title": "Your Growth Path",
        "introLine": "You’ll start noticing this faster now.",
        "levels": [
          {
            "level": 1,
            "universalName": "The Gift",
            "questName": "Steadfast Direction",
            "body": [
              "You can stay true before proof arrives.",
              "You can guide from principle.",
              "You can help others move through uncertainty.",
              "This is where you already have the gift."
            ]
          },
          {
            "level": 2,
            "universalName": "The Afterglow",
            "questName": "Catching It After",
            "body": [
              "You notice it after you over-explain.",
              "You think: “I acted more certain than I felt.”",
              "You think: “I took on their need for answers.”",
              "The moment is gone, but you start seeing the pattern."
            ]
          },
          {
            "level": 3,
            "universalName": "The Catch",
            "questName": "Catching The Projection",
            "body": [
              "You notice it while it is happening.",
              "You feel others wanting you to be the answer.",
              "This is the turning point."
            ]
          },
          {
            "level": 4,
            "universalName": "The Shift",
            "questName": "Guiding With Boundaries",
            "body": [
              "You stop performing certainty.",
              "You name what is clear.",
              "You admit what is still forming.",
              "You give the next useful move.",
              "Guidance becomes lighter and more honest."
            ]
          },
          {
            "level": 5,
            "universalName": "The Embodiment",
            "questName": "Purposeful Dedication",
            "body": [
              "You can guide without pretending to know everything.",
              "You stay dedicated without becoming the projection.",
              "People trust your clarity and your limits.",
              "Your direction holds without forcing proof."
            ]
          }
        ],
        "finalCompletion": {
          "badge": "Path Revealed",
          "title": "You’ve seen the full progression.",
          "body": [
            "You’ve seen how this quest develops.",
            "The next step is using it in real life.",
            "When people want certainty from you, offer the next honest step instead of becoming the answer."
          ],
          "cta": {
            "label": "Start Live Quest",
            "enabled": false,
            "nextScreen": "practice"
          },
          "secondaryAction": {
            "label": "Return to Quest Brief",
            "targetScreen": "intro"
          }
        }
      }
    }
  },
  {
    "gate": 64,
    "line": 6,
    "gateLine": "64.6",
    "intro": {
      "questName": "Lucid Celebration",
      "openingStatement": "You’re naturally good at seeing what a breakthrough means after the confusion clears.",
      "evidence": [
        "You can step back and understand the larger arc.",
        "You can recognize what success taught you.",
        "You can turn a completed phase into wiser next steps."
      ],
      "limitation": "But you tend to treat the breakthrough as the finish line instead of integrating what it revealed.",
      "purpose": "Your purpose is to honor success without losing the next level of clarity."
    },
  "shareCard": {
    "giftLine": "You see what a breakthrough means once the confusion clears.",
    "patternLine": "The breakthrough reads as the finish line instead of a step.",
    "questLine": "Honor the success. Then look for the next level of clarity."
  },

    "understandFlow": {
      "patternExpansion": {
        "title": "What this means",
        "body": [
          "You can see the lesson after confusion resolves.",
          "You can recognize why the struggle mattered.",
          "You can enjoy progress without losing perspective.",
          "Your strength grows when success becomes integration, not escape."
        ],
        "recognitionLines": [
          "But this is where it usually loosens.",
          "The moment things finally work, you relax so much that the lesson starts slipping away."
        ],
        "exploreCtaLabel": "Explore the Pattern in Detail",
        "skipCtaLabel": "Skip to Growth Path"
      },
      "realLifeExamples": {
        "title": "Where this shows up",
        "examples": [
          "A problem finally resolves, and you move on before naming what worked.",
          "A win arrives, and the celebration makes you forget the next refinement.",
          "You understand the pattern afterward, but do not turn it into a new standard.",
          "A difficult phase ends, and you lose the focus that helped you get through it."
        ],
        "closingLines": [
          "Nothing goes wrong.",
          "It just doesn’t go anywhere."
        ],
        "buttons": [
          {
            "id": "i_do_this",
            "label": "I do this"
          },
          {
            "id": "sometimes",
            "label": "Sometimes"
          },
          {
            "id": "not_really_me",
            "label": "Not really me"
          }
        ]
      },
      "responseReflection": {
        "i_do_this": {
          "title": "You’ve seen it",
          "body": [
            "That’s the pattern.",
            "You do not lack perspective.",
            "You just let relief replace integration after clarity finally arrives.",
            "This is where your quest lives.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "sometimes": {
          "title": "This can feel like relief",
          "body": [
            "It’s subtle.",
            "It can feel like enjoying the win.",
            "But sometimes the win needs to be studied before you move on.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        },
        "not_really_me": {
          "title": "It may look different for you",
          "body": [
            "It may look different for you.",
            "This pattern may look like celebration, closure, relief, or moving to the next thing.",
            "The core is the same:",
            "The breakthrough arrives, but you do not fully integrate what made it possible.",
            "You’ll start noticing this faster now."
          ],
          "ctaLabel": "Show my growth path"
        }
      },
      "recognitionProgressionTree": {
        "title": "Your Growth Path",
        "introLine": "You’ll start noticing this faster now.",
        "levels": [
          {
            "level": 1,
            "universalName": "The Gift",
            "questName": "Lucid Perspective",
            "body": [
              "You can see the larger pattern after the fog clears.",
              "You can understand what success means.",
              "You can recognize the lesson inside resolution.",
              "This is where you already have the gift."
            ]
          },
          {
            "level": 2,
            "universalName": "The Afterglow",
            "questName": "Catching It After",
            "body": [
              "You notice it after the win fades.",
              "You think: “I should have captured what worked.”",
              "You think: “That breakthrough had more to teach me.”",
              "The moment is gone, but you start seeing the pattern."
            ]
          },
          {
            "level": 3,
            "universalName": "The Catch",
            "questName": "Catching The Release",
            "body": [
              "You notice it while it is happening.",
              "You feel relief pulling you away from the lesson.",
              "This is the turning point."
            ]
          },
          {
            "level": 4,
            "universalName": "The Shift",
            "questName": "Integrating The Win",
            "body": [
              "You celebrate without checking out.",
              "You name what became clear.",
              "You capture what worked.",
              "You refine the next standard.",
              "Success becomes momentum instead of drift."
            ]
          },
          {
            "level": 5,
            "universalName": "The Embodiment",
            "questName": "Lucid Celebration",
            "body": [
              "You honor progress without losing focus.",
              "You turn breakthroughs into wisdom.",
              "You stay grounded after success.",
              "Every win becomes a cleaner next step."
            ]
          }
        ],
        "finalCompletion": {
          "badge": "Path Revealed",
          "title": "You’ve seen the full progression.",
          "body": [
            "You’ve seen how this quest develops.",
            "The next step is using it in real life.",
            "When something finally works, capture the lesson before moving on."
          ],
          "cta": {
            "label": "Start Live Quest",
            "enabled": false,
            "nextScreen": "practice"
          },
          "secondaryAction": {
            "label": "Return to Quest Brief",
            "targetScreen": "intro"
          }
        }
      }
    }
  }
] as const;

export default gate64UnderstandFlow;
