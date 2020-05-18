# Article analysis for political intend
Background: A similar project was already conducted.
## Goal
1. Build a basic scraping tool to gather articles from websites
2. Save the article texts into an SQL database
3. Analyze the articles for political standpoints
4. Determine political standpoint of article creators and sources
5. Automate the data gathering and saving process

## Tools
* selenium wedriver (data gathering)
* psycopg2 (data base)

## Database
#### article_data
article_ID (PK, serial),
source_ID (Int, not null),
author_ID (Int),
author_name (Varchar),
article_title (Varchar),
article_text (Text),
dl_timestamp (Date, not null),
economic_score (Smallint),
social_freedom_score (Smallint)
#### source_data
source_ID (PK, serial),
source_name (Varchar),
source_page (Varchar, unique),
econimic_score_av (Smallint),
social_score_av (Smallint),
trust_score_av (Smallint)
#### author_data
author_ID (PK, serial),
author_name (Varchar, unique),
aliases (Varchar),
economic_score_av (Smallint),
social_freedom_score_av (Smallint),
trust_score_av (Smallint)