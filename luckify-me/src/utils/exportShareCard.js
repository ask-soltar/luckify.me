import { toPng } from 'html-to-image';

const EXPORT_OPTIONS = {
  width: 1080,
  height: 1350,
  // pixelRatio: 1 → output PNG is exactly 1080×1350 px.
  // The card is already designed at that size so 1x is full quality.
  pixelRatio: 1,
  style: {
    // Override the preview-scale transform so html-to-image renders
    // the card at its natural 1080×1350 size regardless of display scale.
    transform: 'scale(1)',
    transformOrigin: 'top left',
  },
};

function resolveNode(elementId) {
  const node = document.getElementById(elementId);
  if (!node) throw new Error(`Share card element #${elementId} not found`);
  return node;
}

function triggerDownload(dataUrl, filename = 'main-quest.png') {
  const a = document.createElement('a');
  a.href = dataUrl;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

export async function downloadMainQuestShareCard(elementId = 'mq-share-card') {
  const dataUrl = await toPng(resolveNode(elementId), EXPORT_OPTIONS);
  triggerDownload(dataUrl);
}

export async function exportMainQuestShareCard(elementId = 'mq-share-card') {
  const dataUrl = await toPng(resolveNode(elementId), EXPORT_OPTIONS);

  const blob = await fetch(dataUrl).then(r => r.blob());
  const file = new File([blob], 'main-quest.png', { type: 'image/png' });

  if (
    typeof navigator !== 'undefined' &&
    navigator.share &&
    navigator.canShare &&
    navigator.canShare({ files: [file] })
  ) {
    await navigator.share({
      files: [file],
      title: 'My Main Quest',
      text: 'Find your Main Quest at Luckify.me',
    });
    return;
  }

  // Fallback: download when Web Share API is unavailable
  triggerDownload(dataUrl);
}
