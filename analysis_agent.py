# File: analysis_agent.py

class AnalysisAgent:
    def __init__(self):
        print("🧠 System: Initializing Analysis Agent...")

    def analyze_papers(self, papers, llm_function):
        """
        Takes a list of papers and a function to call the LLM.
        Returns a list of analyzed summaries.
        """
        print(f" -> Analysis Agent: Reading {len(papers)} abstracts...")
        
        analyzed_results = []

        for paper in papers:
            print(f"   ... Analyzing: {paper['title'][:30]}...")
            
            # --- THE FIX FOR PLAGIARISM ---
            # We explicitly tell the LLM to "Rewrite" and "Change sentence structure"
            prompt = f"""
            You are a strict academic editor. Rewrite the following abstract into a unique analysis.
            
            INPUT ABSTRACT: {paper['summary']}
            
            CRITICAL INSTRUCTIONS:
            1. Base your analysis STRICTLY on the provided abstract. Do NOT hallucinate or include unrelated datasets, domains, or topics (e.g., LIGO, astronomy, unrelated physics) unless explicitly mentioned in the text.
            2. Maintain strict topic consistency. Do not wander off-topic.
            3. Do NOT just summarize. Rephrase the core ideas completely using your own vocabulary.
            4. Change the sentence structure significantly to avoid plagiarism detection.
            5. Use active voice where possible.
            
            OUTPUT FORMAT (Strictly follow these 3 headers):
            1. Core Problem: (A highly detailed explanation of the research challenge, historical context, and importance)
            2. Methodology: (A comprehensive breakdown of the technical approach, architectures, algorithms, datasets, and equations if applicable)
            3. Key Finding: (The significant discoveries, performance metrics, implications, and future work)
            
            Provide a detailed, professional technical analysis for each section (3-4 sentences per section). Do not be overly verbose. Ensure responses are complete and not cut off.
            """

            # 2. Call the LLM using the function passed from Coordinator
            response = llm_function(
                system_prompt="You are an expert research scientist. Analyze the abstract critically.",
                user_input=prompt
            )
            
            # 3. Store the result
            analyzed_results.append({
                "title": paper['title'],
                "date": paper['date'],
                "analysis": response,
                "url": paper['url']
            })
            
        return analyzed_results