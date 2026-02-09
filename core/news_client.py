import os
import requests
import random
from config.settings import Settings

class NewsClient:
    def __init__(self):
        self.api_key = Settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"
        
        # High-Volume Keywords
        self.STRATEGIC_THEMES = {
            "Banking & FinTech AI": (
                "Fintech OR Digital Banking OR AI Finance OR Open Banking OR "
                "Future of Payments OR Blockchain Finance OR Generative AI Banking"
            ),
            "Smart City & Surveillance": (
                "Smart Cities OR Urban Tech OR AI Surveillance OR Smart Infrastructure OR "
                "Intelligent Transport OR Public Safety Tech OR GovTech"
            ),
            "EdTech & Learning": (
                "EdTech OR Future of Learning OR AI Education OR Digital Classrooms OR "
                "Education Technology OR Personalized Learning OR Reskilling"
            ),
            "Enterprise Automation": (
                "Enterprise AI OR Digital Transformation OR Business Automation OR "
                "Future of Work OR RPA OR Artificial Intelligence Business OR SaaS Trends"
            ),
            "Energy & Power Tech": (
                "Green Tech OR Clean Energy OR Smart Grid OR Renewable Technology OR "
                "Energy Storage OR Climate Tech OR Sustainable Energy"
            ),
            "Healthcare & Life Sciences": (
                "Digital Health OR MedTech OR AI Healthcare OR Biotech Innovation OR "
                "Smart Hospitals OR Telemedicine OR HealthTech"
            )
        }

    def _filter_articles(self, articles, topic_key):
        """
        The Gatekeeper: Aggressively removes noise (Sports, Cars, Supplements, TV).
        """
        # STRICTER Whitelist: Must contain strong tech/business signals
        valid_keywords = [
            "AI", "Artificial Intelligence", "GenAI", "LLM", "Machine Learning",
            "SaaS", "Enterprise", "Startup", "Equity", "Revenue", "Investment",
            "Digital Transformation", "Cloud", "Cybersecurity", "Automation",
            "Fintech", "Blockchain", "Robot", "Smart City", "Infrastructure",
            "Platform", "Software", "Data Center", "API", "Algorithm"
        ]
        
        # EXPANDED Blocklist based on your debug logs
        blocklist = [
            # Sports
            "NFL", "NBA", "Super Bowl", "Cricket", "Football", "Score", "Highlights",
            "Lakers", "Warriors", "Spurs", "Arsenal", "Premier League",
            # Entertainment
            "Movie", "Trailer", "Episode", "Season", "Celeb", "Actor", "Actress", 
            "Concert", "Review", "Hallmark", "Netflix", "HBO", "Disney",
            # Retail / Lifestyle / Cars
            "Deal", "Discount", "Coupon", "Recipe", "Diet", "Supplement", "Vitamin",
            "Porsche", "Chevrolet", "Lexus", "Infiniti", "Toyota", "Ford", "0-60",
            "Decor", "Fashion", "Beauty", "Skincare", "K-Pop",
            # Dev Noise
            "PyPI", "GitHub", "Commit", "Stack Overflow"
        ]

        clean_list = []
        for art in articles:
            # Combine title and description for checking
            text_blob = (str(art.get('title', '')) + " " + str(art.get('description', ''))).lower()
            
            # 1. Kill Noise
            if any(bad.lower() in text_blob for bad in blocklist):
                continue
                
            # 2. Require Signal
            if any(good.lower() in text_blob for good in valid_keywords):
                clean_list.append(art)
                
        return clean_list

    def fetch_global_innovation(self, selected_topics):
        if not selected_topics: return []
            
        queries = [self.STRATEGIC_THEMES.get(topic, topic) for topic in selected_topics]
        combined_query = " OR ".join(f"({q})" for q in queries)
        
        params = {
            'q': combined_query,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 100, # Fetch huge pool
            'apiKey': self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if data.get("status") == "ok" and data.get("totalResults", 0) > 0:
                raw_articles = data['articles']
                print(f"[DEBUG] Fetched {len(raw_articles)} articles for topics: {', '.join(selected_topics)}")
                
                # Apply Strict Filter
                filtered_articles = self._filter_articles(raw_articles, selected_topics)
                print(f"[DEBUG] {len(filtered_articles)} articles remain after filtering.")
                
                # If we have enough clean articles, shuffle and return
                if len(filtered_articles) > 0:
                    # Randomize to ensure freshness every click
                    random.shuffle(filtered_articles)
                    print(f"[DEBUG] Titles {[a['title'] for a in filtered_articles[:15]]}")
                    return filtered_articles[:15]
                
            # Fallback only if strict filter killed everything
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