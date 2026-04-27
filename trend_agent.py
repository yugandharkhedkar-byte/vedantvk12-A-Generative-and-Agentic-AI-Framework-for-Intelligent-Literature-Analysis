# File: trend_agent.py

class TrendAgent:
    def __init__(self):
        print("📈 System: Initializing Trend Agent...")

    def identify_gaps(self, analyzed_data, llm_function):
        """
        Synthesizes multiple paper summaries to find research trends and gaps.
        """
        print(" -> Trend Agent: Analyzing research trends and gaps...")
        
        # 1. Combine all summaries into one big text block
        combined_text = ""
        for item in analyzed_data:
            combined_text += f"PAPER: {item['title']}\nSUMMARY: {item['analysis']}\n\n"

        # 2. Create the prompt — ask for VERY detailed output
        prompt = f"""
        You are a senior research supervisor and expert at synthesizing academic literature.
        Based on the following summaries of {len(analyzed_data)} academic papers, produce a comprehensive analysis.

        Papers:
        {combined_text}

        Generate a DETAILED structured report with the following sections. Each section must have AT LEAST 3-5 detailed bullet points with full explanations. Do not be brief.

        ## Section 1: Dominant Trends
        Identify 5 major recurring themes or technological directions across the papers. For each trend:
        - State the trend clearly
        - Explain WHY it is significant and what is driving it
        - Reference which papers support it

        ## Section 2: Methodological Approaches
        Identify 4 key methodological patterns. For each:
        - Describe the technique or framework being used
        - Explain its advantages and limitations

        ## Section 3: Research Gaps & Open Problems
        Identify 5 specific, concrete research gaps that are NOT being addressed:
        - Clearly state the unsolved problem
        - Explain why it matters for future research
        - Suggest potential directions to address it

        ## Section 4: Future Outlook
        Provide 3 forward-looking predictions about where this field is headed in the next 3-5 years.

        Be thorough and analytical. This will be published in an academic report.
        
        CRITICAL INSTRUCTIONS:
        1. Maintain absolute topic consistency. Do NOT hallucinate trends, datasets, or fields (e.g., LIGO, astronomy, unrelated physics) that are not present in the provided summaries.
        2. Ensure all generated text strictly relates to the user's research domain based on the summaries.
        3. Do not leave bullet points half-finished or cut off. Ensure complete output.
        """

        # 3. Ask the LLM
        response = llm_function(
            system_prompt="You are a world-class senior research supervisor. Produce extremely detailed, insightful academic analysis. Do not be brief.",
            user_input=prompt
        )
        
        return response