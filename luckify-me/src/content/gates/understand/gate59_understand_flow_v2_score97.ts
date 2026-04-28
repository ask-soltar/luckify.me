export type MainQuestUnderstandFlowEntry = {
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
      buttons: { id: "i_do_this" | "sometimes" | "not_really_me"; label: string }[];
    };
    responseReflection: {
      i_do_this: { title: string; body: string[]; ctaLabel: string };
      sometimes: { title: string; body: string[]; ctaLabel: string };
      not_really_me: { title: string; body: string[]; ctaLabel: string };
    };
    recognitionProgressionTree: {
      title: string;
      introLine: string;
      levels: {
        level: number;
        universalName: "The Gift" | "The Afterglow" | "The Catch" | "The Shift" | "The Embodiment";
        questName: string;
        body: string[];
      }[];
      finalCompletion: {
        badge: string;
        title: string;
        body: string[];
        cta: { label: string; enabled: boolean; nextScreen: "practice" };
        secondaryAction: { label: string; targetScreen: string };
      };
    };
  };
};

export type MainQuestUnderstandFlowGate = {
  gate: number;
  quality: {
    score: number;
    schemaValidation: "PASS" | "FAIL";
    status: string;
    target: string;
    standard: string;
  };
  entries: MainQuestUnderstandFlowEntry[];
};

export const gate59UnderstandFlow: MainQuestUnderstandFlowGate = {
  "gate": 59,
  "quality": {
    "score": 97,
    "schemaValidation": "PASS",
    "status": "Gold standard ready",
    "target": "96+",
    "standard": "Include top-level quality.score and quality.schemaValidation in every generated gate file and include the score in the filename."
  },
  "entries": [
    {
      "gate": 59,
      "line": 1,
      "gateLine": "59.1",
      "intro": {
        "questName": "Bold Intimacy",
        "openingStatement": "You’re naturally good at opening the door to real connection.",
        "evidence": [
          "You can feel when closeness wants to begin.",
          "You often notice the moment before someone else does.",
          "You have the courage to make connection possible."
        ],
        "limitation": "But you tend to wait for certainty before taking the first honest step.",
        "purpose": "Your purpose is to initiate real contact before fear turns it into distance."
      },
  "shareCard": {
    "giftLine": "You open the door to real connection.",
    "patternLine": "You wait for certainty before taking the first honest step.",
    "questLine": "Initiate real contact before hesitation turns it into distance."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You can sense when a connection is ready to open.",
            "You notice the first moment where honesty could begin.",
            "You know when the space between people is asking for a step.",
            "Your gift starts when you choose contact before everything feels safe."
          ],
          "recognitionLines": [
            "But this is where it usually stops.",
            "You almost say the honest thing, then wait for the moment to feel safer."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You want to reach out, but you wait until the reason feels perfect.",
            "A conversation gets close, then you hold back the real question.",
            "You feel the opening, but you let the other person go first.",
            "You know the first step is yours, but you delay it until the moment passes."
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
              "You do not lack the ability to connect.",
              "You stop at the threshold when closeness starts asking for courage.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel normal in the moment.",
              "It may look like keeping things easy, safe, useful, or smooth.",
              "Connection is ready, but you wait for certainty first.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not show up in the obvious way.",
              "It may appear in small moments where connection begins and then changes shape.",
              "The core is the same:",
              "Connection is ready, but you wait for certainty first.",
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
              "questName": "First Contact",
              "body": [
                "You can feel the beginning of connection.",
                "You notice when a wall starts to soften.",
                "You understand that closeness needs someone to begin.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the moment is gone.",
                "You think: “I could have reached out there.”",
                "You think: “That was the opening.”",
                "The moment passes, but you start seeing the threshold."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Threshold",
              "body": [
                "You notice it while it is happening.",
                "You feel the chance to speak, reach out, or make contact.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Taking The First Step",
              "body": [
                "You stop waiting for perfect safety.",
                "You say the honest thing sooner.",
                "You let closeness begin before you can control the outcome.",
                "You make the first clean move.",
                "The connection has somewhere to go."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Bold Intimacy",
              "body": [
                "You do not hide behind hesitation anymore.",
                "You initiate real connection with courage.",
                "People feel the sincerity of your first step.",
                "Closeness begins because you are willing to enter."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When connection is ready to begin, take the first honest step."
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
      "gate": 59,
      "line": 2,
      "gateLine": "59.2",
      "intro": {
        "questName": "Transformative Connection",
        "openingStatement": "You’re naturally good at creating connection.",
        "evidence": [
          "Things open quickly around you.",
          "People respond to you.",
          "Opportunities show up."
        ],
        "limitation": "But you tend to keep things comfortable instead of letting them become real.",
        "purpose": "Your purpose is to let those moments actually go somewhere."
      },
      "shareCard": {
        "giftLine": "You create connection naturally.",
        "patternLine": "When it starts to matter, you keep it comfortable.",
        "questLine": "Let the moment become real."
      },
      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You create connection easily.",
            "People open up.",
            "Conversations warm up.",
            "Opportunities start naturally."
          ],
          "recognitionLines": [
            "But this is where it usually stops.",
            "You keep things comfortable instead of letting them become real."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A conversation gets personal, then you change the tone.",
            "Someone opens up, but you don’t respond honestly.",
            "An opportunity appears, but you don’t take the next step.",
            "Something meaningful starts, but you leave it there."
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
              "You don’t struggle to create connection.",
              "You just stop it before it becomes real.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up more than you think",
            "body": [
              "It’s subtle.",
              "It often feels like keeping things smooth or keeping things easy.",
              "But those are the moments that could have gone further.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern isn’t always obvious.",
              "But the core is the same:",
              "Something opens, and it doesn’t get taken further.",
              "Watch for that.",
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
              "questName": "Natural Connection",
              "body": [
                "Connection happens easily.",
                "People open up.",
                "Things begin without effort.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after it’s over.",
                "You think: “I could have said something there.”",
                "You think: “That could have gone somewhere.”",
                "The moment is gone, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching It In The Moment",
              "body": [
                "You notice it while it’s happening.",
                "You feel the moment opening, and you hesitate.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Taking The Step",
              "body": [
                "You start acting in the moment.",
                "You say it.",
                "You follow up.",
                "You stay instead of leaving.",
                "Things begin to move."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Transformative Presence",
              "body": [
                "You don’t stop it anymore.",
                "Connection becomes real.",
                "Things move forward.",
                "Moments change outcomes."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When something opens, don’t stop it early."
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
      "gate": 59,
      "line": 3,
      "gateLine": "59.3",
      "intro": {
        "questName": "Playful Bonding",
        "openingStatement": "You’re naturally good at making connection feel easy.",
        "evidence": [
          "You can warm up a room without forcing it.",
          "People loosen up around your energy.",
          "You know how to make contact feel less heavy."
        ],
        "limitation": "But you tend to let playfulness replace depth instead of leading into it.",
        "purpose": "Your purpose is to use warmth and ease to help real connection develop."
      },
  "shareCard": {
    "giftLine": "You make connection feel easy and natural.",
    "patternLine": "Playfulness replaces depth instead of leading into it.",
    "questLine": "Let warmth and ease help real connection develop."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You bring movement into connection.",
            "You help people relax.",
            "You make the first layer of closeness feel safe.",
            "Your gift opens the door through lightness."
          ],
          "recognitionLines": [
            "But this is where it can scatter.",
            "You get the spark going, then keep it playful so it never has to settle."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You joke when the conversation starts getting real.",
            "You create a fun moment, but avoid the follow-up.",
            "You keep many connections active, but few become deeper.",
            "You feel the bond forming, then turn it into entertainment."
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
              "You do not lack warmth or social ease.",
              "You can leave the connection at the spark instead of letting it deepen.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel normal in the moment.",
              "It may look like keeping things easy, safe, useful, or smooth.",
              "Connection opens through play, but you keep it from landing.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not show up in the obvious way.",
              "It may appear in small moments where connection begins and then changes shape.",
              "The core is the same:",
              "Connection opens through play, but you keep it from landing.",
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
              "questName": "Warm Contact",
              "body": [
                "You bring ease into connection.",
                "People relax around you.",
                "The mood becomes lighter.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the interaction ends.",
                "You think: “That was fun, but it stayed on the surface.”",
                "You think: “I could have stayed with that a little longer.”",
                "The moment passes, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Spark",
              "body": [
                "You notice it while the spark is happening.",
                "You feel the choice between keeping it light and letting it deepen.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Letting Warmth Land",
              "body": [
                "You keep the ease, but stop using it to escape.",
                "You let the conversation stay real for a little longer.",
                "You follow the spark into honest contact.",
                "You stop spreading your energy too thin.",
                "The bond starts to strengthen."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Playful Bonding",
              "body": [
                "Your warmth opens real connection.",
                "Play becomes a doorway, not a hiding place.",
                "People feel safe and seen around you.",
                "Joy and depth can exist together."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When play opens the door, stay long enough for connection to deepen."
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
      "gate": 59,
      "line": 4,
      "gateLine": "59.4",
      "intro": {
        "questName": "Trusted Openness",
        "openingStatement": "You’re naturally good at creating trust between people.",
        "evidence": [
          "You help others feel welcomed.",
          "You notice what makes connection feel safe.",
          "You can turn friendliness into belonging."
        ],
        "limitation": "But you tend to open the door without keeping the connection clear.",
        "purpose": "Your purpose is to build intimacy where openness and boundaries grow together."
      },
  "shareCard": {
    "giftLine": "You create real trust between the people around you.",
    "patternLine": "You open the door without keeping the connection clear.",
    "questLine": "Build intimacy where openness and limits grow together."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You create connection through trust.",
            "People feel included around you.",
            "You make closeness feel less threatening.",
            "Your gift helps belonging become possible."
          ],
          "recognitionLines": [
            "But this is where it can blur.",
            "You make it feel safe for everyone, then forget to keep the connection clean for yourself."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "You say yes to closeness before you know what you actually want.",
            "You keep a friendship warm, but avoid the honest boundary.",
            "A group feels comfortable, but the real issue stays unspoken.",
            "You let people in, then feel responsible for the emotional mess."
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
              "You do not lack openness or care.",
              "You can confuse being available with being clearly connected.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel normal in the moment.",
              "It may look like keeping things easy, safe, useful, or smooth.",
              "Connection feels safe, but the boundary is unclear.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not show up in the obvious way.",
              "It may appear in small moments where connection begins and then changes shape.",
              "The core is the same:",
              "Connection feels safe, but the boundary is unclear.",
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
              "questName": "Trust Builder",
              "body": [
                "You know how to create warmth.",
                "People feel more open around you.",
                "You make belonging easier.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after the connection becomes confusing.",
                "You think: “I let that get too blurry.”",
                "You think: “I should have been clearer earlier.”",
                "The moment passes, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Blur",
              "body": [
                "You notice it while closeness is forming.",
                "You feel the moment where trust needs a boundary.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Keeping Connection Clean",
              "body": [
                "You stay open without overextending.",
                "You speak the boundary sooner.",
                "You let trust include honesty.",
                "You stop protecting comfort at the cost of clarity.",
                "The connection becomes healthier."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Trusted Openness",
              "body": [
                "You create intimacy people can trust.",
                "Your openness has structure.",
                "Belonging feels safe without becoming tangled.",
                "Connection deepens because it stays clean."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When closeness grows, let honesty keep it clean."
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
      "gate": 59,
      "line": 5,
      "gateLine": "59.5",
      "intro": {
        "questName": "Unifying Influence",
        "openingStatement": "You’re naturally good at bringing people together.",
        "evidence": [
          "People often respond to your warmth or presence.",
          "You can dissolve tension in a room.",
          "You know how to turn separation into shared direction."
        ],
        "limitation": "But you tend to become the connector people expect instead of checking what is actually sincere.",
        "purpose": "Your purpose is to use influence to create genuine unity, not just agreement."
      },
  "shareCard": {
    "giftLine": "You bring people together with genuine pull.",
    "patternLine": "You become the expected connector before checking what's real.",
    "questLine": "Use the pull to create genuine unity, not just agreement."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "Your connection has impact.",
            "People may look to you to create harmony.",
            "You can help a room move from distance into trust.",
            "Your gift becomes useful when it serves something real."
          ],
          "recognitionLines": [
            "But this is where projection enters.",
            "You become the person who can bring everyone together before asking whether the bond is honest."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A group expects you to smooth things over, so you do.",
            "Someone is drawn to your warmth, and you keep the charm going.",
            "You create unity quickly, but avoid naming what is not sincere.",
            "You feel responsible for keeping people connected even when the connection is weak."
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
              "You do not lack influence or magnetism.",
              "You can start serving the projection instead of the truth of the connection.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel normal in the moment.",
              "It may look like keeping things easy, safe, useful, or smooth.",
              "People gather around you, but sincerity has to lead.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not show up in the obvious way.",
              "It may appear in small moments where connection begins and then changes shape.",
              "The core is the same:",
              "People gather around you, but sincerity has to lead.",
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
              "questName": "Magnetic Connection",
              "body": [
                "People respond to your presence.",
                "You can create warmth quickly.",
                "You help barriers soften.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after you have carried the room.",
                "You think: “I made that work, but was it real?”",
                "You think: “I became what they needed.”",
                "The moment passes, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Projection",
              "body": [
                "You notice it while others are looking to you.",
                "You feel the pressure to charm, fix, unite, or smooth things over.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Leading With Sincerity",
              "body": [
                "You stop using warmth to manage the room.",
                "You let connection be honest before it becomes unified.",
                "You create harmony without performing it.",
                "You set the boundary before taking the role.",
                "The field becomes more real."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Unifying Influence",
              "body": [
                "Your influence creates genuine trust.",
                "People come together around something sincere.",
                "You can lead connection without becoming the projection.",
                "Unity becomes grounded instead of performed."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When people look to you to unite the field, make sincerity the first condition."
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
      "gate": 59,
      "line": 6,
      "gateLine": "59.6",
      "intro": {
        "questName": "Free Intimacy",
        "openingStatement": "You’re naturally good at letting connection be real without needing to own it.",
        "evidence": [
          "You can feel the value of a moment without forcing it to last.",
          "You understand that some bonds need space to breathe.",
          "You can allow connection to change without making it wrong."
        ],
        "limitation": "But you tend to use freedom as a way to leave before intimacy becomes grounded.",
        "purpose": "Your purpose is to honor connection fully, whether it lasts for a moment or a lifetime."
      },
  "shareCard": {
    "giftLine": "You let connection be real without needing to own it.",
    "patternLine": "You use freedom to leave before the connection gets grounded.",
    "questLine": "Honor the connection fully, however long it lasts."
  },

      "understandFlow": {
        "patternExpansion": {
          "title": "What this means",
          "body": [
            "You understand the changing nature of connection.",
            "You can let intimacy breathe.",
            "You can value a bond without trapping it.",
            "Your gift is spacious closeness."
          ],
          "recognitionLines": [
            "But this is where it can disappear.",
            "You call it freedom, but part of you is already leaving before the connection can deepen."
          ],
          "exploreCtaLabel": "Explore the Pattern in Detail",
          "skipCtaLabel": "Skip to Growth Path"
        },
        "realLifeExamples": {
          "title": "Where this shows up",
          "examples": [
            "A connection feels meaningful, then you avoid the next grounded step.",
            "You keep things open-ended so nothing has to be named.",
            "You move on quickly and tell yourself the moment served its purpose.",
            "You want closeness, but resist the responsibility that comes with it."
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
              "You do not lack depth or sensitivity.",
              "You can leave too early and call it freedom.",
              "This is where your quest lives.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "sometimes": {
            "title": "This shows up quietly",
            "body": [
              "It can feel normal in the moment.",
              "It may look like keeping things easy, safe, useful, or smooth.",
              "Connection can be fluid, but it still needs presence.",
              "You’ll start noticing this faster now."
            ],
            "ctaLabel": "Show my growth path"
          },
          "not_really_me": {
            "title": "It may look different for you",
            "body": [
              "This pattern may not show up in the obvious way.",
              "It may appear in small moments where connection begins and then changes shape.",
              "The core is the same:",
              "Connection can be fluid, but it still needs presence.",
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
              "questName": "Spacious Connection",
              "body": [
                "You can connect without trying to control the bond.",
                "You respect the natural movement of relationships.",
                "You understand that closeness needs room.",
                "This is where you already have the gift."
              ]
            },
            {
              "level": 2,
              "universalName": "The Afterglow",
              "questName": "Catching It After",
              "body": [
                "You notice it after you have already stepped away.",
                "You think: “I left before I knew what that was.”",
                "You think: “That may have needed more presence.”",
                "The moment passes, but you start seeing the pattern."
              ]
            },
            {
              "level": 3,
              "universalName": "The Catch",
              "questName": "Catching The Exit",
              "body": [
                "You notice it while you are beginning to pull back.",
                "You feel the difference between giving space and leaving early.",
                "This is the turning point."
              ]
            },
            {
              "level": 4,
              "universalName": "The Shift",
              "questName": "Staying Without Owning",
              "body": [
                "You stay present without trying to trap the connection.",
                "You name what is real without demanding permanence.",
                "You let freedom include responsibility.",
                "You stop using openness to avoid depth.",
                "The bond can breathe and still matter."
              ]
            },
            {
              "level": 5,
              "universalName": "The Embodiment",
              "questName": "Free Intimacy",
              "body": [
                "You honor connection without possession.",
                "You can stay present inside change.",
                "Brief bonds and lasting bonds both become meaningful.",
                "Freedom serves honesty instead of escape."
              ]
            }
          ],
          "finalCompletion": {
            "badge": "Path Revealed",
            "title": "You’ve seen the full progression.",
            "body": [
              "You’ve seen how this quest develops.",
              "The next step is using it in real life.",
              "When connection changes shape, stay honest before you step away."
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

export default gate59UnderstandFlow;
