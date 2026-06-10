"use client";

import { useEffect, useMemo, useState } from "react";

import TournamentSection from "../components/TournamentSection";
import DateNavigator from "../components/DateNavigator";

import { getMatches } from "../services/api";

import type { Match } from "../types/match";

export default function HomePage() {

  const [matches, setMatches] = useState<Match[]>([]);

  const [loading, setLoading] = useState(false);

  const [selectedDate, setSelectedDate] =
    useState(() => {

      const today = new Date();

      return today
        .toISOString()
        .split("T")[0];

    });

  const fetchMatches = async (
    date: string
  ) => {

    setLoading(true);

    try {

      const response =
        await getMatches(date);

      console.log(
        "API RESPONSE:",
        response
      );

      /*
      YOUR API STRUCTURE:

      {
        tournaments: [
          {
            tournament_name: "",
            matches: []
          }
        ]
      }
      */

      const tournaments =
        response?.tournaments || [];

      const allMatches =
        tournaments.flatMap(
          (tournament: any) => {

            return (
              tournament.matches || []
            );

          }
        );

      setMatches(allMatches);

    } catch (error) {

      console.error(
        "Error fetching matches:",
        error
      );

      setMatches([]);

    } finally {

      setLoading(false);

    }

  };

  useEffect(() => {

    fetchMatches(selectedDate);

  }, [selectedDate]);

  /*
  GROUP MATCHES
  */

  const groupedMatches =
    useMemo(() => {

      return matches.reduce(

        (
          acc,
          match: any
        ) => {

          const tournamentName =
            match.tournament ||
            "Unknown";

          if (
            !acc[tournamentName]
          ) {

            acc[tournamentName] = [];

          }

          acc[tournamentName]
            .push(match);

          return acc;

        },

        {} as Record<
          string,
          Match[]
        >

      );

    }, [matches]);

  const handleDateChange = (
    newDate: string
  ) => {

    setSelectedDate(newDate);

  };

  return (

    <main className="
      min-h-screen
      bg-[#02033B]
      relative
      overflow-hidden
    ">

      {/* TOP WHITE HEADER */}

      <div className="
        bg-white
        text-black
        text-[14px]
        px-2
        py-1
        border-b
      ">
        CRICKET LIVE MATCH TRACKER
      </div>

      {/* DATE NAVIGATOR */}

      <DateNavigator
        selectedDate={selectedDate}
        onDateChange={
          handleDateChange
        }
      />

      {/* CENTER MATCH TRACKER */}

      <div className="
        flex
        justify-center
        pt-2
        pb-10
      ">

        <div className="
          w-[260px]
          sm:w-[280px]
        ">

          {loading ? (

            <div className="
              bg-white
              text-center
              text-[11px]
              py-4
              border
            ">
              Processing...
            </div>

          ) : matches.length > 0 ? (

            Object.entries(
              groupedMatches
            ).map(

              ([
                tournament,
                tournamentMatches
              ]) => (

                <TournamentSection
                  key={tournament}
                  tournament={
                    tournament
                  }
                  matches={
                    tournamentMatches
                  }
                />

              )

            )

          ) : (

            <div className="
              bg-white
              text-center
              text-[11px]
              py-4
              border
            ">
              No matches available
            </div>

          )}

        </div>

      </div>

    </main>

  );

}