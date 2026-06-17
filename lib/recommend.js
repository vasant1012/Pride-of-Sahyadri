// Simple similarity-based recommendation engine for forts.

import { FORTS } from './forts';

function elevationSimilarity(a, b) {
  const diff = Math.abs(a - b);
  // 0m diff -> 1.0, 1500m diff -> ~0
  return Math.max(0, 1 - diff / 1500);
}

export function recommendFor(fortId, topN = 4) {
  const selected = FORTS.find(f => f.id === fortId);
  if (!selected) return [];

  const scored = FORTS.filter(f => f.id !== fortId).map(other => {
    let score = 0;
    const reasons = [];

    if (other.district === selected.district) {
      score += 0.25;
      reasons.push(`Same district (${selected.district})`);
    }
    if (other.type === selected.type) {
      score += 0.25;
      reasons.push(`Same fort type (${selected.type})`);
    }
    if (other.difficulty === selected.difficulty) {
      score += 0.20;
      reasons.push(`Same trek difficulty (${selected.difficulty})`);
    }
    const elev = elevationSimilarity(other.elevation, selected.elevation);
    score += elev * 0.20;
    if (elev > 0.85) reasons.push('Similar elevation');

    const aSeasons = new Set(selected.season.split(',').map(s => s.trim()));
    const bSeasons = new Set(other.season.split(',').map(s => s.trim()));
    const overlap = [...aSeasons].filter(x => bSeasons.has(x)).length;
    if (overlap > 0) {
      score += 0.10 * Math.min(1, overlap / aSeasons.size);
      reasons.push('Overlapping best season');
    }

    return {
      fort: other,
      score: Math.round(score * 100),
      reasons,
    };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, topN);
}
