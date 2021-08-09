## culpa-cache Scraper (Python)

Created by: [Richard Shin](https://www.rshin.dev/)

`main.py` scrapes CULPA (or Wayback Machine archives) for all pertinent information: professor name, professor ID (as assigned by CULPA), course name of the review, date of the review, review content.

Since professor ID's are not 100% incremental (well, maybe they were, but some are missing/deleted/not cached), the script begins scraping from professor ID 1.

When a successful scrape occurs a `.json` file is saved in the `data` folder with the following naming convention: `prof-{id}.json`. So, reviews from `http://www.culpa.info/professors/1` is saved as `prof-1.json`.

If the script is unsuccessful in scraping from that ID it'll increment by one and try again.

There are two measures in place to prevent rate limitation: 
1. Quit scraping if there are too many consecutive failed scrapes,
2. Five second delay in execution of the next scrape (comes out to around ~560 actions per hour).

`export.py` extracts just the Professor Name and ID from all the .json files in `data` and compiles it into one file: `all_professors.json`. This file is later used in the API server.