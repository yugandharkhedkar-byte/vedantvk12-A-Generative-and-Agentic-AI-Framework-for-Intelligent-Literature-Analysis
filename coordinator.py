# File: coordinator.py
import os
from groq import Groq
from dotenv import load_dotenv
import json

# --- IMPORTS ---
from search_agent import SearchAgent
from analysis_agent import AnalysisAgent
from trend_agent import TrendAgent
from citation_agent import CitationAgent
from memory_agent import MemoryAgent
from plagiarism_agent import PlagiarismAgent
from ai_detection_agent import AIDetectionAgent
from humanizer_agent import HumanizerAgent

load_dotenv(override=True)

class CoordinatorAgent:
    def __init__(self):
        print("🤖 System: Initializing Coordinator Agent...")
        
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found!")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        
        # Initialize ALL Agents
        self.search_agent = SearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.trend_agent = TrendAgent()
        self.citation_agent = CitationAgent()
        self.memory_agent = MemoryAgent()
        self.plagiarism_agent = PlagiarismAgent()
        self.ai_detection_agent = AIDetectionAgent()
        self.humanizer_agent = HumanizerAgent()

    def query_llm(self, system_prompt, user_input, fallback=True):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                model=self.model,
                temperature=0.3, # Strict consistency
                max_tokens=2000, # Prevent cut-offs
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            # If rate limited, 400, or model decommissioned, gracefully fallback
            if fallback and ("rate limit" in error_msg or "429" in error_msg or "400" in error_msg or "decommissioned" in error_msg):
                print(f"⚠️ API Error ({self.model}): {error_msg}. Falling back to llama-3.1-8b-instant...")
                try:
                    chat_completion = self.client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.3,
                        max_tokens=2000,
                    )
                    return chat_completion.choices[0].message.content
                except Exception as e2:
                    return f"Error communicating with Groq (Fallback also failed): {e2}"
            return f"Error communicating with Groq: {e}"

    def generate_project_sections(self, topic):
        print(f" -> Generating core project sections for {topic}...")
        prompt = f"""
        You are an engineering student writing a final year project paper on: "{topic}".
        Generate highly detailed, academic sections. Focus STRICTLY on the AI Assistant System. No unrelated topics.
        Technical constraints to include: Python-based multi-agent architecture (Query, Research, Summarization, Response agents), React + Tailwind frontend, no database (real-time processing), and API communication.

        Required Output Format (use exactly these headers with ===):
        ===ABSTRACT===
        (150-250 words)
        ===INTRODUCTION===
        (Detailed academic intro)
        ===METHODOLOGY===
        (Explain the multi-agent swarm logic)
        ===IMPLEMENTATION===
        (Explain React, Tailwind, Python APIs)
        ===CONCLUSION===
        (Summary)
        ===FUTURE SCOPE===
        (Future improvements)
        """
        response = self.query_llm("You are a strict academic writer.", prompt)
        
        sections = {
            "ABSTRACT": "", "INTRODUCTION": "", "METHODOLOGY": "", 
            "IMPLEMENTATION": "", "CONCLUSION": "", "FUTURE_SCOPE": ""
        }
        
        curr = None
        for line in response.split('\n'):
            line_upper = line.strip().upper()
            if "===ABSTRACT===" in line_upper: curr = "ABSTRACT"
            elif "===INTRODUCTION===" in line_upper: curr = "INTRODUCTION"
            elif "===METHODOLOGY===" in line_upper: curr = "METHODOLOGY"
            elif "===IMPLEMENTATION===" in line_upper: curr = "IMPLEMENTATION"
            elif "===CONCLUSION===" in line_upper: curr = "CONCLUSION"
            elif "===FUTURE SCOPE===" in line_upper: curr = "FUTURE_SCOPE"
            elif curr:
                sections[curr] += line + "\n"
                
        return sections

    # --- NEW FUNCTION FOR REACT SERVER ---
    def generate_full_report_data(self, topic):
        print(f"\n🎯 Server Processing Topic: {topic}")

        # 1. Refine
        refine_prompt = f"Convert the user's research topic '{topic}' into a highly specific, optimized search query for ArXiv. Focus only on the core technical keywords. Return ONLY the raw keywords separated by spaces. No explanations."
        keywords = self.query_llm("Output only raw text.", refine_prompt).strip().replace('"', '')
        
        # 2. Search
        papers = self.search_agent.search_papers(keywords)
        
        # 3. Analyze
        analyzed_data = self.analysis_agent.analyze_papers(papers, self.query_llm)
        
        # 4. Trends
        trends_text = self.trend_agent.identify_gaps(analyzed_data, self.query_llm)
        trends_list = [line.strip().replace('*', '').replace('-', '') for line in trends_text.split('\n') if len(line) > 10][:10]
        if not trends_list: trends_list = ["Trend analysis is detailed in the PDF report."]

        # Combine text to analyze for AI/Plagiarism
        full_text_to_analyze = trends_text + "\n"
        for p in analyzed_data:
            full_text_to_analyze += p.get('analysis', '') + "\n"

        # 5. Citations (Cleaned for Frontend)
        citations_text = self.citation_agent.generate_citations(papers)
        # Split by newline and remove empty strings
        citations_list = [c.strip() for c in citations_text.split('\n') if c.strip()]

        # 6. Plagiarism Check
        plagiarism_result = self.plagiarism_agent.check_plagiarism(full_text_to_analyze)

        # 7. AI Detection
        ai_detection_result = self.ai_detection_agent.analyze_text(full_text_to_analyze)

        # 8. Humanizer (Humanize trends as an example of humanized output)
        humanizer_result = self.humanizer_agent.humanize_text(trends_text, self.query_llm)
        humanized_trends_list = [line.strip().replace('*', '').replace('-', '') for line in humanizer_result["humanized_text"].split('\n') if len(line) > 10][:10]

        # 8.5 Generate Project Sections
        project_sections = self.generate_project_sections(topic)

        # 9. Save PDF (This triggers the new IEEE format)
        pdf_filename = self.memory_agent.save_report_pdf(
            topic, 
            trends_text, 
            analyzed_data, 
            citations_text,
            ai_score=ai_detection_result["ai_probability"],
            plag_score=plagiarism_result["plagiarism_score"],
            project_sections=project_sections
        )

        # 10. Return JSON
        return {
            "topic": topic,
            "trends": trends_list,
            "humanized_trends": humanized_trends_list,
            "gaps": ["Detailed research gaps are available in the generated PDF."],
            "papers": [
                {
                    "title": p['title'],
                    "date": p['date'],
                    "analysis": p['analysis'], # Full analysis
                    "finding": p['analysis'],  # Use full analysis here too
                    "link": p['url']
                } for p in analyzed_data
            ],
            "references": citations_list, 
            "citations": citations_list, 
            "pdf_link": f"http://localhost:5000/download/{pdf_filename}",
            "plagiarism": plagiarism_result,
            "ai_detection": ai_detection_result
        }


if __name__ == "__main__":
    app = CoordinatorAgent()
    # Simple test execution
    # user_topic = input("Enter a research topic: ")
    # app.generate_full_report_data(user_topic)