import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TARGET_URL = "https://news.ycombinator.com/" # Hacker News as a source
KEYWORDS = ['AI', 'GPT', 'LLM', 'Neural', 'Machine Learning', 'OpenAI', 'DeepMind', 'Anthropic']

client = OpenAI(api_key=OPENAI_API_KEY)

def get_ai_headlines():
    """Scrapes headlines from the target URL and filters by AI keywords."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        logging.info(f"Fetching news from {TARGET_URL}...")
        response = requests.get(TARGET_URL, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = []
        
        # Selector specific to Hacker News (class 'titleline')
        for item in soup.select(".titleline > a"):
            title = item.get_text()
            link = item.get('href')
            
            # Filter by keywords
            if any(k.lower() in title.lower() for k in KEYWORDS):
                headlines.append(f"- {title} ({link})")
                
        logging.info(f"Found {len(headlines)} relevant articles.")
        return headlines
    
    except Exception as e:
        logging.error(f"Error scraping data: {e}")
        return []

def generate_summary(headlines):
    """Uses OpenAI API to generate a concise summary of the headlines."""
    if not headlines:
        return None

    text_block = "\n".join(headlines)
    prompt = (
        f"Here is a list of recent tech headlines:\n{text_block}\n\n"
        "Task: Summarize the key AI trends or events from this list in Russian. "
        "Keep it concise (3 bullet points maximum). "
        "Start with an engaging emoji title."
    )

    try:
        logging.info("Generating summary via OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Cost-effective model
            messages=[
                {"role": "system", "content": "You are a tech journalist providing concise daily briefings."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI API Error: {e}")
        return None

def send_telegram_message(message):
    """Sends the summary to a Telegram chat."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.warning("Telegram credentials not found. Skipping notification.")
        print(message) # Fallback to console
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logging.info("Message sent to Telegram successfully.")
        else:
            logging.error(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        logging.error(f"Telegram connection error: {e}")

if __name__ == "__main__":
    ai_news = get_ai_headlines()
    
    if ai_news:
        summary = generate_summary(ai_news)
        if summary:
            send_telegram_message(summary)
    else:
        logging.info("No AI news found today.")
