import re
import numpy as np
from collections import Counter

class AIDetectionAgent:
    def __init__(self):
        print("🤖 System: Initializing AI Detection Agent...")

    def _get_sentences(self, text):
        text = re.sub(r'\n+', ' ', text)
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if len(s.strip()) > 5]

    def _calculate_perplexity_proxy(self, sentences):
        """
        Approximates perplexity by analyzing sentence length predictability.
        AI text often has very uniform sentence lengths (low variance).
        Human text has high variance in sentence length.
        """
        if not sentences: return 50
        
        lengths = [len(s.split()) for s in sentences]
        variance = np.var(lengths)
        
        # If variance is low, it's highly predictable -> more likely AI
        # If variance is high, it's less predictable -> more likely Human
        # Let's map variance (0 to ~100) to an AI score (0 to 1)
        # Expected human variance might be around 50-100.
        
        ai_prob = max(0, min(1, 1.0 - (variance / 80.0)))
        return ai_prob

    def _calculate_burstiness(self, sentences):
        """
        Burstiness measures the variation of sentence lengths.
        High burstiness = human (mix of very long and very short).
        Low burstiness = AI (consistent lengths).
        """
        if len(sentences) < 2: return 0.5
        lengths = [len(s.split()) for s in sentences]
        max_len = max(lengths)
        min_len = min(lengths)
        avg_len = np.mean(lengths)
        
        # Burstiness proxy: (max - min) / avg
        burst_score = (max_len - min_len) / (avg_len + 1e-5)
        
        # High burst score (e.g. > 1.5) -> Human
        # Low burst score (e.g. < 0.5) -> AI
        ai_prob = max(0, min(1, 1.5 - burst_score))
        return ai_prob

    def _detect_repetition(self, text):
        """
        AI tends to reuse certain transition words and structures.
        """
        words = re.findall(r'\b\w+\b', text.lower())
        if not words: return 0.5
        
        # Common AI transition words / structures
        ai_markers = [
            "furthermore", "moreover", "in conclusion", "it is important to note",
            "additionally", "crucial", "delve", "tapestry", "realm", "underscores"
        ]
        
        marker_count = sum(1 for word in words if word in ai_markers)
        word_count = len(words)
        
        # Frequency of AI markers
        freq = marker_count / (word_count + 1e-5)
        
        # If high frequency (> 2%), likely AI
        ai_prob = min(1, freq * 50)
        return ai_prob

    def analyze_text(self, text):
        sentences = self._get_sentences(text)
        
        if not sentences:
            return {"ai_probability": 0.0, "label": "Human Written"}

        perplexity_prob = self._calculate_perplexity_proxy(sentences)
        burstiness_prob = self._calculate_burstiness(sentences)
        repetition_prob = self._detect_repetition(text)

        # Weighted combination
        final_prob = (0.4 * perplexity_prob) + (0.4 * burstiness_prob) + (0.2 * repetition_prob)
        
        # Determine label
        if final_prob > 0.8:
            label = "Highly Likely AI Generated"
        elif final_prob > 0.6:
            label = "Likely AI Generated"
        elif final_prob > 0.4:
            label = "Mixed / Unclear"
        else:
            label = "Likely Human Written"

        return {
            "ai_probability": round(float(final_prob) * 100, 1),
            "label": label,
            "metrics": {
                "perplexity_proxy": round(float(perplexity_prob), 2),
                "burstiness": round(float(burstiness_prob), 2),
                "repetition": round(float(repetition_prob), 2)
            }
        }
