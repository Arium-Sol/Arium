import { calculateScore } from "../src/lib/gameScoring";

const sample = {
  team: 8,
  tokenomics: 7,
  codeQuality: 9,
  community: 6,
  documentation: 8,
};

console.log("Test score result:", calculateScore(sample)); // Expect around 7.5
