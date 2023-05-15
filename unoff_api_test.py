from twitter.scraper import Scraper

email, username, password = 'peter.nadel@tufts.edu', 'tufts_dh', 'TuftsDH2022!'
scraper = Scraper(email, username, password, save=True, debug=False)
