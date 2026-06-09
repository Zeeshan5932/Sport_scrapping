export interface ScorecardEntry {
  id?: string;
  name: string;
  runs: number;
  balls: number;
  fours: number;
  sixes: number;
  strike_rate?: number;
  strikeRate?: number;
}

export interface MatchStats {
  label: string;
  value: string;
}

export interface HeadToHead {
  team1_wins: number;
  team2_wins: number;
}

export interface Match {
  id: string;
  team1: string;
  team2: string;
  score1: string;
  score2: string;
  status: string;
  tournament?: string;
  live?: boolean;
  scorecard?: ScorecardEntry[];
  stats?: MatchStats[];
  head_to_head?: HeadToHead;
}

export interface MatchDetailResponse {
  id: string;
  team1: string;
  team2: string;
  score1: string;
  score2: string;
  status: string;
  tournament?: string;
  scorecard?: ScorecardEntry[];
  stats?: MatchStats[];
  head_to_head?: HeadToHead;
}
