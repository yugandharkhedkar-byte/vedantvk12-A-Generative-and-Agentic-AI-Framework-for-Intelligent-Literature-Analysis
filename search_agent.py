# File: search_agent.py
import arxiv

class SearchAgent:
    def __init__(self):
        print("🔍 System: Initializing Search Agent...")
        self.client = arxiv.Client()

    def search_papers(self, topic, max_results=8):
        """
        Searches ArXiv for papers related to the topic.
        Returns a list of simplified paper dictionaries.
        """
        print(f" -> Search Agent: Searching ArXiv for '{topic}'...")
        
        # 1. Construct the search query
        # sort_by=arxiv.SortCriterion.Relevance ensures we get the best matches
        search = arxiv.Search(
            query = topic,
            max_results = max_results,
            sort_by = arxiv.SortCriterion.Relevance
        )

        # 2. Fetch and clean the results
        paper_list = []
        
        # We use a loop to process the results from the generator
        for result in self.client.results(search):
            paper_info = {
                "title": result.title,
                "date": result.published.strftime("%Y-%m-%d"), # Format date nicely
                "authors": [author.name for author in result.authors],
                "summary": result.summary.replace("\n", " "), # Remove messy newlines
                "url": result.pdf_url
            }
            paper_list.append(paper_info)
            
        print(f" -> Search Agent: Found {len(paper_list)} papers.")
        return paper_list

# Simple test block to run this file alone
if __name__ == "__main__":
    agent = SearchAgent()
    topic = input("Enter a topic to search (e.g., 'Generative AI'): ")
    results = agent.search_papers(topic)
    
    # Print the first result to see if it worked
    if results:
        print("\n--- First Paper Found ---")
        print(f"Title: {results[0]['title']}")
        print(f"Date: {results[0]['date']}")
        print(f"Abstract Snippet: {results[0]['summary'][:200]}...") # First 200 chars