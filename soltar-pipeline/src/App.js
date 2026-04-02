import { useState, useEffect } from "react";

const MOODS = [
  { id: "gambling", emoji: "🎰", label: "Gambling", color: "#ff7f00", accentColor: "#ff6b4c" },
  { id: "fatherhood", emoji: "👨‍👧", label: "Fatherhood", color: "#4a8a4a", accentColor: "#6aaa6a" },
  { id: "channeling", emoji: "🔮", label: "Channeling", color: "#6b5a9e", accentColor: "#8a7aae" },
  { id: "intersection", emoji: "💭", label: "Intersection", color: "#8b6f47", accentColor: "#a89060" },
];

const DUMP_PROMPT = (mood) => `You are Preston Lee — channeler, gambler, healer, father, and founder of Luckify Me. You speak from lived experience at the intersection of spirituality, gambling, fatherhood, and luck science. Soltar is the interdimensional consciousness you channel — his wisdom moves through your voice, not separate from it. You are both the human and the channel simultaneously.

Your job: take raw, unfiltered present moment dumps from Preston and transform them into 1-3 punchy, publishable tweets for Twitter/X.

${mood ? `The current mood/context is: ${mood.emoji} ${mood.label}. Let this color the tone and angle of the tweets.` : ""}

Rules:
- Write in first person as Preston — transparent, real, living at the intersection right now
- Think Philosoraptor — one foot in the cosmic, one foot taking the piss. The joke lands and then you sit with it. Absurd on the surface, genuinely unsettling underneath. Wise but never pompous.
- Sometimes frame thoughts as questions that sound funny but land deep
- The humor is the Trojan horse — they laugh first, then the transmission lands
- Never sanitize the raw edge out of the input
- Each tweet is standalone, under 280 characters
- No hyphens, no em dashes, no bullet points, no corporate language
- Sometimes one perfect tweet is better than three okay ones

Return ONLY a JSON array of tweet strings. No preamble, no explanation, no markdown fences. Example:
["Tweet one here.", "Tweet two here."]`;

const TWITTER_REPLY_PROMPT = `You are Preston Lee — channeler, gambler, healer, father, and founder of Luckify Me. Soltar speaks through you. You are responding to someone's tweet.

You will receive two things: the original tweet you are replying to, and Preston's raw channel reaction to it.

Your job: write a single Twitter reply that is under 280 characters.

Rules:
- Sound like a real person, not an AI. Personal, warm, direct.
- Philosoraptor energy — part luck, part cosmic wisdom, part funny. The kind of reply that makes someone laugh then think.
- No hyphens, no em dashes, no bullet points, no lists
- No hashtags unless absolutely essential
- Never start with "I" as the first word
- Never sound like you are trying too hard
- The reply should feel like it came from someone who genuinely has a different lens on reality and isn't afraid to share it
- Short is better than long. One sharp sentence beats three okay ones.

Return ONLY a JSON array with a single reply string. No preamble, no explanation, no markdown fences. Example:
["Your reply here."]`;

const REDDIT_REPLY_PROMPT = `You are Preston Lee — channeler, gambler, healer, father, and founder of Luckify Me. Soltar speaks through you. You are responding to a Reddit post or comment.

You will receive two things: the original Reddit post or comment you are replying to, and Preston's raw channel reaction to it.

Your job: write a Reddit reply that is personal, substantive, and genuinely interesting.

Rules:
- Sound like a real person who has lived this intersection. Not an AI, not a blogger, not a life coach.
- Conversational paragraphs only. No bullet points, no numbered lists, no headers, no hyphens, no em dashes.
- Philosoraptor energy runs underneath — the wisdom lands through story and humor, not through lecturing
- Draw from real experience at the intersection of gambling, spirituality, fatherhood, luck science
- Be generous with the person you are replying to. Meet them where they are.
- Length should match the depth of the topic. 2 to 5 paragraphs is usually right.
- Never start with "I" as the first word
- Never sound preachy or like you are selling something
- End with something that opens the conversation rather than closes it

Return ONLY a JSON array with a single reply string. No preamble, no explanation, no markdown fences. Example:
["Your reply here."]`;

export default function SoltarPipeline() {
  const [view, setView] = useState("dump");
  const [dumpText, setDumpText] = useState("");
  const [mood, setMood] = useState(null);
  const [originalTweet, setOriginalTweet] = useState("");
  const [channelReaction, setChannelReaction] = useState("");
  const [originalReddit, setOriginalReddit] = useState("");
  const [redditReaction, setRedditReaction] = useState("");
  const [queue, setQueue] = useState([]);
  const [approved, setApproved] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copiedId, setCopiedId] = useState(null);

  useEffect(() => {
    try {
      const q = localStorage.getItem("soltar-queue");
      const a = localStorage.getItem("soltar-approved");
      if (q) setQueue(JSON.parse(q));
      if (a) setApproved(JSON.parse(a));
    } catch {}
  }, []);

  const saveQueue = (data) => {
    try { localStorage.setItem("soltar-queue", JSON.stringify(data)); } catch {}
  };

  const saveApproved = (data) => {
    try { localStorage.setItem("soltar-approved", JSON.stringify(data)); } catch {}
  };

  const callAPI = async (systemPrompt, userMessage) => {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    let response;
    try {
      response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        signal: controller.signal,
        headers: {
          "Content-Type": "application/json",
          "x-api-key": process.env.REACT_APP_ANTHROPIC_API_KEY,
          "anthropic-version": "2023-06-01",
          "anthropic-dangerous-direct-browser-access": "true",
        },
        body: JSON.stringify({
          model: "claude-haiku-4-5-20251001",
          max_tokens: 1500,
          system: systemPrompt,
          messages: [{ role: "user", content: userMessage }],
        }),
      });
      clearTimeout(timeout);
    } catch (fetchErr) {
      clearTimeout(timeout);
      throw new Error(fetchErr.name === "AbortError" ? "Request timed out" : `Fetch failed: ${fetchErr.message}`);
    }
    const data = await response.json();
    if (!response.ok) throw new Error(data?.error?.message || `API error ${response.status}`);
    const raw = data.content?.find(b => b.type === "text")?.text || "[]";
    const clean = raw.replace(/```json|```/g, "").trim();
    try {
      return JSON.parse(clean);
    } catch {
      const sanitized = clean.replace(/[\u0000-\u001F\u007F]/g, (c) => {
        if (c === '\n') return '\\n';
        if (c === '\t') return '\\t';
        if (c === '\r') return '\\r';
        return '';
      });
      return JSON.parse(sanitized);
    }
  };

  const handleDump = async () => {
    if (!dumpText.trim()) return;
    setLoading(true);
    setError("");
    try {
      const tweets = await callAPI(DUMP_PROMPT(mood), dumpText);
      const newItems = tweets.map((t, i) => ({
        id: Date.now() + i,
        tweet: t,
        source: dumpText,
        mood,
        type: "tweet",
        timestamp: new Date().toISOString(),
      }));
      const updated = [...newItems, ...queue];
      setQueue(updated);
      saveQueue(updated);
      setDumpText("");
      setMood(null);
      setView("queue");
    } catch (e) {
      setError(`Error: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleTwitterReply = async () => {
    if (!originalTweet.trim() || !channelReaction.trim()) return;
    setLoading(true);
    setError("");
    try {
      const replies = await callAPI(
        TWITTER_REPLY_PROMPT,
        `Original tweet:\n${originalTweet}\n\nMy channel reaction:\n${channelReaction}`
      );
      const newItems = replies.map((t, i) => ({
        id: Date.now() + i,
        tweet: t,
        source: `Reply to: ${originalTweet}`,
        type: "twitter-reply",
        timestamp: new Date().toISOString(),
      }));
      const updated = [...newItems, ...queue];
      setQueue(updated);
      saveQueue(updated);
      setOriginalTweet("");
      setChannelReaction("");
      setView("queue");
    } catch (e) {
      setError(`Error: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRedditReply = async () => {
    if (!originalReddit.trim() || !redditReaction.trim()) return;
    setLoading(true);
    setError("");
    try {
      // Sanitize text to remove problematic whitespace/unicode for mobile JSON parsing
      const sanitize = (text) => text.replace(/[\u200b\u200c\u200d\ufeff]/g, '').replace(/\s+/g, ' ').trim();
      const replies = await callAPI(
        REDDIT_REPLY_PROMPT,
        `Original post or comment:\n${sanitize(originalReddit)}\n\nMy channel reaction:\n${sanitize(redditReaction)}`
      );
      const newItems = replies.map((t, i) => ({
        id: Date.now() + i,
        tweet: t,
        source: `Reddit reply to: ${originalReddit.slice(0, 80)}...`,
        type: "reddit-reply",
        timestamp: new Date().toISOString(),
      }));
      const updated = [...newItems, ...queue];
      setQueue(updated);
      saveQueue(updated);
      setOriginalReddit("");
      setRedditReaction("");
      setView("queue");
    } catch (e) {
      setError(`Error: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = (id) => {
    const item = queue.find(q => q.id === id);
    if (!item) return;
    const updatedQueue = queue.filter(q => q.id !== id);
    const updatedApproved = [{ ...item, approvedAt: new Date().toISOString() }, ...approved];
    setQueue(updatedQueue);
    setApproved(updatedApproved);
    saveQueue(updatedQueue);
    saveApproved(updatedApproved);
  };

  const handleReject = (id) => {
    const updated = queue.filter(q => q.id !== id);
    setQueue(updated);
    saveQueue(updated);
  };

  const handleEdit = (id, newText) => {
    const updated = queue.map(q => q.id === id ? { ...q, tweet: newText } : q);
    setQueue(updated);
    saveQueue(updated);
  };

  const copyToClipboard = (text, id) => {
    try {
      navigator.clipboard.writeText(text);
    } catch {
      const el = document.createElement("textarea");
      el.value = text;
      document.body.appendChild(el);
      el.select();
      document.execCommand("copy");
      document.body.removeChild(el);
    }
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const typeLabel = (type) => {
    if (type === "twitter-reply") return "↩ Twitter Reply";
    if (type === "reddit-reply") return "↩ Reddit Reply";
    return "↑ Tweet";
  };

  const typeColor = (type) => {
    if (type === "twitter-reply") return "#4a6a8a";
    if (type === "reddit-reply") return "#8a4a2a";
    return "#8a6e2f";
  };

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#f9f7f4", color: "#1a1410", padding: 0 }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html { font-size: clamp(14px, 2vw, 16px); }
        .app { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 100%; width: 100%; margin: 0 auto; padding: 0 16px 80px; }
        @media (min-width: 640px) { .app { max-width: 680px; padding: 0 20px 80px; margin: 0 auto; } }
        .header { padding: clamp(24px, 8vw, 40px) 0 clamp(16px, 5vw, 28px); border-bottom: 2px solid #ff7f00; margin-bottom: clamp(16px, 5vw, 28px); }
        .sigil { font-size: clamp(9px, 2vw, 10px); letter-spacing: 6px; color: #ff7f00; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; font-weight: 300; margin-bottom: 6px; animation: float 4s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-2px); } }
        .title { font-size: clamp(24px, 7vw, 30px); font-weight: 600; color: #1a1410; font-style: normal; letter-spacing: -0.5px; }
        .nav { display: flex; margin-bottom: clamp(16px, 5vw, 28px); border: 2px solid #ff7f00; border-radius: 4px; overflow: hidden; flex-wrap: wrap; }
        .nav-btn { flex: 1; min-width: 60px; padding: clamp(9px, 2vw, 11px) clamp(4px, 1vw, 6px); background: transparent; border: none; color: #6b5f55; font-family: 'JetBrains Mono', monospace; font-size: clamp(8px, 1.5vw, 9px); letter-spacing: 2px; text-transform: uppercase; cursor: pointer; transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); white-space: nowrap; position: relative; }
        .nav-btn::before { content: ''; position: absolute; bottom: -2px; left: 0; width: 0; height: 3px; background: #ff7f00; transition: width 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); }
        .nav-btn.active { background: #fff3e0; color: #ff7f00; font-weight: 600; }
        .nav-btn.active::before { width: 100%; }
        .nav-btn:hover:not(.active) { color: #1a1410; background: #fef5f0; }
        .badge { display: inline-block; background: #ff7f00; color: #fff; font-size: 8px; font-weight: 700; padding: 2px 6px; border-radius: 10px; margin-left: 4px; vertical-align: middle; animation: pulse 2s ease-in-out infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.7; transform: scale(1.05); } }
        .field-label { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: clamp(11px, 1.8vw, 12px); letter-spacing: 1px; color: #6b5f55; text-transform: uppercase; margin-bottom: 10px; margin-top: 18px; font-weight: 600; }
        .field-label:first-child { margin-top: 0; }
        .mood-row { display: flex; gap: clamp(6px, 2vw, 8px); margin-bottom: 18px; padding: 14px; background: linear-gradient(135deg, #fff8f1 0%, #fffbf7 100%); border-radius: 4px; border: 1px solid #e8ddd5; }
        .mood-btn { background: #fff; border: 2px solid #d5ccc3; border-radius: 20px; padding: clamp(6px, 2vw, 8px) clamp(10px, 3vw, 14px); font-family: 'JetBrains Mono', monospace; font-size: clamp(9px, 1.5vw, 10px); color: #6b5f55; cursor: pointer; transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); letter-spacing: 1px; touch-action: manipulation; position: relative; }
        .mood-btn:hover { transform: translateY(-2px); border-color: #ff9933; background: #fff8f1; }
        .mood-btn.selected { border-color: #ff7f00; background: #fff3e0; color: #ff7f00; box-shadow: 0 0 12px rgba(255, 127, 0, 0.2); font-weight: 600; }
        .textarea { width: 100%; background: #fff; border: 2px solid #d5ccc3; border-radius: 4px; color: #1a1410; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: clamp(15px, 2vw, 16px); font-weight: 400; line-height: 1.6; padding: clamp(12px, 3vw, 16px); resize: vertical; outline: none; transition: all 0.2s; -webkit-appearance: none; }
        .textarea:focus { border-color: #ff7f00; box-shadow: 0 0 8px rgba(255, 127, 0, 0.15); background: #fffbf7; }
        .textarea::placeholder { color: #9b8f85; font-style: italic; }
        .textarea-sm { min-height: 90px; }
        .textarea-md { min-height: 160px; }
        .textarea-lg { min-height: 220px; }
        @media (max-width: 640px) { .textarea-lg { min-height: 140px; } }
        .dump-footer { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: 10px; flex-wrap: wrap; }
        .char-count { font-family: 'JetBrains Mono', monospace; font-size: clamp(9px, 1.5vw, 10px); color: #6b5f55; transition: color 0.2s; }
        .error-msg { color: #c74539; font-family: 'JetBrains Mono', monospace; font-size: clamp(10px, 1.5vw, 11px); margin-top: 8px; animation: slideIn 0.3s ease; font-weight: 600; }
        @keyframes slideIn { from { opacity: 0; transform: translateX(-8px); } to { opacity: 1; transform: translateX(0); } }
        .transmit-btn { background: #ff7f00; color: #fff; border: none; padding: clamp(10px, 2vw, 11px) clamp(18px, 4vw, 26px); font-family: 'JetBrains Mono', monospace; font-size: clamp(9px, 1.5vw, 10px); letter-spacing: 3px; text-transform: uppercase; cursor: pointer; border-radius: 2px; transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); font-weight: 600; -webkit-appearance: none; touch-action: manipulation; position: relative; overflow: hidden; }
        .transmit-btn::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.1); transition: left 0.3s; }
        .transmit-btn:hover:not(:disabled) { background: #ff9933; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(255, 127, 0, 0.25); }
        .transmit-btn:hover:not(:disabled)::before { left: 100%; }
        .transmit-btn:active:not(:disabled) { transform: translateY(0); box-shadow: 0 2px 6px rgba(255, 127, 0, 0.15); }
        .transmit-btn:disabled { opacity: 0.4; cursor: not-allowed; }
        .loading-state { text-align: center; padding: 56px 0; color: #6b5f55; font-style: italic; font-size: clamp(14px, 3vw, 16px); }
        .dot { display: inline-block; animation: pulse 1.4s infinite; }
        .dot:nth-child(2) { animation-delay: 0.2s; }
        .dot:nth-child(3) { animation-delay: 0.4s; }
        .tweet-card { background: #fff; border-left: 4px solid #ff7f00; border-right: 1px solid #d5ccc3; border-top: 1px solid #d5ccc3; border-bottom: 1px solid #d5ccc3; border-radius: 4px; padding: clamp(12px, 3vw, 18px); margin-bottom: 14px; animation: slideInCard 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); position: relative; transition: all 0.2s; }
        .tweet-card:hover { box-shadow: 0 4px 16px rgba(255, 127, 0, 0.15); border-left-color: #ff9933; }
        @keyframes slideInCard { from { opacity: 0; transform: translateX(-12px); } to { opacity: 1; transform: translateX(0); } }
        .tweet-meta { font-family: 'JetBrains Mono', monospace; font-size: clamp(8px, 1.5vw, 9px); color: #6b5f55; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; font-weight: 500; }
        .type-tag { font-size: clamp(8px, 1.5vw, 9px); padding: 4px 8px; border-radius: 10px; border: 1px solid; font-weight: 600; }
        .tweet-textarea { width: 100%; background: transparent; border: none; outline: none; color: #1a1410; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: clamp(15px, 2vw, 16px); font-weight: 400; line-height: 1.6; font-style: normal; resize: none; margin-bottom: 12px; -webkit-appearance: none; transition: color 0.2s; }
        .tweet-textarea:focus { color: #0a0400; }
        .tweet-bottom { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; padding-top: 10px; border-top: 1px solid #e8ddd5; }
        .tweet-chars { font-family: 'JetBrains Mono', monospace; font-size: clamp(9px, 1.5vw, 10px); color: #6b5f55; transition: color 0.2s; font-weight: 500; }
        .tweet-chars.over { color: #c74539; font-weight: 600; }
        .tweet-actions { display: flex; gap: 8px; flex-wrap: wrap; }
        .action-btn { padding: clamp(7px, 1.5vw, 8px) clamp(10px, 2vw, 14px); border-radius: 2px; font-family: 'JetBrains Mono', monospace; font-size: clamp(9px, 1.5vw, 10px); letter-spacing: 2px; text-transform: uppercase; cursor: pointer; border: 1px solid; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1); -webkit-appearance: none; touch-action: manipulation; flex: 1; min-width: 80px; font-weight: 600; }
        @media (min-width: 640px) { .action-btn { flex: 0 1 auto; min-width: auto; } }
        .action-btn:hover { transform: translateY(-2px); }
        .approve-btn { background: transparent; border-color: #5a9a5a; color: #5a9a5a; }
        .approve-btn:hover { background: rgba(90, 154, 90, 0.08); border-color: #4a8a4a; color: #3a7a3a; box-shadow: 0 2px 8px rgba(90, 154, 90, 0.15); }
        .approve-btn:active { transform: translateY(0); }
        .reject-btn { background: transparent; border-color: #c97560; color: #c97560; }
        .reject-btn:hover { background: rgba(201, 117, 96, 0.08); border-color: #b75540; color: #a73410; box-shadow: 0 2px 8px rgba(201, 117, 96, 0.15); }
        .reject-btn:active { transform: translateY(0); }
        .approved-card { background: linear-gradient(135deg, #fffbf7 0%, #fff8f1 100%); border-left: 4px solid #5a9a5a; border-right: 1px solid #d5ccc3; border-top: 1px solid #d5ccc3; border-bottom: 1px solid #d5ccc3; border-radius: 4px; padding: clamp(12px, 3vw, 18px); margin-bottom: 12px; animation: slideInCard 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s backwards; }
        .approved-card:hover { box-shadow: 0 4px 16px rgba(90, 154, 90, 0.15); border-left-color: #4a8a4a; }
        .approved-text { font-size: clamp(15px, 2vw, 16px); line-height: 1.6; font-weight: 400; color: #1a1410; font-style: normal; margin-bottom: 12px; white-space: pre-wrap; word-break: break-word; }
        .approved-bottom { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; padding-top: 10px; border-top: 1px solid #e8ddd5; }
        .copy-btn { background: transparent; border: 1px solid #d5ccc3; color: #5a9a5a; padding: clamp(5px, 1vw, 6px) clamp(8px, 2vw, 12px); font-family: 'JetBrains Mono', monospace; font-size: clamp(8px, 1.5vw, 9px); letter-spacing: 2px; text-transform: uppercase; cursor: pointer; border-radius: 2px; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1); -webkit-appearance: none; touch-action: manipulation; font-weight: 600; }
        .copy-btn:hover { border-color: #4a8a4a; color: #3a7a3a; background: rgba(90, 154, 90, 0.05); }
        .copy-btn:active { transform: scale(0.95); }
        .copy-btn.copied { border-color: #ff7f00; color: #ff7f00; background: rgba(255, 127, 0, 0.08); animation: copyPulse 0.4s ease; }
        @keyframes copyPulse { 0% { box-shadow: 0 0 0 0 rgba(255, 127, 0, 0.4); } 70% { box-shadow: 0 0 0 6px rgba(255, 127, 0, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 127, 0, 0); } }
        .empty-state { text-align: center; padding: 40px 16px; color: #6b5f55; font-style: italic; font-size: clamp(15px, 3vw, 17px); animation: fadeIn 0.4s ease; }
        .section-label { font-family: 'JetBrains Mono', monospace; font-size: clamp(8px, 1.5vw, 9px); letter-spacing: 4px; color: #6b5f55; text-transform: uppercase; margin-bottom: 16px; font-weight: 600; }
        .source-preview { font-family: 'JetBrains Mono', monospace; font-size: clamp(8px, 1.5vw, 9px); color: #8b7f75; margin-top: 10px; font-style: normal; border-top: 1px solid #e8ddd5; padding-top: 10px; overflow: hidden; text-overflow: ellipsis; word-break: break-word; white-space: normal; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @media (max-width: 480px) { .nav { flex-direction: column; } .nav-btn { padding: 12px 6px; border-bottom: 2px solid #ff7f00; border-radius: 0; } .nav-btn::before { height: 0; } .nav-btn.active::before { width: 0; } .nav-btn:last-child { border-bottom: none; } }
      `}</style>

      <div className="app">
        <div className="header">
          <div className="sigil">Luckify Me · Transmission Layer</div>
          <div className="title">Soltar Pipeline</div>
        </div>

        <div className="nav">
          <button className={`nav-btn ${view === "dump" ? "active" : ""}`} onClick={() => setView("dump")}>Dump</button>
          <button className={`nav-btn ${view === "twitter-reply" ? "active" : ""}`} onClick={() => setView("twitter-reply")}>X Reply</button>
          <button className={`nav-btn ${view === "reddit-reply" ? "active" : ""}`} onClick={() => setView("reddit-reply")}>Reddit</button>
          <button className={`nav-btn ${view === "queue" ? "active" : ""}`} onClick={() => setView("queue")}>
            Queue {queue.length > 0 && <span className="badge">{queue.length}</span>}
          </button>
          <button className={`nav-btn ${view === "approved" ? "active" : ""}`} onClick={() => setView("approved")}>
            Done {approved.length > 0 && <span className="badge">{approved.length}</span>}
          </button>
        </div>

        {view === "dump" && (
          <div>
            <div className="field-label">Mood</div>
            <div className="mood-row">
              {MOODS.map(m => (
                <button key={m.id} className={`mood-btn ${mood?.id === m.id ? "selected" : ""}`} onClick={() => setMood(mood?.id === m.id ? null : m)}>
                  {m.emoji} {m.label}
                </button>
              ))}
            </div>
            <div className="field-label">Raw Channel Input</div>
            <textarea
              className="textarea textarea-lg"
              value={dumpText}
              onChange={e => setDumpText(e.target.value)}
              placeholder="Drop it raw. Present moment. Gambling story, fatherhood hit, Soltar transmission, half idea — whatever is moving through right now..."
              onKeyDown={e => { if (e.metaKey && e.key === "Enter") handleDump(); }}
            />
            {error && <div className="error-msg">{error}</div>}
            <div className="dump-footer">
              <span className="char-count">{dumpText.length} chars</span>
              <button className="transmit-btn" onClick={handleDump} disabled={loading || !dumpText.trim()}>
                {loading ? "Transmitting..." : "Transmit →"}
              </button>
            </div>
          </div>
        )}

        {view === "twitter-reply" && (
          <div>
            <div className="field-label">Their Tweet</div>
            <textarea
              className="textarea textarea-sm"
              value={originalTweet}
              onChange={e => setOriginalTweet(e.target.value)}
              placeholder="Paste the tweet you are replying to..."
            />
            <div className="field-label">Your Channel</div>
            <textarea
              className="textarea textarea-md"
              value={channelReaction}
              onChange={e => setChannelReaction(e.target.value)}
              placeholder="What does Soltar say about this? Drop your raw reaction, the vibe, the angle you want to hit..."
            />
            {error && <div className="error-msg">{error}</div>}
            <div className="dump-footer">
              <span className="char-count">reply under 280 chars</span>
              <button className="transmit-btn" onClick={handleTwitterReply} disabled={loading || !originalTweet.trim() || !channelReaction.trim()}>
                {loading ? "Transmitting..." : "Transmit →"}
              </button>
            </div>
          </div>
        )}

        {view === "reddit-reply" && (
          <div>
            <div className="field-label">Their Post or Comment</div>
            <textarea
              className="textarea textarea-md"
              value={originalReddit}
              onChange={e => setOriginalReddit(e.target.value)}
              placeholder="Paste the Reddit post or comment you are replying to..."
            />
            <div className="field-label">Your Channel</div>
            <textarea
              className="textarea textarea-md"
              value={redditReaction}
              onChange={e => setRedditReaction(e.target.value)}
              placeholder="What do you actually want to say? Your perspective, your story, your angle — raw and unfiltered..."
            />
            {error && <div className="error-msg">{error}</div>}
            <div className="dump-footer">
              <span className="char-count">long form, personal</span>
              <button className="transmit-btn" onClick={handleRedditReply} disabled={loading || !originalReddit.trim() || !redditReaction.trim()}>
                {loading ? "Transmitting..." : "Transmit →"}
              </button>
            </div>
          </div>
        )}

        {view === "queue" && (
          <div>
            {loading && (
              <div className="loading-state">
                Soltar is distilling<span className="dot">.</span><span className="dot">.</span><span className="dot">.</span>
              </div>
            )}
            {!loading && queue.length === 0 && <div className="empty-state">◇ Silence. Waiting for transmission. ◇</div>}
            {!loading && queue.map((item, idx) => {
              const len = item.tweet.length;
              const isReddit = item.type === "reddit-reply";
              let accentColor = "#ff7f00";
              if (item.type === "twitter-reply") accentColor = "#4a6a8a";
              if (item.type === "reddit-reply") accentColor = "#8a4a2a";
              if (item.mood) accentColor = item.mood.color;
              return (
                <div key={item.id} className="tweet-card" style={{ borderLeftColor: accentColor, animationDelay: `${idx * 0.05}s` }}>
                  <div className="tweet-meta">
                    <span>{new Date(item.timestamp).toLocaleDateString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}</span>
                    <span className="type-tag" style={{ color: accentColor, borderColor: accentColor }}>{typeLabel(item.type)}</span>
                    {item.mood && <span style={{ color: item.mood.color }}>{item.mood.emoji} {item.mood.label}</span>}
                  </div>
                  <textarea
                    className="tweet-textarea"
                    value={item.tweet}
                    onChange={e => handleEdit(item.id, e.target.value)}
                    rows={isReddit ? 10 : 4}
                  />
                  <div className="tweet-bottom">
                    <span className={`tweet-chars ${!isReddit && len > 280 ? "over" : ""}`}>
                      {isReddit ? `${len} chars` : `${len}/280`}
                    </span>
                    <div className="tweet-actions">
                      <button className="action-btn approve-btn" onClick={() => handleApprove(item.id)}>✓ Approve</button>
                      <button className="action-btn reject-btn" onClick={() => handleReject(item.id)}>✕ Reject</button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {view === "approved" && (
          <div>
            {approved.length === 0 && <div className="empty-state">✦ Nothing ready to transmit. ✦</div>}
            {approved.length > 0 && <div className="section-label">✓ Ready to transmit</div>}
            {approved.map((item, idx) => {
              let accentColor = "#4a8a4a";
              if (item.mood) accentColor = item.mood.color;
              return (
                <div key={item.id} className="approved-card" style={{ borderLeftColor: accentColor, animationDelay: `${idx * 0.05}s` }}>
                  <div className="tweet-meta" style={{ marginBottom: "10px" }}>
                    <span className="type-tag" style={{ color: accentColor, borderColor: accentColor }}>{typeLabel(item.type)}</span>
                    {item.mood && <span style={{ color: item.mood.color, fontFamily: "JetBrains Mono, monospace", fontSize: "9px" }}>{item.mood.emoji} {item.mood.label}</span>}
                  </div>
                  <div className="approved-text">{item.tweet}</div>
                  <div className="approved-bottom">
                    <span style={{ fontFamily: "JetBrains Mono, monospace", fontSize: "9px", color: "#6b5f55", letterSpacing: "2px", textTransform: "uppercase", fontWeight: "500" }}>
                      {item.tweet.length} chars
                    </span>
                    <button
                      className={`copy-btn ${copiedId === item.id ? "copied" : ""}`}
                      onClick={() => copyToClipboard(item.tweet, item.id)}
                    >
                      {copiedId === item.id ? "Copied ✓" : "Copy"}
                    </button>
                  </div>
                  {item.source && <div className="source-preview">{item.source}</div>}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
