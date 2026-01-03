# 🤖 AI Tech News Aggregator

An automated data pipeline that scrapes the latest tech news, filters for AI/ML topics, summarizes them using GPT-4, and delivers a daily digest via Telegram.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenAI](https://img.shields.io/badge/API-OpenAI-green)
![License](https://img.shields.io/badge/License-MIT-purple)

## 📌 Overview

Keeping up with the rapid pace of Artificial Intelligence developments is challenging. This project automates the consumption of information by:
1.  **Scraping** reputable tech news sources (e.g., Hacker News).
2.  **Filtering** content specifically related to AI, LLMs, and Machine Learning.
3.  **Synthesizing** a 3-bullet-point summary using OpenAI's GPT models.
4.  **Notifying** the user instantly via a Telegram Bot.

## 🛠 Tech Stack

* **Language:** Python 3
* **Web Scraping:** BeautifulSoup4, Requests
* **AI Engine:** OpenAI API (GPT-4o-mini / GPT-3.5)
* **Notifications:** Telegram Bot API
* **Automation:** GitHub Actions (Cron Job)

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/ai-news-aggregator.git](https://github.com/your-username/ai-news-aggregator.git)
cd ai-news-aggregator
