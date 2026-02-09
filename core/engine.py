import re
from google import genai
from config.settings import Settings

class StrategicEngine:
    def __init__(self):
        self.client = genai.Client(api_key=Settings.GEMINI_API_KEY)

    def analyze_global_trends(self, topics, news_data):
        if not news_data:
            return 50, "No data available. Recommend expanding search parameters."

        # Format news for the prompt
        context = "\n".join([f"- {a['title']}: {a['description']}" for a in news_data[:10]])
        topic_str = ", ".join(topics)
        
        prompt = f"""
        ROLE: Global Innovation Consultant for Jaffer Business Systems (JBS).
        MISSION: Help JBS hit PKR 100 Billion Revenue by adopting WORLD-CLASS technology.
        FOCUS AREA: {topic_str}

        GLOBAL INTEL (What the world's best are doing):
        {context}

        TASK:
        1. Analyze these global trends.
        2. Bridge the gap: How can JBS bring this SPECIFIC technology to Pakistan?
        3. Create a strategy that makes local competitors look outdated.

        OUTPUT FORMAT:
        SCORE: [0-100 Global Alignment Score]
        
        MEMO:
        🚀 VISION 2030 IMPACT: 
        (Explain how adopting these global standards captures high-value revenue for JBS.)
        
        🚩 COMPETITIVE GAP ANALYSIS:
        (Compare JBS not just to locals, but to GLOBAL standards. "Local rivals are doing X, but Global leaders are doing Y. JBS must do Y.")
        
        💡 THE 'WORKS BETTER' STRATEGIC MOVE:
        (Propose a specific product/service JBS should launch NOW to bring this global tech to the local market.)
        """
        
        try:
            response = self.client.models.generate_content(
                model=Settings.MODEL_ID,
                contents=prompt
            )
            res_text = response.text
            
            # Extract Score
            score_match = re.search(r"SCORE:\s*(\d+)", res_text)
            score = int(score_match.group(1)) if score_match else 85
            
            # Extract Memo
            if "MEMO:" in res_text:
                memo = res_text.split("MEMO:")[-1].strip()
            else:
                memo = res_text
                
            return score, memo

        except Exception as e:
            return 0, f"Error generating strategy: {str(e)}"