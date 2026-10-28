const express = require('express');
const path = require('path');
const cors = require('cors');
const profile = require('./data/profile.json');

const app = express();
const PORT = process.env.PORT || 3000;
const TTS_URL = 'https://tts.nhohoai.vn/tts';
const ALLOWED_VOICES = new Set([
  'en-US-AriaNeural',
  'en-US-GuyNeural',
  'en-US-JennyNeural',
  'en-GB-SoniaNeural',
  'en-GB-RyanNeural',
  'en-AU-NatashaNeural',
]);
const ALLOWED_RATES = new Set(['-25%', '-10%', '+0%', '+25%', '+50%']);

app.disable('x-powered-by');
app.use(cors());
app.use(express.json({ limit: '64kb' }));
app.use(express.urlencoded({ extended: false, limit: '64kb' }));
app.use(express.static(path.join(__dirname, 'public'), { maxAge: '1h' }));

app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

app.get('/api/profile', (_req, res) => {
  res.json(profile);
});

/**
 * Proxy Tempo/Nhớ Hoài Azure Neural TTS (Aria/Guy/…) with word timeline.
 * Returns JSON: { audio: base64 mp3, words: [{t,d,w}], mime }.
 */
app.post('/api/tts', async (req, res) => {
  try {
    const text = String(req.body?.text || '').trim();
    const voice = String(req.body?.voice || 'en-US-AriaNeural');
    const voiceB = String(req.body?.voice_b || req.body?.voiceB || '').trim();
    const rate = String(req.body?.rate || '+0%');

    if (!text) return res.status(400).json({ ok: false, error: 'text is required' });
    if (text.length > 5000) return res.status(400).json({ ok: false, error: 'text too long (max 5000)' });
    if (!ALLOWED_VOICES.has(voice)) return res.status(400).json({ ok: false, error: 'invalid voice' });
    if (voiceB && !ALLOWED_VOICES.has(voiceB)) {
      return res.status(400).json({ ok: false, error: 'invalid voice_b' });
    }
    if (!ALLOWED_RATES.has(rate)) return res.status(400).json({ ok: false, error: 'invalid rate' });

    const params = new URLSearchParams({ text, voice, rate, timeline: '1' });
    if (voiceB) params.set('voice_b', voiceB);

    const upstream = await fetch(TTS_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        Origin: 'https://tempo.nhohoai.vn',
        Referer: 'https://tempo.nhohoai.vn/',
        'User-Agent': 'hieu-portfolio-tts-proxy/1.0',
      },
      body: params.toString(),
    });

    if (!upstream.ok) {
      let detail = `TTS upstream ${upstream.status}`;
      try {
        const err = await upstream.json();
        if (err?.detail) detail = String(err.detail);
      } catch (_) {}
      return res.status(502).json({ ok: false, error: detail });
    }

    const buf = Buffer.from(await upstream.arrayBuffer());
    const audioChunks = [];
    const words = [];
    let offset = 0;
    while (offset + 5 <= buf.length) {
      const type = buf[offset];
      const len = buf.readUInt32BE(offset + 1);
      offset += 5;
      if (offset + len > buf.length) break;
      const payload = buf.subarray(offset, offset + len);
      offset += len;
      if (type === 0) audioChunks.push(payload);
      else if (type === 1) {
        try {
          words.push(JSON.parse(payload.toString('utf8')));
        } catch (_) {}
      }
    }

    const audio = Buffer.concat(audioChunks);
    if (!audio.length) {
      return res.status(502).json({ ok: false, error: 'empty audio from TTS' });
    }

    res.json({
      ok: true,
      mime: 'audio/mpeg',
      audio: audio.toString('base64'),
      words,
      duration: words.length
        ? words[words.length - 1].t + (words[words.length - 1].d || 0)
        : null,
    });
  } catch (err) {
    console.error('[tts]', err?.message || err);
    res.status(502).json({ ok: false, error: 'TTS proxy failed' });
  }
});

app.post('/api/contact', (req, res) => {
  const name = String(req.body?.name || '').trim();
  const email = String(req.body?.email || '').trim();
  const message = String(req.body?.message || '').trim();

  if (!name || !email || !message) {
    return res.status(400).json({ ok: false, error: 'name, email, and message are required' });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ ok: false, error: 'invalid email' });
  }

  console.log('[contact]', new Date().toISOString(), {
    name,
    email,
    message: message.slice(0, 800),
  });

  res.json({ ok: true });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Portfolio listening on http://0.0.0.0:${PORT}`);
});
