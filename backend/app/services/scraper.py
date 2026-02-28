import requests
from bs4 import BeautifulSoup
from app.models.models import Opportunity
from app.db.session import SessionLocal
from datetime import datetime
import time

class ScraperService:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    SOURCES = {
        "Yale": "https://events.yale.edu/events",
        "Harvard": "https://pce.harvard.edu/events",
    }

    def _get_soup(self, url):
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, headers=self.HEADERS, timeout=10)
            response.raise_for_status()
            print(f"Successfully fetched: {url}")
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Scraper Error for {url}: {str(e)}")
            return None

    def scrape_yale(self):
        soup = self._get_soup(self.SOURCES["Yale"])
        if not soup: return []
        
        events = []
        # Target the specific Yale event cards
        for item in soup.select('.event-card, .lw_cal_event, .event-item'):
            try:
                title_elem = item.select_one('.lw_event_title, h3, .title, a')
                if not title_elem: continue
                
                title = title_elem.get_text(strip=True)
                summary_elem = item.select_one('.lw_event_summary, .description, .summary, .event-description')
                desc = summary_elem.get_text(strip=True) if summary_elem else "Explore this Yale academic opportunity."
                
                link_elem = item.find('a')
                link = link_elem['href'] if link_elem and link_elem.has_attr('href') else self.SOURCES["Yale"]
                if link.startswith('/'):
                    link = "https://events.yale.edu" + link

                events.append({
                    "title": title[:200],
                    "description": desc,
                    "url": link,
                    "source": "Yale",
                    "domain": "General" 
                })
            except Exception as e:
                print(f"Error parsing Yale item: {e}")
                
        return events

    def scrape_harvard(self):
        soup = self._get_soup(self.SOURCES["Harvard"])
        if not soup: return []
        
        events = []
        # PC Harvard events use 'views-row' or similar
        for item in soup.select('.views-row, .event-teaser, .node-event'):
            try:
                title_elem = item.select_one('h2, h3, .field-name-title')
                if not title_elem: continue
                
                title = title_elem.get_text(strip=True)
                desc_elem = item.select_one('.field-name-body, .summary, .description')
                desc = desc_elem.get_text(strip=True) if desc_elem else "Discover Harvard research and fellowships."
                
                link_elem = item.find('a')
                link = link_elem['href'] if link_elem and link_elem.has_attr('href') else self.SOURCES["Harvard"]
                if link.startswith('/'):
                    link = "https://pce.harvard.edu" + link

                events.append({
                    "title": title[:200],
                    "description": desc,
                    "url": link,
                    "source": "Harvard",
                    "domain": "General"
                })
            except Exception as e:
                print(f"Error parsing Harvard item: {e}")
                
        return events

    def sync_all(self):
        db = SessionLocal()
        from app.services.intelligence import intelligence_engine
        
        all_events = []
        all_events.extend(self.scrape_yale())
        all_events.extend(self.scrape_harvard())
        
        added_count = 0
        for event_data in all_events:
            # Check if exists by URL or Title to avoid duplicates
            exists = db.query(Opportunity).filter(
                (Opportunity.url == event_data["url"]) | (Opportunity.title == event_data["title"])
            ).first()
            
            if not exists:
                domain = intelligence_engine.classify(f"{event_data['title']} {event_data['description']}")
                event_data["domain"] = domain
                
                new_opp = Opportunity(**event_data)
                db.add(new_opp)
                added_count += 1
        
        db.commit()
        db.close()
        return added_count

scraper_service = ScraperService()
