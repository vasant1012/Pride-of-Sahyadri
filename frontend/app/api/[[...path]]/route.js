import { NextResponse } from 'next/server';
import { MongoClient } from 'mongodb';
import { v4 as uuidv4 } from 'uuid';
import { FORTS, getFortById, listDistricts, listTypes, listDifficulties, listSeasons } from '@/lib/forts';
import { recommendFor } from '@/lib/recommend';
import { chatComplete } from '@/lib/emergent';

export const dynamic = 'force-dynamic';

// --- MongoDB singleton ---
let _client = null;
async function getDb() {
  if (!_client) {
    _client = new MongoClient(process.env.MONGO_URL);
    await _client.connect();
  }
  return _client.db(process.env.DB_NAME || 'sahyadri');
}

function json(data, init) {
  return NextResponse.json(data, init);
}

function segmentsOf(params) {
  const path = params?.path || [];
  return Array.isArray(path) ? path : [path];
}

// --- GET handler ---
export async function GET(req, { params }) {
  try {
    const segs = segmentsOf(await params);
    const url = new URL(req.url);

    if (segs.length === 0 || segs[0] === '') {
      return json({ ok: true, message: 'Pride of Sahyadri API' });
    }

    if (segs[0] === 'forts' && segs.length === 1) {
      const district = url.searchParams.get('district');
      const type = url.searchParams.get('type');
      const difficulty = url.searchParams.get('difficulty');
      const season = url.searchParams.get('season');
      const water = url.searchParams.get('water');
      const search = url.searchParams.get('q');
      const minElev = url.searchParams.get('minElev');
      const maxElev = url.searchParams.get('maxElev');

      let results = FORTS.slice();
      if (district && district !== 'all') results = results.filter(f => f.district === district);
      if (type && type !== 'all') results = results.filter(f => f.type === type);
      if (difficulty && difficulty !== 'all') results = results.filter(f => f.difficulty === difficulty);
      if (season && season !== 'all') results = results.filter(f => f.season.toLowerCase().includes(season.toLowerCase()));
      if (water && water !== 'all') results = results.filter(f => f.water === water);
      if (minElev) results = results.filter(f => f.elevation >= parseInt(minElev, 10));
      if (maxElev) results = results.filter(f => f.elevation <= parseInt(maxElev, 10));
      if (search) {
        const q = search.toLowerCase();
        results = results.filter(f =>
          f.name.toLowerCase().includes(q) ||
          f.district.toLowerCase().includes(q) ||
          f.summary.toLowerCase().includes(q) ||
          f.history.toLowerCase().includes(q),
        );
      }
      return json({ count: results.length, forts: results });
    }

    if (segs[0] === 'forts' && segs[1]) {
      const fort = getFortById(segs[1]);
      if (!fort) return json({ error: 'Fort not found' }, { status: 404 });
      return json({ fort });
    }

    if (segs[0] === 'meta') {
      return json({
        districts: listDistricts(),
        types: listTypes(),
        difficulties: listDifficulties(),
        seasons: listSeasons(),
        waterOptions: ['Year-round', 'Seasonal', 'Sea around', 'None'],
        totalForts: FORTS.length,
      });
    }

    if (segs[0] === 'stats') {
      const byType = {};
      const byDifficulty = {};
      const byDistrict = {};
      const elevations = [];
      FORTS.forEach(f => {
        byType[f.type] = (byType[f.type] || 0) + 1;
        byDifficulty[f.difficulty] = (byDifficulty[f.difficulty] || 0) + 1;
        byDistrict[f.district] = (byDistrict[f.district] || 0) + 1;
        elevations.push({ name: f.name, elevation: f.elevation });
      });
      const districtCovered = Object.keys(byDistrict).length;
      return json({
        totals: {
          totalForts: FORTS.length,
          districtsCovered: districtCovered,
          trekRoutes: FORTS.filter(f => f.elevation > 0).length,
          heritageSites: FORTS.length, // all forts treated as heritage sites
        },
        byType: Object.entries(byType).map(([name, value]) => ({ name, value })),
        byDifficulty: Object.entries(byDifficulty).map(([name, value]) => ({ name, value })),
        byDistrict: Object.entries(byDistrict).map(([name, value]) => ({ name, value })).sort((a,b) => b.value - a.value),
        elevations: elevations.sort((a, b) => b.elevation - a.elevation).slice(0, 12),
      });
    }

    if (segs[0] === 'chat-history' && segs[1]) {
      const db = await getDb();
      const session = await db.collection('chat_sessions').findOne({ session_id: segs[1] });
      return json({ messages: session?.messages || [] });
    }

    return json({ error: 'Not found' }, { status: 404 });
  } catch (err) {
    console.error('GET error', err);
    return json({ error: err.message }, { status: 500 });
  }
}

// --- POST handler ---
export async function POST(req, { params }) {
  try {
    const segs = segmentsOf(await params);
    const body = await req.json().catch(() => ({}));

    if (segs[0] === 'recommend') {
      const { fortId, topN } = body;
      const recs = recommendFor(fortId, topN || 4);
      return json({ selected: getFortById(fortId), recommendations: recs });
    }

    if (segs[0] === 'chat') {
      const { message, session_id } = body;
      if (!message) return json({ error: 'message is required' }, { status: 400 });
      const sid = session_id || uuidv4();

      const db = await getDb();
      const col = db.collection('chat_sessions');
      const existing = await col.findOne({ session_id: sid });
      const history = existing?.messages || [];

      // Build context: include ALL forts data as condensed RAG context
      const context = FORTS.map(f => (
        `# ${f.name} (id: ${f.id})\n` +
        `District: ${f.district} | Type: ${f.type} | Difficulty: ${f.difficulty} | ` +
        `Elevation: ${f.elevation}m | Best Season: ${f.season} | Water: ${f.water} | Stay: ${f.accommodation}\n` +
        `Coordinates: ${f.coordinates.lat}, ${f.coordinates.lng}\n` +
        `Summary: ${f.summary}\n` +
        `History: ${f.history}\n` +
        `Architecture: ${f.architecture}\n` +
        `Strategic Importance: ${f.strategic}\n` +
        `Visitor Notes: ${f.notes}`
      )).join('\n\n');

      const systemPrompt = (
        'You are "Pride of Sahyadri", a knowledgeable and enthusiastic guide ' +
        'about the historical hill and sea forts of Maharashtra, India. ' +
        'Always answer in well-structured GitHub-flavored Markdown with clear ' +
        'headings (##), short paragraphs, and bullet lists when helpful. ' +
        'You may use a friendly Marathi greeting like "\u091c\u0935\u093e\u0928 \u092e\u0939\u093e\u0930\u093e\u0937\u094d\u091f\u094d\u0930!" only when relevant. ' +
        'Cite the names of forts you reference with **bold** formatting. ' +
        'Prefer the facts in the provided KNOWLEDGE BASE; if the user asks ' +
        'about something outside it, share general historically-accepted ' +
        'information but explicitly note that it is not from the curated dataset. ' +
        'Keep answers vivid but concise (about 150-300 words unless asked for detail).'
      );

      const userPrompt = (
        '## KNOWLEDGE BASE (Maharashtra Forts)\n' +
        context +
        '\n\n## USER QUESTION\n' +
        message
      );

      const messagesForLLM = [
        { role: 'system', content: systemPrompt },
        ...history.slice(-6).map(m => ({ role: m.role, content: m.content })),
        { role: 'user', content: userPrompt },
      ];

      const answer = await chatComplete(messagesForLLM, { stream: false });

      const updatedMessages = [
        ...history,
        { role: 'user', content: message, ts: new Date().toISOString() },
        { role: 'assistant', content: answer, ts: new Date().toISOString() },
      ];

      await col.updateOne(
        { session_id: sid },
        { $set: { session_id: sid, messages: updatedMessages, updatedAt: new Date() } },
        { upsert: true },
      );

      return json({ session_id: sid, answer });
    }

    return json({ error: 'Not found' }, { status: 404 });
  } catch (err) {
    console.error('POST error', err);
    return json({ error: err.message }, { status: 500 });
  }
}
