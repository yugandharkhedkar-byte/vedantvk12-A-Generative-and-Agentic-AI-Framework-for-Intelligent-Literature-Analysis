class HumanizerAgent:
    def __init__(self):
        print("✨ System: Initializing Humanizer Agent...")

    def humanize_text(self, original_text, llm_query_func):
        prompt = """
        You are a distinguished senior research academic and professional science communicator. Your task is to transform the provided AI-generated text into a highly natural, detailed, and sophisticated academic narrative.
        
        CRITICAL DIRECTIVES:
        1. DEPTH & DETAIL: Do not just summarize. Expand on the concepts. If the input mentions a trend, explain WHY it is significant and its broader implications.
        2. NATURAL FLOW: Vary sentence structure extensively. Use a mix of complex, compound, and simple sentences to create a rhythmic, human-like cadence.
        3. SOPHISTICATED VOCABULARY: Use precise academic terminology, but avoid stereotypical AI "filler" words (e.g., "tapestry", "delve", "realm", "pivotal", "underscores", "moreover", "furthermore").
        4. ENGAGING NARRATIVE: The text should read like a well-written literature review introduction, not a bulleted list.
        5. DO NOT add any meta-talk like "Here is the humanized version". Output ONLY the rewritten text.
        
        Make the output at least 50% longer than the input by adding context and analytical depth.
        """
        
        try:
            humanized_text = llm_query_func(prompt, original_text)
            
            return {
                "original_text": original_text,
                "humanized_text": humanized_text.strip()
            }
        except Exception as e:
            print(f"Error in Humanizer Agent: {e}")
            return {
                "original_text": original_text,
                "humanized_text": original_text  # Fallback to original
            }
