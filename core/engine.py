import re
from google import genai
from config.settings import Settings

class StrategicEngine:
    def __init__(self):
        self.client = genai.Client(api_key=Settings.GEMINI_API_KEY)

    def analyze_market_intelligence(self, unit_name: str, news_data: list):
        if not news_data:
            return 50, "No high-impact signals found. Recommend scanning KSA government tenders manually."

        context = "\n".join([f"SIGNAL: {a['title']}" for a in news_data[:12]])
        
        # PROMPT: Hardcoding the JBS Vision 2030 Report Context
        prompt = f"""
        Act as the JBS Strategic Intelligence Lead. 
        JBS GOAL: PKR 100 Billion Revenue by 2030. 
        JBS PIVOT: Transition from hardware vendor to AI & Computer Vision leader.
        JBS FOCUS: Pakistan Trust vs. KSA/Global Innovation.
        
        DATA TO FILTER:
        {context}
        
        TASK:
        1. Throw away generic tech news.
        2. Identify GAPS where competitors like Systems Ltd or 10Pearls are leading.
        3. Recommend a specific 'Human-Centric AI' move to counter rivals.
        
        RESPONSE FORMAT:
        SCORE: [0-100 Opportunity Score]
        MEMO:
        🚀 VISION 2030 IMPACT: (How this hits our PKR 100B target)
        🚩 COMPETITIVE GAP: (Specific moves by rivals in {unit_name})
        💡 THE JBS 'WORKS BETTER' MOVE: (Actionable advice for the KSA/Local sales team)
        """
        
        response = self.client.models.generate_content(
            model=Settings.MODEL_ID,
            contents=prompt
        )
        
        res_text = response.text
        score_match = re.search(r"SCORE:\s*(\d+)", res_text)
        score = int(score_match.group(1)) if score_match else 50
        memo = res_text.split("MEMO:")[-1].strip() if "MEMO:" in res_text else res_text
        
        return score, memo