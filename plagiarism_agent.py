import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class PlagiarismAgent:
    def __init__(self):
        print("🕵️ System: Initializing Plagiarism Agent...")
        # Mock database of "existing literature"
        self.knowledge_base = [
            "The rapid expansion of research in artificial intelligence has created a need for automated analysis tools.",
            "This paper utilizes a Generative and Agentic AI framework to systematically review the current state of the art.",
            "Machine learning models are increasingly being deployed in healthcare systems.",
            "Quantum error correction remains a significant hurdle in the development of scalable quantum computers.",
            "The objective is to identify methodologies, compare results, and detect gaps in the existing literature.",
            "Large language models have shown remarkable capabilities in natural language understanding.",
            "Automated literature reviews can significantly reduce the time researchers spend on preliminary research.",
            "The system employs a Hub-and-Spoke multi-agent architecture.",
            "Data synthesis and analysis are core components of systematic reviews."
        ]
        self.vectorizer = TfidfVectorizer().fit(self.knowledge_base)
        self.kb_vectors = self.vectorizer.transform(self.knowledge_base)

    def _get_sentences(self, text):
        # Basic sentence splitting
        text = re.sub(r'\n+', ' ', text)
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]

    def check_plagiarism(self, text):
        sentences = self._get_sentences(text)
        if not sentences:
            return {"plagiarism_score": 0, "risk": "Low", "matched_sources": []}

        # Vectorize input sentences
        input_vectors = self.vectorizer.transform(sentences)
        
        # Calculate cosine similarity against knowledge base
        similarities = cosine_similarity(input_vectors, self.kb_vectors)
        
        # For each sentence, find the max similarity in KB
        max_sims = np.max(similarities, axis=1)
        
        # Overall plagiarism score is the average of max similarities * 100
        # If max_sim is > 0.8, it's a strong match
        plagiarized_count = np.sum(max_sims > 0.6)
        
        overall_score = float(np.mean(max_sims) * 100)
        # Boost score slightly to make it look realistic if there are strong matches
        if plagiarized_count > 0:
            overall_score = min(100.0, overall_score + (plagiarized_count * 5))

        # Determine risk
        risk = "Low"
        if overall_score > 40:
            risk = "High"
        elif overall_score > 15:
            risk = "Medium"

        # Find top 3 matches
        matched_sources = []
        if plagiarized_count > 0:
            # Get indices of top matches
            top_indices = np.argsort(max_sims)[-3:][::-1]
            for idx in top_indices:
                sim = max_sims[idx]
                if sim > 0.3:
                    matched_kb_idx = np.argmax(similarities[idx])
                    matched_sources.append({
                        "matched_text": self.knowledge_base[matched_kb_idx],
                        "similarity": round(float(sim) * 100, 1),
                        "source": f"IEEE Xplore - Document ID: {np.random.randint(10000, 99999)}"
                    })

        # Ensure we always have some dummy matches for UI display if none found above 0.3, just for demonstration
        if not matched_sources and overall_score > 0:
             top_idx = np.argmax(max_sims)
             if max_sims[top_idx] > 0.1:
                matched_kb_idx = np.argmax(similarities[top_idx])
                matched_sources.append({
                    "matched_text": self.knowledge_base[matched_kb_idx],
                    "similarity": round(float(max_sims[top_idx]) * 100, 1),
                    "source": f"ArXiv - Pre-print {np.random.randint(1000, 9999)}"
                })

        return {
            "plagiarism_score": round(overall_score, 1),
            "risk": risk,
            "matched_sources": matched_sources
        }
