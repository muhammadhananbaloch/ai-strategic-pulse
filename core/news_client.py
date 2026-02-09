import os
import requests
import random
from config.settings import Settings

class NewsClient:
    def __init__(self):
        self.api_key = Settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"
        
        # OPTIMIZED QUERIES: Focused on "Market", "Business", and "Tech" to avoid lifestyle noise
        self.STRATEGIC_THEMES = {
            "Banking & FinTech AI": (
                '"Fintech Market" OR "Digital Banking Trends" OR "AI in Finance" OR '
                '"Open Banking" OR "Future of Payments" OR "Generative AI Banking" OR '
                '"Blockchain Finance" OR "Bank Automation"'
            ),
            "Smart City & Surveillance": (
                '"Smart City Market" OR "Urban Tech Investment" OR "AI Surveillance" OR '
                '"Intelligent Transport System" OR "GovTech Trends" OR "Public Safety Tech" OR '
                '"Smart Infrastructure"'
            ),
            "EdTech & Learning": (
                '"EdTech Market" OR "AI in Education" OR "Corporate Reskilling" OR '
                '"Digital Classroom Market" OR "Learning Management Systems" OR '
                '"Educational Technology Trends" OR "Personalized Learning AI"'
            ),
            "Enterprise Automation": (
                '"Enterprise AI" OR "Business Process Automation" OR "RPA Market" OR '
                '"Digital Transformation Trends" OR "SaaS Growth" OR "Future of Work Tech" OR '
                '"AI Workforce"'
            ),
            "Energy & Power Tech": (
                '"Clean Energy Market" OR "Smart Grid Technology" OR "Renewable Energy Investment" OR '
                '"Energy Storage Trends" OR "Green Tech Innovation" OR "Climate Tech Startup"'
            ),
            "Healthcare & Life Sciences": (
                '"Digital Health Market" OR "MedTech Innovation" OR "AI Drug Discovery" OR '
                '"Telemedicine Trends" OR "Smart Hospital" OR "HealthTech Investment" OR '
                '"Medical Robotics"'
            )
        }

    def _filter_articles(self, articles):
        """
        The Gatekeeper: Aggressively removes Politics, Sports, Cars, and Lifestyle noise.
        """
        # STRICT Whitelist: Article MUST have at least one of these to pass
        valid_keywords = [
            "market", "growth", "launch", "tech", "ai", "data", "digital", 
            "system", "platform", "enterprise", "industry", "startup", "invest", 
            "funding", "revenue", "software", "automation", "cyber", "cloud", 
            "smart", "transform", "solution", "service", "sector", "trend"
        ]
        
        # EXPANDED Blocklist: The "Noise Killer"
        blocklist = [
            # Politics & Crime (Huge source of noise)
            "trump", "biden", "kamala", "election", "voter", "poll", "senate", "congress",
            "democrat", "republican", "lawsuit", "court", "judge", "police", "arrest", 
            "shooting", "murder", "crime", "war", "gaza", "israel", "ukraine", "russia",
            "strike", "protest", "prison", "jail",
            
            # Sports (Olympics were clogging EdTech)
            "olympic", "medal", "game", "match", "score", "league", "cup", "nfl", "nba",
            "football", "cricket", "soccer", "tennis", "athlete", "coach", "stadium",
            
            # Cars (Mercedes was clogging everything)
            "mercedes", "bmw", "ford", "toyota", "honda", "lexus", "sedan", "suv", "truck",
            "4matic", "engine", "horsepower", "dealer", "drive",
            
            # Lifestyle / Home / Celeb
            "kitchen", "decor", "home", "garden", "recipe", "diet", "weight", "fashion",
            "beauty", "movie", "film", "star", "actor", "actress", "concert", "ticket",
            "episode", "season", "show", "netflix", "hbo", "disney", "review"
        ]

        clean_list = []
        seen_titles = set()

        for art in articles:
            # Clean text for checking
            title = str(art.get('title', '')).strip()
            desc = str(art.get('description', '')).strip()
            text_blob = (title + " " + desc).lower()
            
            # 1. Deduplicate
            if title in seen_titles:
                continue
            seen_titles.add(title)
            
            # 2. Kill Noise (If any bad word is present)
            if any(bad in text_blob for bad in blocklist):
                continue
                
            # 3. Require Business Signal (Must have valid keyword)
            if any(good in text_blob for good in valid_keywords):
                clean_list.append(art)
                
        return clean_list

    def fetch_global_innovation(self, selected_topics):
        if not selected_topics: return []
            
        # Join queries with OR
        queries = [self.STRATEGIC_THEMES.get(topic, topic) for topic in selected_topics]
        combined_query = " OR ".join(f"({q})" for q in queries)
        
        params = {
            'q': combined_query,
            'language': 'en',
            'sortBy': 'publishedAt', # Newest first
            'pageSize': 100,         # Maximize pool for filtering
            'apiKey': self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if data.get("status") == "ok" and data.get("totalResults", 0) > 0:
                raw_articles = data['articles']
                print(f"[DEBUG] Raw Fetch: {len(raw_articles)} articles.")
                
                # Apply Strict Filter
                filtered_articles = self._filter_articles(raw_articles)
                print(f"[DEBUG] After Filtering: {len(filtered_articles)} clean articles.")
                
                # If we have enough clean articles, shuffle and return
                if len(filtered_articles) > 0:
                    random.shuffle(filtered_articles)
                    # print(f"[DEBUG] Titles {[a['title'] for a in filtered_articles[:15]]}")
                    return filtered_articles[:15] # Return top 15 clean ones
                
            print("[DEBUG] No clean results found. Switching to Mock Data.")
            return self._get_global_mock_data(selected_topics)

        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return self._get_global_mock_data(selected_topics)

    def _get_global_mock_data(self, topics):
        """
        Fallback: High-End Global Innovation Headlines.
        """
        mock_library = [
            {
                "source": {"name": "TechCrunch"},
                "title": "JP Morgan Deploys Generative AI Assistant to 50,000 Employees",
                "description": "The banking giant bets big on LLMs for internal productivity."
            },
            {
                "source": {"name": "VentureBeat"},
                "title": "Saudi Neom City Tests Advanced Computer Vision for Traffic Control",
                "description": "AI-driven surveillance set to revolutionize smart city management in KSA."
            },
            {
                "source": {"name": "Forbes Tech"},
                "title": "The Rise of 'Human-Centric' AI in Customer Service: 2026 Trends",
                "description": "Why empathy is the new frontier for automated banking agents."
            },
            {
                "source": {"name": "Bloomberg"},
                "title": "Global Banks Shift to 'Hyper-Personalization' Engines Powered by AI",
                "description": "Standard banking apps are dead; AI prediction is the future."
            }
        ]
        return mock_library