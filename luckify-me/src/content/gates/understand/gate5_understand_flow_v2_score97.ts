import type { MainQuestUnderstandFlow } from './types';

export const gate5UnderstandFlow = {
  "gate": 5,
  "quality": {
    "score": 97,
    "status": "Gold standard ready",
    "target": "96+",
    "standard": "Include top-level quality.score in every generated gate file and include the score in the filename.",
    "schemaValidation": "PASS",
    "validator": "07_VALIDATOR_APP_ALIGNED_V4.md",
    "notes": "Precision pass complete; current Understand Flow schema only; Start Live Quest remains disabled."
  },
  "entries": [
    {
      "gate": 5,
      "line": 1,
      "gateLine": "5.1",
      "intro": {
        "questName": "Steady Timing",
        "openingStatement": "You’re naturally good at building progress through rhythm.",
        "evidence": [
          "You can stay with something longer than most people.",
          "You notice when a pace is sustainable or not.",
          "Your progress gets stronger when you repeat the right thing at the right time."
        ],
        "limitation": "But you tend to lose your rhythm when outside pressure makes you question your pace.",
        "purpose": "Your purpose is to stay loyal to your timing long enough for steady progress to become real."
      },
  "shareCard": {
    "giftLine": "Progress builds naturally when you keep your rhythm.",
    "patternLine": "Outside pressure pulls you off the pace you know.",
    "questLine": "Stay with your rhythm. Progress is building."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You are here to work with rhythm, consistency, and timing.",
            "You do not need to move because everyone else is moving.",
            "Your strength builds through repeated, well-timed effort.",
            "The base of this quest is learning what pace you can actually sustain."
          ],
          "recognitionLines": [
            "But this is where the pattern usually bends.",
            "You almost stay with your rhythm, then change pace so other people feel better."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You have a good routine, then abandon it because someone else moves faster.",
            "You know your pace works, but you rush because the room feels impatient.",
            "You commit to something steady, then start adjusting it for everyone else.",
            "You lose momentum because you tried to keep up with timing that was never yours."
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
              "You do not lack discipline.",
              "You lose the rhythm when outside pressure starts feeling more real than your own pace.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This can look responsible",
            "body": [
              "It often feels like being flexible or considerate.",
              "But sometimes you are leaving your rhythm too quickly.",
              "The stronger move is staying steady before you adjust.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look like losing rhythm.",
              "It may look like helping, reacting, speeding up, or trying to keep everyone comfortable.",
              "The core is the same:",
              "Your pace was working, but you left it before it had time to build.",
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
              "questName": "Natural Rhythm",
              "body": [
                "You can sense a sustainable pace.",
                "You can stay with a process.",
                "You notice when timing matters.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after your rhythm has already been interrupted.",
                "You think: “I was fine before I sped up.”",
                "You think: “That was not actually my pace.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Pressure",
              "body": [
                "You notice it while it is happening.",
                "You feel the pressure to change pace before your rhythm has proven itself.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Staying With Your Pace",
              "body": [
                "You pause before adjusting.",
                "You check whether the pressure is actually yours.",
                "You keep the rhythm that is already working.",
                "You let consistency build weight.",
                "Progress starts feeling more trustworthy."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Steady Timing",
              "body": [
                "You do not abandon your rhythm to satisfy urgency.",
                "You move with steady commitment.",
                "Your timing becomes dependable.",
                "Progress builds because your pace holds."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When outside pressure gets loud, stay with the rhythm that is already working."
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
      "gate": 5,
      "line": 2,
      "gateLine": "5.2",
      "intro": {
        "questName": "Peaceful Timing",
        "openingStatement": "You’re naturally good at staying calm while timing unfolds.",
        "evidence": [
          "You can wait without immediately treating delay as failure.",
          "Your steadiness can calm the people around you.",
          "You often know that the right moment has not arrived yet."
        ],
        "limitation": "But you tend to disturb your own calm when uncertainty starts to feel unsafe.",
        "purpose": "Your purpose is to let waiting become a source of peace instead of pressure."
      },
  "shareCard": {
    "giftLine": "You hold calm while others rush.",
    "patternLine": "Uncertainty makes you disrupt the calm you built.",
    "questLine": "Let the waiting be steady, not something to fix."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You have a natural ability to stay settled while things unfold.",
            "You can let timing breathe without needing to force the next step.",
            "Your calm is useful because it keeps unnecessary disruption out of the moment.",
            "You do not need to prove progress by moving too soon."
          ],
          "recognitionLines": [
            "But this is where the gift gets interrupted.",
            "You say you trust the timing, then start checking for proof that it is safe to wait."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A decision needs more time, but you keep refreshing for updates.",
            "Someone is not ready to answer, and you start reading silence as a problem.",
            "A plan is moving slowly, and you begin looking for something to fix.",
            "You know waiting is correct, but your body starts acting like something is wrong."
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
              "You just stop trusting it when uncertainty starts feeling unsafe.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel like being alert or prepared.",
              "But sometimes you are disturbing the very calm that would help the moment.",
              "The stronger move is letting peace stay in the room.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look like anxiety.",
              "It may look like checking, planning, asking, or needing reassurance.",
              "The core is the same:",
              "Timing is unfolding, but you start treating the wait like a threat.",
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
              "questName": "Natural Calm",
              "body": [
                "You can wait without forcing the moment.",
                "You can stay settled while things unfold.",
                "You can bring peace to uncertain timing.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after you have already disturbed the calm.",
                "You think: “I did not need to push there.”",
                "You think: “The timing was still fine.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Restlessness",
              "body": [
                "You notice it while it is happening.",
                "You feel the urge to check, force, or get reassurance before the moment is ready.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Letting Peace Hold",
              "body": [
                "You stop reacting to the delay.",
                "You let the silence stay quiet.",
                "You let the process keep moving at its pace.",
                "You stay calm without becoming passive.",
                "The environment starts to settle with you."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Peaceful Timing",
              "body": [
                "You do not break your calm to prove progress.",
                "You trust the right moment without chasing it.",
                "Your presence makes waiting feel safer.",
                "Timing becomes something you can live inside."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When waiting starts to feel unsafe, let your calm be the proof that timing is still working."
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
      "gate": 5,
      "line": 3,
      "gateLine": "5.3",
      "intro": {
        "questName": "Steady Nerves",
        "openingStatement": "You’re naturally good at turning pressure into readiness.",
        "evidence": [
          "You can feel tension before something happens.",
          "You often become more alert when timing is uncertain.",
          "Your nervous energy can become focus when you know where to put it."
        ],
        "limitation": "But you tend to create movement just to escape the discomfort of waiting.",
        "purpose": "Your purpose is to turn restlessness into prepared patience."
      },
  "shareCard": {
    "giftLine": "Pressure makes you more ready, not less.",
    "patternLine": "You create movement to escape the waiting.",
    "questLine": "Stay with the discomfort. It's building something."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You are here to learn timing through pressure, not away from it.",
            "Stillness can feel intense because your body wants something to do.",
            "The gift is not removing the tension.",
            "The gift is using it without letting it take over."
          ],
          "recognitionLines": [
            "But this is where the pattern usually sparks.",
            "You call it getting ready, but part of you is just trying not to feel the wait."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You send the extra message because waiting for the reply feels too uncomfortable.",
            "You change the plan before you know whether the first plan is working.",
            "You start cleaning, checking, fixing, or scrolling because stillness feels too loud.",
            "You make a move just so the tension has somewhere to go."
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
              "You do not lack energy.",
              "You just let the discomfort of waiting turn into unnecessary motion.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This can look productive",
            "body": [
              "It often feels like doing something useful.",
              "But sometimes the activity is only there to escape the tension.",
              "The stronger move is turning that energy into readiness.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look chaotic.",
              "It may look like preparation, checking, adjusting, or staying busy.",
              "The core is the same:",
              "The wait feels uncomfortable, so you create movement before timing asks for it.",
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
              "questName": "Alert Timing",
              "body": [
                "You can feel pressure building.",
                "You can sense when something is about to move.",
                "You have energy that can become readiness.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after you have already reacted.",
                "You think: “I moved because I was tense.”",
                "You think: “That action did not actually help.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Impulse",
              "body": [
                "You notice it while it is happening.",
                "You feel the urge to act just to release pressure.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Using The Tension",
              "body": [
                "You stop before reacting.",
                "You give the energy a useful place to go.",
                "You prepare instead of interfering.",
                "You let the timing stay intact.",
                "Your pressure becomes focus."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Steady Nerves",
              "body": [
                "You can wait without scattering yourself.",
                "You can feel tension without obeying it.",
                "You turn restlessness into readiness.",
                "Your timing becomes stronger under pressure."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When waiting feels too loud, prepare instead of creating unnecessary movement."
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
      "gate": 5,
      "line": 4,
      "gateLine": "5.4",
      "intro": {
        "questName": "Adaptive Timing",
        "openingStatement": "You’re naturally good at using timing strategically.",
        "evidence": [
          "You can tell when to hold, pivot, or move.",
          "You notice changes in the environment before others do.",
          "You can turn a waiting period into preparation."
        ],
        "limitation": "But you tend to stay loyal to a plan after the timing has already changed.",
        "purpose": "Your purpose is to keep your rhythm rooted while letting your strategy adapt."
      },
  "shareCard": {
    "giftLine": "You use timing as a tool, not a constraint.",
    "patternLine": "You hold the old plan past the moment it fits.",
    "questLine": "Stay rooted. Let the strategy shift when needed."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "Your timing is not meant to be rigid.",
            "You can stay consistent without becoming predictable.",
            "You can use waiting as preparation, not just delay.",
            "Your strength grows when your rhythm stays steady and your strategy stays flexible."
          ],
          "recognitionLines": [
            "But this is where the pattern gets stuck.",
            "You know the situation changed, but you keep following the old timing because it feels safer."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A plan stops working, but you keep defending it because you already committed.",
            "A project needs a different pace, but you keep using the original schedule.",
            "People around you are ready to move, but you are still waiting for the old signal.",
            "You miss the opening because you were holding the rhythm too tightly."
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
              "You do not lack timing.",
              "You just sometimes protect the old rhythm after the moment has changed.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This can look consistent",
            "body": [
              "It often feels like staying committed.",
              "But sometimes commitment turns into rigidity.",
              "The stronger move is adapting without losing your center.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look rigid at first.",
              "It may look like loyalty, patience, planning, or staying on track.",
              "The core is the same:",
              "The timing changed, but your strategy did not change with it.",
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
              "questName": "Strategic Timing",
              "body": [
                "You can read timing in the environment.",
                "You can sense when preparation matters.",
                "You can turn waiting into advantage.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the opening has passed.",
                "You think: “I should have adjusted there.”",
                "You think: “I stayed with the old plan too long.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Stuck Point",
              "body": [
                "You notice it while it is happening.",
                "You feel the moment change, but part of you wants to keep the original timing.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Adapting Without Losing Rhythm",
              "body": [
                "You keep the deeper rhythm intact.",
                "You change the strategy when conditions change.",
                "You use the wait to prepare better.",
                "You move when the opening becomes real.",
                "Timing becomes practical instead of fixed."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Adaptive Timing",
              "body": [
                "You do not confuse consistency with rigidity.",
                "You can hold, pivot, or act cleanly.",
                "You let timing guide strategy.",
                "Waiting becomes a source of opportunity."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When the timing changes, adjust the strategy without abandoning your center."
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
      "gate": 5,
      "line": 5,
      "gateLine": "5.5",
      "intro": {
        "questName": "Serene Presence",
        "openingStatement": "You’re naturally good at making patience feel steady for others.",
        "evidence": [
          "Your calm can change the tone of a pressured moment.",
          "People may look to you when waiting feels uncomfortable.",
          "You can show that delay does not have to mean failure."
        ],
        "limitation": "But you tend to take on the pressure to prove that waiting is useful.",
        "purpose": "Your purpose is to model calm timing without becoming responsible for everyone else’s impatience."
      },
  "shareCard": {
    "giftLine": "Your patience steadies the people around you.",
    "patternLine": "You feel pressure to prove that waiting is worthwhile.",
    "questLine": "Model the calm. Their impatience isn't yours to fix."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "Your presence can make patience feel stronger.",
            "You can help others stay settled when timing is not immediate.",
            "The gift is not just waiting.",
            "The gift is showing that calm can still carry power."
          ],
          "recognitionLines": [
            "But this is where projection enters.",
            "People get impatient, and you start feeling responsible for making the wait mean something."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A group gets restless, and you feel pressure to reassure everyone.",
            "Someone doubts the process, and you try to prove the timing is still worth trusting.",
            "A delay happens, and you feel like you have to make everyone calm.",
            "You become the steady one before checking whether that role is actually yours."
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
              "You do not lack calm.",
              "You just start carrying other people’s discomfort with waiting.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This can look helpful",
            "body": [
              "It often feels like being the grounded person in the room.",
              "But sometimes you are absorbing pressure that does not belong to you.",
              "The stronger move is modeling calm without performing it.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look like pressure.",
              "It may look like reassuring, explaining, holding the room, or staying composed for others.",
              "The core is the same:",
              "Waiting becomes visible, and you feel expected to make everyone okay with it.",
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
              "questName": "Calm Presence",
              "body": [
                "You can stay steady under delay.",
                "You can make patience feel less threatening.",
                "You can bring ease to pressured timing.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after you have already carried the room.",
                "You think: “I made their impatience my job.”",
                "You think: “I did not need to prove the timing.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Projection",
              "body": [
                "You notice it while it is happening.",
                "You feel others expecting you to make waiting feel safe or meaningful.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Modeling Without Carrying",
              "body": [
                "You stay calm without taking over.",
                "You let others have their impatience.",
                "You do not perform reassurance.",
                "You keep your presence clean.",
                "The room can settle without becoming your responsibility."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Serene Presence",
              "body": [
                "You do not become the role others project onto you.",
                "You let patience have dignity.",
                "You model calm timing without carrying the field.",
                "Your presence stays peaceful and bounded."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When others get impatient, model calm without making their discomfort your job."
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
      "gate": 5,
      "line": 6,
      "gateLine": "5.6",
      "intro": {
        "questName": "Yielding Wisdom",
        "openingStatement": "You’re naturally good at learning timing through pressure.",
        "evidence": [
          "You can see how stress reveals what is sustainable.",
          "You understand that not every delay is a block.",
          "You can bend with pressure without losing your deeper direction."
        ],
        "limitation": "But you tend to resist the pressure until it becomes heavier than it needed to be.",
        "purpose": "Your purpose is to let pressure refine your timing without breaking your center."
      },
  "shareCard": {
    "giftLine": "Pressure teaches you when to yield and when to hold.",
    "patternLine": "You resist past the point where yielding would have helped.",
    "questLine": "Let it teach you when to move."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "This quest matures through pressure, patience, and perspective.",
            "You can see when life is asking you to bend instead of force.",
            "You can stay aligned without pretending the pressure is easy.",
            "Your wisdom grows when you respond to strain instead of fighting reality."
          ],
          "recognitionLines": [
            "But this is where maturity gets tested.",
            "You call it staying strong, but your body already knows you are bracing."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A long delay wears you down, but you keep acting like nothing is affecting you.",
            "A situation needs flexibility, but you hold your stance until you feel exhausted.",
            "You know the pressure is teaching you something, but you resist the lesson first.",
            "You stay in control so long that adapting starts to feel like losing."
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
              "You do not lack strength.",
              "You just sometimes mistake resistance for resilience.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This can look mature",
            "body": [
              "It often feels like holding yourself together.",
              "But sometimes real maturity is bending before you burn out.",
              "The stronger move is yielding without surrendering your center.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look like resistance.",
              "It may look like endurance, control, discipline, or staying above the stress.",
              "The core is the same:",
              "Pressure is asking for flexibility, but you keep bracing.",
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
              "questName": "Pressure Wisdom",
              "body": [
                "You can learn from difficult timing.",
                "You can see how pressure shapes maturity.",
                "You can stay aware when strain builds.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after you have already pushed too hard.",
                "You think: “I was bracing the whole time.”",
                "You think: “I could have adjusted sooner.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Brace",
              "body": [
                "You notice it while it is happening.",
                "You feel the pressure building, and you can tell whether you are bending or resisting.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Yielding Without Collapsing",
              "body": [
                "You stop fighting the reality of the moment.",
                "You soften the rigid part of the plan.",
                "You keep your deeper center intact.",
                "You let pressure teach the next adjustment.",
                "Strength becomes more flexible."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Yielding Wisdom",
              "body": [
                "You do not break under timing pressure.",
                "You can bend without giving yourself away.",
                "You let adversity refine your rhythm.",
                "Your timing becomes mature, resilient, and alive."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When pressure builds, bend before resistance turns into burnout."
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
  ]
} as const;

export const gate5UnderstandFlowEntries = gate5UnderstandFlow.entries satisfies readonly MainQuestUnderstandFlow[];

export default gate5UnderstandFlow;
