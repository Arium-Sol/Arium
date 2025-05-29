// gameScoring.ts

export type GameScoreInput = {
  team: number;         // 0–10
  tokenomics: number;   // 0–10
  codeQuality: number;  // 0–10
  community: number;    // 0–10
  documentation: number;// 0–10
};

export function calculateScore(input: GameScoreInput): number {
  const weights = {
    team: 0.25,
    tokenomics: 0.25,
    codeQuality: 0.2,
    community: 0.2,
    documentation: 0.1,
  };

  const score =
    input.team * weights.team +
    input.tokenomics * weights.tokenomics +
    input.codeQuality * weights.codeQuality +
    input.community * weights.community +
    input.documentation * weights.documentation;

  return Math.round(score * 10) / 10; // return with 1 decimal
}
