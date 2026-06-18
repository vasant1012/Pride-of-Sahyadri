// Thin helper to call the Emergent Universal LLM Key via the OpenAI-compatible endpoint.
// Endpoint: https://integrations.emergentagent.com/v1/chat/completions

const BASE_URL = process.env.EMERGENT_BASE_URL || 'https://integrations.emergentagent.com/v1';
const API_KEY = process.env.EMERGENT_LLM_KEY;
const MODEL = process.env.EMERGENT_MODEL || 'gpt-5';

export async function chatComplete(messages, { stream = false } = {}) {
  if (!API_KEY) {
    throw new Error('EMERGENT_LLM_KEY is not configured');
  }

  const response = await fetch(`${BASE_URL}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      model: MODEL,
      messages,
      stream,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => '');
    throw new Error(`Emergent LLM request failed (${response.status}): ${errorText}`);
  }

  if (stream) {
    return response; // caller will read the SSE stream
  }

  const data = await response.json();
  const content = data?.choices?.[0]?.message?.content ?? '';
  return content;
}
