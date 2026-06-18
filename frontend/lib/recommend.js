// Recommendation engine integrated with FastAPI backend.

import { getSimilarForts } from './backend';

/**
 * Fetch similar forts for the given fort ID from the backend.
 * @param {string|number} fortId - Fort ID to find similar forts for
 * @param {number} topN - Number of recommendations to return (default 4)
 * @returns {Promise<Array>} Array of recommendation objects with fort, score, and reasons
 */
export async function recommendFor(fortId, topN = 4) {
  try {
    const forts = await getSimilarForts(fortId, topN);
    
    return forts.map((fort, index) => ({
      fort,
      // Scoring: top result = 100%, descending
      score: Math.max(60, 100 - (index * 10)),
      reasons: [
        `Elevation: ${fort.elevation}m`,
        `Type: ${fort.type}`,
        `Difficulty: ${fort.difficulty}`,
        `Best season: ${fort.season}`,
      ].filter(Boolean),
    }));
  } catch (error) {
    console.error('Recommendation fetch failed:', error);
    return [];
  }
}
