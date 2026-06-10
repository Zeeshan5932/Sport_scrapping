import axios from "axios";
import type { Match, MatchDetailResponse } from "../types/match";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export const API = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export async function getMatches(date?: string): Promise<Match[]> {
  try {
    const dateParam = date || new Date().toISOString().split("T")[0];
    const response = await API.get<Match[]>(`/matches?date=${dateParam}`);
    if (response?.data && Array.isArray(response.data)) {
      return response.data;
    }
  } catch (error) {
    console.error("Error fetching matches:", error);
  }
  return [];
}

export async function getMatchById(id: string, date?: string): Promise<MatchDetailResponse | null> {
  try {
    const dateParam = date || new Date().toISOString().split("T")[0];
    const response = await API.get<MatchDetailResponse>(`/match/${id}?date=${dateParam}`);
    if (response?.data) {
      return response.data;
    }
  } catch (error) {
    console.error("Error fetching match details:", error);
  }
  return null;
}
