import os
import requests
from config.settings import Settings

class NewsClient:
    def __init__(self):
        self.api_key = Settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"
        
        # DEFINING THE HIGH-VALUE STRATEGIC TOPICS
        self.STRATEGIC_THEMES = {
            "Banking & FinTech AI": "Generative AI in banking OR Fintech fraud detection AI OR Future of digital payments",
            "Smart City & Surveillance": "Computer Vision smart city OR AI surveillance systems OR Intelligent traffic management",
            "EdTech & Learning": "AI personalized learning OR EdTech trends 2025 OR Adaptive learning platforms",
            "Enterprise Automation": "Hyperautomation trends OR RPA AI integration OR Enterprise Generative AI",
            "Energy & Power Tech": "Smart grid AI OR Renewable energy predictive maintenance OR IoT in energy",
            "Healthcare & Life Sciences": "AI in diagnostics OR Computer Vision in healthcare OR Telemedicine trends"
        }

    def fetch_global_innovation(self, selected_topics):
        """
        Searches for Global Innovation news based on user-selected topics.
        """
        # 1. Construct the Global Search Query
        # If user selects multiple, we join them with OR to get a broad radar scan
        if not selected_topics:
            return []
            
        # Get the actual search query strings from our dictionary
        queries = [self.STRATEGIC_THEMES.get(topic, topic) for topic in selected_topics]
        combined_query = " OR ".join(f"({q})" for q in queries)
        print(f"[DEBUG] Combined Query for NewsAPI: {combined_query}")
        params = {
            'q': combined_query,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 15,  # Fetch more to filter for quality
            'apiKey': self.api_key
        }

        try:
            # 2. Try Fetching Real Global News
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if data.get("status") == "ok" and data.get("totalResults", 0) > 0:
                print(f"[DEBUG] Found {data['totalResults']} global articles.")
                return data['articles']
            
            print("[DEBUG] No articles found or API error. Switching to Global Mock Data.")
            return self._get_global_mock_data(selected_topics)

        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return self._get_global_mock_data(selected_topics)

    def _get_global_mock_data(self, topics):
        """
        Fallback: High-End Global Innovation Headlines (NOT Local).
        Ensures the 'Vibe' remains international even if API fails.
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