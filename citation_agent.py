# File: citation_agent.py
import datetime

class CitationAgent:
    def __init__(self):
        print("📝 System: Initializing Citation Agent...")

    def generate_citations(self, papers):
        """
        Takes a list of papers and returns a formatted IEEE bibliography string.
        """
        print(" -> Citation Agent: Formatting references (IEEE Style)...")
        bibliography = []

        for index, paper in enumerate(papers):
            # 1. Process Authors (Get the first author + 'et al.' if many)
            authors = paper['authors']
            if len(authors) > 1:
                author_str = f"{authors[0]} et al."
            elif len(authors) == 1:
                author_str = authors[0]
            else:
                author_str = "Unknown Author"

            # 2. Format Date (Extract just the year)
            # format: [1] Author, "Title," Source, Year.
            year = paper['date'].split('-')[0]
            
            citation = f"[{index + 1}] {author_str}, \"{paper['title']},\" ArXiv Preprint, {year}. Available: {paper['url']}"
            bibliography.append(citation)

        return "\n".join(bibliography)