import type { MainQuestUnderstandFlow } from './types';

export const gate38UnderstandFlow: { gate: number; quality: { score: number; schemaValidation: string; status: string; target: string; standard: string }; entries: MainQuestUnderstandFlow[] } = {
  "gate": 38,
  "quality": {
    "score": 97,
    "schemaValidation": "PASS",
    "status": "Gold standard ready",
    "target": "96+",
    "standard": "Include top-level quality.score and quality.schemaValidation in every generated gate file and include the score in the filename."
  },
  "entries": [
    {
      "gate": 38,
      "line": 1,
      "gateLine": "38.1",
      "intro": {
        "questName": "Foundation of Worthy Struggle",
        "openingStatement": "You’re naturally good at sensing when something is worth fighting for.",
        "evidence": [
          "You notice when a challenge actually matters.",
          "You can feel when resistance is asking for commitment.",
          "You do not give up just because something is difficult."
        ],
        "limitation": "But you tend to hold back until you are sure the struggle is justified.",
        "purpose": "Your purpose is to choose the fight that matters and take the first real step."
      },
  "shareCard": {
    "giftLine": "You sense when something is genuinely worth fighting for.",
    "patternLine": "You hold back until you're sure the struggle is justified.",
    "questLine": "Choose the fight that matters. Take the first real step."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You can sense when struggle has meaning.",
            "You know not every battle deserves your energy.",
            "You look for the reason before you commit.",
            "Your strength grows when you stop waiting for perfect certainty before you stand for something."
          ],
          "recognitionLines": [
            "But this is where it usually stops.",
            "You almost take a stand, then look for one more reason to prove it is worth it."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You know a boundary matters, but you wait before saying it.",
            "A project gets hard, and you pause to decide if it deserves you.",
            "Someone challenges what you value, but you stay quiet until you feel fully ready.",
            "You feel the fight in you, then keep checking whether you are allowed to care that much."
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
              "You just wait for the struggle to feel fully justified before you enter it.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel reasonable.",
              "It can look like choosing your battles wisely.",
              "But those are often the moments where your real strength is being tested.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look obvious.",
              "It may look like researching, waiting, or needing a stronger reason.",
              "The core is the same:",
              "Something matters, but you delay standing for it.",
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
              "questName": "Sense of Worth",
              "body": [
                "You can feel when something matters.",
                "You do not waste energy on every fight.",
                "You look for meaning before you commit.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the moment passes.",
                "You think: “I should have said something there.”",
                "You think: “That mattered more than I admitted.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Threshold",
              "body": [
                "You notice it while it is happening.",
                "You feel yourself checking if the stand is justified.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Taking The Stand",
              "body": [
                "You name what matters.",
                "You take one clean step.",
                "You stop needing the whole path to be proven first.",
                "You let the struggle show you more.",
                "Your energy has somewhere real to go."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Grounded Resolve",
              "body": [
                "You do not fight everything.",
                "You do not avoid the real fight either.",
                "You can stand for what matters without overexplaining it.",
                "Your struggle becomes purposeful."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When something matters, take one clean step before asking for perfect proof."
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
      "gate": 38,
      "line": 2,
      "gateLine": "38.2",
      "intro": {
        "questName": "Natural Resolve",
        "openingStatement": "You’re naturally good at holding steady when something matters.",
        "evidence": [
          "You can stay with a challenge without making it dramatic.",
          "You know what deserves your energy before you can explain why.",
          "You often carry quiet determination that others may not see."
        ],
        "limitation": "But you tend to downplay your own resolve or wait for the struggle to name itself.",
        "purpose": "Your purpose is to own what matters without needing pressure to prove it."
      },
  "shareCard": {
    "giftLine": "You hold steady when something actually matters.",
    "patternLine": "You downplay your resolve or wait for pressure to prove it.",
    "questLine": "Own what matters without needing pressure to confirm it."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "Your strength can be quiet.",
            "You do not need to perform intensity to care deeply.",
            "You can stay with what matters naturally.",
            "Your strength grows when you stop acting like your resolve is accidental."
          ],
          "recognitionLines": [
            "But this is where it usually gets hidden.",
            "It comes naturally, so you act like it does not count until life pushes you."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You keep showing up for something, but call it no big deal.",
            "A cause matters to you, but you wait for someone else to make it serious.",
            "You endure a hard season quietly, then pretend it did not take strength.",
            "You know what you care about, but you avoid claiming how much it matters."
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
              "You do not lack resolve.",
              "You just treat your strength like it does not count because it comes quietly.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel reasonable.",
              "It can look like being casual, low-key, or not wanting attention.",
              "But those are often the moments where your real strength is being tested.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look obvious.",
              "It may show up as quiet consistency that you do not fully claim.",
              "The core is the same:",
              "You care more than you admit, but you wait for pressure to reveal it.",
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
              "questName": "Quiet Determination",
              "body": [
                "You can keep going without making noise.",
                "You know what matters in your body.",
                "You carry strength before you explain it.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the moment passes.",
                "You think: “I acted like that did not matter, but it did.”",
                "You think: “That mattered more than I admitted.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Care",
              "body": [
                "You notice it while it is happening.",
                "You feel your quiet determination becoming visible.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Claiming The Struggle",
              "body": [
                "You stop minimizing your care.",
                "You claim the thing that matters.",
                "You keep your effort clean.",
                "You let your strength be seen without performing it.",
                "The struggle becomes easier to respect."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Embodied Resolve",
              "body": [
                "You do not need life to force your strength out of hiding.",
                "You know what matters.",
                "You stay with it consciously.",
                "Your quiet resolve becomes dependable."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When your resolve is already there, do not pretend it is nothing."
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
      "gate": 38,
      "line": 3,
      "gateLine": "38.3",
      "intro": {
        "questName": "Tested Tenacity",
        "openingStatement": "You’re naturally good at learning through resistance.",
        "evidence": [
          "You discover what matters when life pushes back.",
          "You can adapt after setbacks.",
          "You often find your strength through the struggle itself."
        ],
        "limitation": "But you tend to read friction as a sign that the whole path is wrong.",
        "purpose": "Your purpose is to learn from resistance instead of restarting before the lesson lands."
      },
  "shareCard": {
    "giftLine": "You learn through resistance.",
    "patternLine": "Friction reads as a sign the whole path is off.",
    "questLine": "Learn from resistance instead of restarting before it lands."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You learn by meeting the edge.",
            "Resistance shows you what is real.",
            "Setbacks can sharpen your commitment.",
            "Your strength grows when you adjust instead of abandoning the whole fight."
          ],
          "recognitionLines": [
            "But this is where it usually gets messy.",
            "The fight gets uncomfortable, and you start treating the obstacle like proof to quit."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A plan hits resistance, and you immediately look for a new path.",
            "A conflict reveals what matters, but you turn it into a reason to leave.",
            "You try something hard, then judge yourself before you learn from it.",
            "You keep changing the fight instead of reading what the last one taught you."
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
              "You do not lack tenacity.",
              "You just sometimes confuse resistance with proof that you chose wrong.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel reasonable.",
              "It can look like being practical, flexible, or knowing when to move on.",
              "But those are often the moments where your real strength is being tested.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look obvious.",
              "It may look like repeated resets under different names.",
              "The core is the same:",
              "The fight gets hard, and you leave before the lesson becomes useful.",
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
              "questName": "Friction Reader",
              "body": [
                "You can learn from resistance.",
                "You notice what pressure reveals.",
                "You find useful feedback inside the struggle.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the moment passes.",
                "You think: “I left before I understood what that taught me.”",
                "You think: “That mattered more than I admitted.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Reset",
              "body": [
                "You notice it while it is happening.",
                "You feel the urge to reset before you have read the feedback.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Adjusting The Fight",
              "body": [
                "You pause before restarting.",
                "You ask what the resistance is showing you.",
                "You change the move, not the whole purpose.",
                "You carry the lesson forward.",
                "The struggle starts making you sharper."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Resilient Purpose",
              "body": [
                "You do not need the path to be smooth.",
                "You learn while staying engaged.",
                "You can meet resistance without making it your identity.",
                "Your purpose becomes tested and real."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When resistance appears, adjust the move before abandoning the purpose."
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
      "gate": 38,
      "line": 4,
      "gateLine": "38.4",
      "intro": {
        "questName": "Loyal Courage",
        "openingStatement": "You’re naturally good at standing for what matters through people and trust.",
        "evidence": [
          "You notice when someone needs an ally.",
          "You can feel when a relationship is asking for loyalty.",
          "You understand that some struggles are not meant to be faced alone."
        ],
        "limitation": "But you tend to protect comfort in the relationship instead of naming the fight that matters.",
        "purpose": "Your purpose is to let trust carry honest courage."
      },
  "shareCard": {
    "giftLine": "You stand for what matters through the people you trust.",
    "patternLine": "Protecting comfort keeps the real fight unnamed.",
    "questLine": "Let trust carry honest courage into the right moment."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "Your strength moves through relationship.",
            "You can stand with people when something matters.",
            "You understand loyalty as action, not just feeling.",
            "Your strength grows when connection becomes honest enough to carry conflict."
          ],
          "recognitionLines": [
            "But this is where it usually gets softened.",
            "You keep the bond comfortable, then avoid the stand the relationship actually needs."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A friend needs you to be direct, but you stay agreeable.",
            "A group avoids the real issue, and you help keep things smooth.",
            "Someone crosses a line, but you protect the relationship from conflict.",
            "You care enough to stand with someone, then soften the truth until it disappears."
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
              "You just sometimes protect the comfort of the bond instead of the courage inside it.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel reasonable.",
              "It can look like keeping peace, being kind, or protecting trust.",
              "But those are often the moments where your real strength is being tested.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look obvious.",
              "It may show up through friendships, teams, family, or groups.",
              "The core is the same:",
              "The relationship matters, but the real stand stays unnamed.",
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
              "questName": "Relational Strength",
              "body": [
                "You know how to stand with people.",
                "You feel when trust needs action.",
                "You understand the strength of loyalty.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the moment passes.",
                "You think: “I kept it comfortable, but I did not say the real thing.”",
                "You think: “That mattered more than I admitted.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Softening",
              "body": [
                "You notice it while it is happening.",
                "You feel yourself choosing smoothness over the honest stand.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Letting Trust Stand",
              "body": [
                "You say the hard thing cleanly.",
                "You let the bond carry truth.",
                "You stand with people without hiding the issue.",
                "You make loyalty active.",
                "The relationship becomes stronger because it is real."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Courageous Loyalty",
              "body": [
                "You do not confuse harmony with trust.",
                "You can stay connected while naming what matters.",
                "Your loyalty has courage inside it.",
                "People know where you stand."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When the relationship needs courage, do not trade the stand for comfort."
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
      "gate": 38,
      "line": 5,
      "gateLine": "38.5",
      "intro": {
        "questName": "Purposeful Opposition",
        "openingStatement": "You’re naturally good at becoming the person others expect to stand strong.",
        "evidence": [
          "People may look to you when something needs defending.",
          "You can become practical under pressure.",
          "You often see what is worth protecting before others do."
        ],
        "limitation": "But you tend to become the fighter others project onto you before checking if the fight is truly yours.",
        "purpose": "Your purpose is to stand for what matters without becoming every battle’s answer."
      },
  "shareCard": {
    "giftLine": "People expect you to be the one who stands strong.",
    "patternLine": "You become the fighter before checking if the fight is yours.",
    "questLine": "Stand for what matters. Not every battle is yours."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "People can project strength onto you.",
            "You may be asked to defend, challenge, or hold the line.",
            "You can be useful when a real stand is needed.",
            "Your strength grows when you choose the fight instead of becoming the role."
          ],
          "recognitionLines": [
            "But this is where the pressure enters.",
            "People need a fighter, and you become the stand before asking if it is yours."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A group expects you to say what everyone else avoids.",
            "Someone pulls you into their conflict because you seem strong enough to handle it.",
            "You defend a position before checking whether you actually believe in it.",
            "You become the brave one, then feel trapped carrying everyone’s battle."
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
              "You do not lack impact.",
              "You just sometimes become the fighter before the fight is clearly yours.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel reasonable.",
              "It can look like being useful, brave, direct, or protective.",
              "But those are often the moments where your real strength is being tested.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look obvious.",
              "It may feel like pressure, responsibility, or being made into the strong one.",
              "The core is the same:",
              "People expect you to stand, and you step into the role before checking the truth.",
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
              "questName": "Practical Courage",
              "body": [
                "You can be strong when it matters.",
                "You can protect what has value.",
                "You know how to stand under pressure.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the moment passes.",
                "You think: “I took that on before I knew it was mine.”",
                "You think: “That mattered more than I admitted.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Projection",
              "body": [
                "You notice it while it is happening.",
                "You feel people expecting you to become the fighter.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Choosing The Fight",
              "body": [
                "You pause before taking the role.",
                "You ask what actually matters.",
                "You name what you will and will not carry.",
                "You stand where your strength is clean.",
                "Your impact becomes more trustworthy."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Bounded Strength",
              "body": [
                "You do not become every battle’s answer.",
                "You choose what is worth your strength.",
                "You can stand without absorbing the projection.",
                "Your courage becomes practical and bounded."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When people expect you to fight, choose the stand before becoming the role."
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
      "gate": 38,
      "line": 6,
      "gateLine": "38.6",
      "intro": {
        "questName": "Embodied Purpose",
        "openingStatement": "You’re naturally good at seeing which struggles become meaningful over time.",
        "evidence": [
          "You can tell when a fight is petty and when it has purpose.",
          "You notice what struggle teaches across a longer arc.",
          "You understand that strength has to become lived, not just observed."
        ],
        "limitation": "But you tend to step back and judge the struggle instead of returning to participate in the one that matters.",
        "purpose": "Your purpose is to become a living example of strength used wisely."
      },
  "shareCard": {
    "giftLine": "You see which struggles become meaningful over time.",
    "patternLine": "You observe the struggle instead of returning to participate.",
    "questLine": "Return to it. Show what strength looks like when it counts."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You can see the bigger pattern behind struggle.",
            "You notice which battles mature a person and which ones drain them.",
            "You understand that not every opposition deserves participation.",
            "Your strength grows when perspective returns into lived courage."
          ],
          "recognitionLines": [
            "But this is where distance can look wise.",
            "You call it perspective, but part of you has already left the fight."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You see what a conflict is really about, but stay above it instead of acting cleanly.",
            "You understand what matters, but delay participating until the moment passes.",
            "You judge a struggle as immature, then avoid the part that is yours to live.",
            "You know the stronger standard, but hesitate to model it in real time."
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
              "You just sometimes leave the struggle in your mind before returning with clean action.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel reasonable.",
              "It can look like maturity, discernment, or not wanting drama.",
              "But those are often the moments where your real strength is being tested.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not look obvious.",
              "It may feel like distance, standards, or waiting for the situation to become cleaner.",
              "The core is the same:",
              "You can see what matters, but still need to live the next courageous step.",
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
              "questName": "Long-View Strength",
              "body": [
                "You can see what struggle becomes over time.",
                "You know which battles matter.",
                "You understand strength beyond reaction.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the moment passes.",
                "You think: “I saw it clearly, but I did not live it.”",
                "You think: “That mattered more than I admitted.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Distance",
              "body": [
                "You notice it while it is happening.",
                "You feel yourself rising above the struggle instead of entering the true part.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Returning With Courage",
              "body": [
                "You return to the real moment.",
                "You act without making the fight your identity.",
                "You model clean strength.",
                "You release what is not yours.",
                "You live the standard you can see."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Wise Resolve",
              "body": [
                "You do not escape into perspective anymore.",
                "You choose meaningful struggle with maturity.",
                "Your courage becomes calm and lived.",
                "Strength becomes something people can learn from."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When you can see the meaningful struggle, return and live the next clean step."
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

export default gate38UnderstandFlow;
