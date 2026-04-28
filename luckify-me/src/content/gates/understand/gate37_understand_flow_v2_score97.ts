import type { MainQuestUnderstandFlow } from './types';

export const gate37UnderstandFlow: { gate: number; quality: { score: number; schemaValidation: string; status: string; target: string; standard: string }; entries: MainQuestUnderstandFlow[] } = {
  "gate": 37,
  "quality": {
    "score": 97,
    "schemaValidation": "PASS",
    "status": "Gold standard ready",
    "target": "96+",
    "standard": "Include top-level quality.score and quality.schemaValidation in every generated gate file and include the score in the filename."
  },
  "entries": [
    {
      "gate": 37,
      "line": 1,
      "gateLine": "37.1",
      "intro": {
        "questName": "Foundation of Trust",
        "openingStatement": "You’re naturally good at sensing what a relationship needs to feel safe.",
        "evidence": [
          "You notice when people need consistency before they open.",
          "You understand that trust grows through small actions.",
          "You can feel when a promise needs a stronger base."
        ],
        "limitation": "But you tend to hold back until the relationship feels completely secure.",
        "purpose": "Your purpose is to build enough trust to make the next honest move."
      },
  "shareCard": {
    "giftLine": "You sense what a relationship needs to feel safe.",
    "patternLine": "You hold back until the relationship feels completely secure.",
    "questLine": "Build enough trust to make the next honest move."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You can sense what makes people feel safe.",
            "You know that trust is built through repeated actions.",
            "You notice when the foundation is not strong enough yet.",
            "Your strength grows when you stabilize the bond before asking for more."
          ],
          "recognitionLines": [
            "But this is where it usually stops.",
            "You almost make the relationship real, then wait for more proof that it is safe."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You want to say what you need, but you wait for the perfect moment.",
            "Someone offers support, but you test whether they really mean it.",
            "A friendship could deepen, but you stay at the polite level.",
            "You notice a shaky agreement, then avoid naming what needs to be clearer."
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
              "You do not lack care or loyalty.",
              "You just wait for the bond to feel safer before you fully enter it.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel like being careful.",
              "It can look like giving the relationship more time.",
              "But sometimes the next step is what builds the trust you are waiting for.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look like hesitation.",
              "It may look like testing, watching, or keeping things casual.",
              "The core is the same:",
              "Trust is forming, but you delay the honest next step.",
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
              "questName": "Trust Sensitivity",
              "body": [
                "You can feel what makes a bond safe.",
                "You notice what people need from each other.",
                "You understand the value of consistency.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the moment passes.",
                "You think: “I could have been more honest there.”",
                "You think: “That needed a clearer agreement.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Threshold",
              "body": [
                "You notice it while it is happening.",
                "You feel the relationship asking for more honesty, and you pause.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Making The Bond Clear",
              "body": [
                "You name the need.",
                "You clarify the agreement.",
                "You take the next honest step.",
                "You let trust become action.",
                "The relationship has something real to stand on."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Grounded Trust",
              "body": [
                "You do not wait for perfect safety anymore.",
                "You build trust through clean action.",
                "Your care becomes steady and clear.",
                "The bond knows where it stands."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When trust is forming, take the next honest step instead of waiting for perfect safety."
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
      "gate": 37,
      "line": 2,
      "gateLine": "37.2",
      "intro": {
        "questName": "Natural Belonging",
        "openingStatement": "You’re naturally good at making people feel included without forcing it.",
        "evidence": [
          "People often relax around you.",
          "You can create warmth without making a big performance out of it.",
          "You sense who needs reassurance before they ask."
        ],
        "limitation": "But you tend to downplay the warmth you bring or wait for others to name it first.",
        "purpose": "Your purpose is to own your ability to create belonging consciously."
      },
  "shareCard": {
    "giftLine": "You make people feel included without forcing it.",
    "patternLine": "You downplay the warmth you bring or wait for it to be named.",
    "questLine": "Own your ability to create belonging. It's real."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You create warmth naturally.",
            "People feel more included around you.",
            "You can make a space feel safer without overthinking it.",
            "Your strength grows when you stop treating that as accidental."
          ],
          "recognitionLines": [
            "But this is where it usually gets hidden.",
            "It feels natural, so you act like the warmth you bring does not matter."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A group relaxes after you arrive, but you pretend you did nothing.",
            "Someone feels left out, and you quietly make space for them.",
            "A tense conversation softens because of your tone, but you brush it off.",
            "People return to you for comfort, but you do not fully claim why."
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
              "You do not lack the gift of belonging.",
              "You just treat it like it is too natural to count.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel ordinary to you.",
              "It can look like just being kind, warm, or easy to be around.",
              "But those moments are often the place where people feel safe enough to belong.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not feel obvious.",
              "It may show up in small moments where people settle around you.",
              "The core is the same:",
              "You create belonging, then act like it was nothing.",
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
              "questName": "Natural Warmth",
              "body": [
                "Belonging happens easily around you.",
                "People feel included.",
                "The room softens without effort.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the moment is over.",
                "You think: “They opened up there.”",
                "You think: “The room changed after that.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Warmth",
              "body": [
                "You notice it while it is happening.",
                "You feel people relaxing around you, and you realize your presence is part of it.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Owning The Welcome",
              "body": [
                "You stop brushing it off.",
                "You include people on purpose.",
                "You make the agreement clearer.",
                "You let your warmth have direction.",
                "People know they are actually welcome."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Conscious Belonging",
              "body": [
                "You create belonging without hiding it.",
                "Your warmth becomes steady.",
                "People know where they stand with you.",
                "Connection becomes easier to trust."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When your warmth changes the room, do not act like it was nothing."
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
      "gate": 37,
      "line": 3,
      "gateLine": "37.3",
      "intro": {
        "questName": "Tested Agreement",
        "openingStatement": "You’re naturally good at learning what a relationship needs through real contact.",
        "evidence": [
          "You notice what holds after pressure.",
          "You learn quickly when an agreement is unclear.",
          "You can adjust after friction instead of pretending nothing happened."
        ],
        "limitation": "But you tend to treat relational friction like the bond is failing instead of showing you what needs to change.",
        "purpose": "Your purpose is to use friction to make trust cleaner."
      },
  "shareCard": {
    "giftLine": "You learn what a relationship needs through real contact.",
    "patternLine": "Friction makes you think the bond is struggling.",
    "questLine": "Use friction to make trust cleaner."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You learn through real contact.",
            "You notice where agreements break down.",
            "You can see what needs repair after friction happens.",
            "Your strength grows when you adjust instead of abandoning the bond too early."
          ],
          "recognitionLines": [
            "But this is where it usually gets messy.",
            "The agreement gets tested, and you start acting like the whole bond is the problem."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A small misunderstanding happens, and you pull back more than you meant to.",
            "Someone disappoints you, and you quietly rewrite the whole relationship.",
            "A promise gets missed, and you stop trusting the person completely.",
            "A conflict shows what needs repair, but you treat it like proof to leave."
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
              "You do not lack loyalty or care.",
              "You just sometimes read friction as failure before it has taught you anything.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up in small ruptures",
            "body": [
              "It can feel like protecting yourself.",
              "It can look like being realistic about people.",
              "But sometimes the friction is showing the exact agreement that needs to be rebuilt.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look dramatic.",
              "It may look like quiet distance after something feels off.",
              "The core is the same:",
              "A bond gets tested, and the repair does not fully happen.",
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
              "questName": "Relational Feedback",
              "body": [
                "You can learn from what happens between people.",
                "You notice where trust gets tested.",
                "You see what needs repair.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the rupture.",
                "You think: “I pulled away fast there.”",
                "You think: “That needed a conversation, not just distance.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Test",
              "body": [
                "You notice it while it is happening.",
                "You feel the bond being tested, and you pause before reacting.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Repairing The Agreement",
              "body": [
                "You name what happened.",
                "You ask what needs to change.",
                "You listen for the real agreement.",
                "You repair what can be repaired.",
                "Trust becomes more honest than before."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Tested Trust",
              "body": [
                "You do not panic when friction appears.",
                "You let the relationship show you what is real.",
                "You repair without pretending.",
                "Your bonds become stronger because they can be tested."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When friction appears, look for the repair before you decide the bond has failed."
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
      "gate": 37,
      "line": 4,
      "gateLine": "37.4",
      "intro": {
        "questName": "Relational Pact",
        "openingStatement": "You’re naturally good at building trust through people, loyalty, and shared agreements.",
        "evidence": [
          "You notice who belongs in the circle.",
          "You understand the power of promises kept over time.",
          "You can help people feel held by a shared commitment."
        ],
        "limitation": "But you tend to protect comfort in the relationship instead of naming what the agreement really requires.",
        "purpose": "Your purpose is to let trust carry truth, not hide from it."
      },
  "shareCard": {
    "giftLine": "You build trust through loyalty and shared agreements.",
    "patternLine": "Comfort keeps you from naming what the agreement requires.",
    "questLine": "Let trust carry honesty, not hide from it."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You move through relationship.",
            "You build trust through consistency and shared care.",
            "You notice when people need to know where they stand.",
            "Your strength grows when the bond becomes honest, not just comfortable."
          ],
          "recognitionLines": [
            "But this is where it usually softens too much.",
            "You keep the peace, and the real agreement stays unspoken."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A friend needs honesty, but you soften it until the point disappears.",
            "A group agreement is unclear, but you avoid being the one to name it.",
            "Someone keeps taking from the relationship, and you keep making it comfortable.",
            "You know the circle needs a boundary, but you wait for someone else to say it."
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
              "You do not lack loyalty.",
              "You just sometimes protect the comfort of the bond instead of the truth inside it.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up through people",
            "body": [
              "It can feel like keeping everyone connected.",
              "It can look like being kind, loyal, or flexible.",
              "But sometimes the relationship needs truth more than it needs smoothness.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look like avoidance.",
              "It may look like keeping the group steady or giving people time.",
              "The core is the same:",
              "The bond stays comfortable, but the real agreement stays unclear.",
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
              "questName": "Loyal Connection",
              "body": [
                "You can build trust through relationship.",
                "You understand loyalty.",
                "You notice what keeps people connected.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the conversation.",
                "You think: “I made that easier, but not clearer.”",
                "You think: “We still do not know the real agreement.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Comfort",
              "body": [
                "You notice it while it is happening.",
                "You feel yourself choosing smoothness over truth.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Letting Trust Speak",
              "body": [
                "You say the honest thing cleanly.",
                "You clarify the expectation.",
                "You protect the bond by making it real.",
                "You let people know where they stand.",
                "The relationship becomes stronger because it is clearer."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Clean Loyalty",
              "body": [
                "You do not confuse peace with trust.",
                "You let relationships hold honest agreements.",
                "Your loyalty becomes clearer.",
                "People can trust your warmth because it has truth in it."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When the relationship needs truth, do not trade clarity for comfort."
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
      "gate": 37,
      "line": 5,
      "gateLine": "37.5",
      "intro": {
        "questName": "Bounded Support",
        "openingStatement": "You’re naturally good at becoming the person others trust to hold things together.",
        "evidence": [
          "People often look to you for reassurance.",
          "You can make a group feel supported when things get tense.",
          "You understand what people need from each other in practical terms."
        ],
        "limitation": "But you tend to become the support others expect before checking what you actually agreed to carry.",
        "purpose": "Your purpose is to offer support without becoming responsible for everyone’s stability."
      },
  "shareCard": {
    "giftLine": "You become the person others trust to hold things together.",
    "patternLine": "You take on more support than you actually agreed to.",
    "questLine": "Offer support without becoming everyone's stability."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "People can project safety onto you.",
            "You may become the one who holds the group together.",
            "You can see what support would actually help.",
            "Your strength grows when your care has boundaries."
          ],
          "recognitionLines": [
            "But this is where the pressure enters.",
            "People need you, and you become the agreement before you have made one."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "Everyone assumes you will handle the emotional cleanup.",
            "Someone expects loyalty from you before the relationship has earned it.",
            "A group leans on you, and you say yes before checking your capacity.",
            "You become the reliable one, then quietly resent how much you are carrying."
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
              "You do not lack care or usefulness.",
              "You just sometimes become the support role before the agreement is clear.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up under expectation",
            "body": [
              "It can feel like being the dependable one.",
              "It can look like helping, reassuring, or keeping the peace.",
              "But support becomes cleaner when it is chosen instead of assumed.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look like pressure at first.",
              "It may look like people naturally trusting you.",
              "The core is the same:",
              "You become the support before the boundary is clear.",
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
              "questName": "Practical Support",
              "body": [
                "You can see what people need from each other.",
                "You can offer steadiness.",
                "You know how support works in real life.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after you have said yes.",
                "You think: “I took on more than I agreed to.”",
                "You think: “They made me the steady one again.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Projection",
              "body": [
                "You notice it while it is happening.",
                "You feel people expecting you to be the support, and you pause.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Clarifying The Agreement",
              "body": [
                "You name what you can offer.",
                "You name what you cannot carry.",
                "You let care stay practical.",
                "You support without absorbing the whole field.",
                "The agreement becomes cleaner for everyone."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Bounded Care",
              "body": [
                "You do not become the role anymore.",
                "You offer support with clear limits.",
                "People know what they can count on.",
                "Your care becomes strong because it is not overextended."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When people expect you to hold it together, clarify what you are actually agreeing to carry."
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
      "gate": 37,
      "line": 6,
      "gateLine": "37.6",
      "intro": {
        "questName": "Embodied Kinship",
        "openingStatement": "You’re naturally good at seeing what makes relationships mature over time.",
        "evidence": [
          "You can recognize which bonds are truly reciprocal.",
          "You notice when loyalty has become habit instead of truth.",
          "You understand that belonging has to be lived, not just idealized."
        ],
        "limitation": "But you tend to step back and observe the relationship instead of returning to participate in it honestly.",
        "purpose": "Your purpose is to become a living example of mature, reciprocal trust."
      },
  "shareCard": {
    "giftLine": "You see what makes relationships mature over time.",
    "patternLine": "You step back from the relationship instead of participating.",
    "questLine": "Become a living example of mature, honest connection."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You can see the long arc of a relationship.",
            "You notice what is real and what is only familiar.",
            "You understand that loyalty must keep evolving.",
            "Your strength grows when perspective returns into honest participation."
          ],
          "recognitionLines": [
            "But this is where distance can look wise.",
            "You call it perspective, but part of you has already left the table."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You see the pattern in a family or group, but stop participating honestly.",
            "You know a relationship needs a new agreement, but you watch instead of entering the conversation.",
            "You outgrow an old loyalty, but stay distant rather than cleanly redefining it.",
            "You understand what mature care looks like, but hesitate to model it in real time."
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
              "You just sometimes leave the relationship in your mind before you return with the truth.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up through distance",
            "body": [
              "It can feel like maturity.",
              "It can look like giving people space or seeing the bigger picture.",
              "But sometimes the mature move is to come back and participate honestly.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not feel like withdrawal.",
              "It may feel like discernment, standards, or needing space.",
              "The core is the same:",
              "You can see the relationship clearly, but still need to live the next truth inside it.",
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
              "questName": "Long-View Trust",
              "body": [
                "You can see how relationships mature.",
                "You notice what lasts.",
                "You understand what loyalty becomes over time.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after you have stepped back.",
                "You think: “I saw it, but I did not enter it.”",
                "You think: “That needed my real participation.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Distance",
              "body": [
                "You notice it while it is happening.",
                "You feel yourself rising above the relationship instead of staying present in it.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Returning With Truth",
              "body": [
                "You come back into the conversation.",
                "You say what has matured.",
                "You redefine the agreement honestly.",
                "You model reciprocal care.",
                "The relationship has a chance to grow up with you."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Mature Kinship",
              "body": [
                "You do not escape into perspective anymore.",
                "You live the standard you can see.",
                "Your relationships become clearer and more reciprocal.",
                "Belonging becomes something you embody, not something you watch from a distance."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When you can see the relationship clearly, return and live the next honest agreement."
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
};

export default gate37UnderstandFlow;
