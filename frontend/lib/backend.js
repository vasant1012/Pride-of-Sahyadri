const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8030';
const DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1526772662000-3f88f10405ff?auto=format&fit=crop&w=1200&q=80';

function buildUrl(path, params = {}) {
  const url = new URL(path, BACKEND_URL);
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null) return;
    url.searchParams.set(key, String(value));
  });
  return url.toString();
}

function normalizeFortType(value) {
  if (!value) return 'Unknown';
  const lower = value.toLowerCase();
  if (lower.includes('sea')) return 'Sea Fort';
  if (lower.includes('hill') || lower.includes('giri') || lower.includes('durg') || lower.includes('plateau')) return 'Hill Fort';
  if (lower.includes('land')) return 'Land Fort';
  return value;
}

function transformFort(raw) {
  return {
    id: String(raw.fort_id ?? raw.id ?? ''),
    name: raw.name ?? 'Unknown Fort',
    district: raw.district ?? 'Unknown',
    type: normalizeFortType(raw.type ?? raw.fort_type ?? ''),
    difficulty: raw.trek_difficulty ?? raw.difficulty ?? 'Unknown',
    elevation: raw.elevation_m ?? raw.elevation ?? 0,
    season: raw.best_season ?? raw.season ?? '',
    water: raw.water_availability ?? raw.water ?? 'Unknown',
    accommodation: raw.accommodation ?? 'Information Not Available',
    summary: raw.notes || raw.current_condition || raw.key_events || raw.summary || 'A historic Maharashtra fort with rich heritage.',
    notes: raw.notes ?? '',
    history: raw.history ?? raw.key_events ?? '',
    image: raw.image || DEFAULT_IMAGE,
    coordinates: {
      lat: raw.latitude ?? raw.coordinates?.lat ?? 0,
      lng: raw.longitude ?? raw.coordinates?.lng ?? 0,
    },
    raw,
  };
}

async function fetchJson(url, init) {
  const res = await fetch(url, init);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Backend request failed: ${res.status} ${text}`);
  }
  return res.json();
}

export async function getMeta() {
  const data = await fetchJson(buildUrl('/meta'));
  return data;
}

export async function getStats() {
  const data = await fetchJson(buildUrl('/stats'));
  return data;
}

export async function getForts(params = {}) {
  const url = buildUrl('/forts', params);
  const data = await fetchJson(url);
  return Array.isArray(data) ? data.map(transformFort) : [];
}

export async function getSimilarForts(fortId, topN = 6) {
  const url = buildUrl(`/recommend/similar/${fortId}`, { k: topN });
  const data = await fetchJson(url);
  return Array.isArray(data) ? data.map(transformFort) : [];
}

export async function querySemanticSearch(query, topK = 3) {
  /**
   * Query the RAG-powered semantic search endpoint.
   * Uses the backend's RAG engine to retrieve relevant fort context
   * and generate an AI-powered answer.
   *
   * @param {string} query - User's natural language question
   * @param {number} topK - Number of top results to retrieve (default 3)
   * @returns {Promise<string>} - Generated answer from the RAG pipeline
   */
  const url = buildUrl('/search/semantic_search', { q: query, top_k: topK });
  const data = await fetchJson(url);

  // Handle error responses from RAG engine
  if (data?.error) {
    throw new Error(`Semantic search error: ${data.error}`);
  }

  // Handle direct string response from LLM
  if (typeof data === 'string') {
    return data;
  }

  // Handle object response with answer field
  if (data?.answer) {
    return data.answer;
  }

  // Fallback: convert to string
  return String(data);
}
