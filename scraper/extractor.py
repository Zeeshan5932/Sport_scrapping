from config import SELECTORS

class Extractor:
    def __init__(self, page):
        self.page = page

    async def get_match_data(self):
        return await self.page.evaluate("""
        () => {
            const teams = Array.from(document.querySelectorAll('.sr-simcrick-scb__team-name'))
                .map(e => e.innerText);

            const scores = Array.from(document.querySelectorAll('.sr-simcrick-scb__result'))
                .map(e => e.innerText);

            const status = document.querySelector('.sr-simcrick-scb__status')?.innerText || null;
            const comment = document.querySelector('.sr-simcrick-scb__comment')?.innerText || null;

            return {
                teamA: teams[0] || null,
                teamB: teams[1] || null,
                scoreA: scores[0] || null,
                scoreB: scores[1] || null,
                status,
                comment
            };
        }
        """)