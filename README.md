# DGDA Autoscraper

Using GitHub Actions and Python, this repo automatically scrapes the content of Bangladesh's Directorate General of Drug Administration's allopathic medicines registry every month. Changes will be appended based on DAR field. An email of the file will be sent only if there have been changes.

Files in repo:
- scrape.py: python scraping script
- send_mail.py: python sendgrid mailer script
- bdg_scraped.csv: scraped pricing database, updated only upon DGDA website update
- DGDA Scraper.ipynb: jupyter notebook explaining process
- .github/workflows: yaml file for automation
