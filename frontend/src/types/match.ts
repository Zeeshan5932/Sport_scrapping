export interface ScorecardEntry {
  id: string;
  name: string;
  runs: number;
  balls: number;
  fours: number;
  sixes: number;
  strikeRate: number;
}

export interface Statistics {
  teamA: {
    runs: number;
    wickets: number;
    overs: string;
  };
  teamB: {
    runs: number;
    wickets: number;
    overs: string;
  };
  partnerships?: Array<{ players: string; runs: number }>;
}

export interface HeadToHeadItem {
  date: string;
  tournament: string;
  winner: string;
  margin: string;
}

export interface BallEvent {
  over: number;
  ball: number;
  run: number;
  summary: string;
}

export interface RunRatePoint {
  over: number;
  runRate: number;
}

export interface Match {
  id: string;
  tournament: string;
  teamA: string;
  teamB: string;
  scoreA?: string;
  scoreB?: string;
  overs?: string;
  status: string;
  live: boolean;
  scorecard?: ScorecardEntry[];
  statistics?: Statistics;
  headToHead?: HeadToHeadItem[];
  balls?: BallEvent[];
  runRate?: RunRatePoint[];
}
