import { QuestShell } from './quest/index.js';
import { buildMainQuestPanel } from '../content/mainQuest.ts';
import '../styles/quest-system.css';

export function MainQuestScreen({ entry }) {
  return <QuestShell key={entry.id} panel={buildMainQuestPanel(entry)} />;
}
