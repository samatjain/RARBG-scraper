DATE="2023-May-30"
poetry run scrapy crawl rarbg -a search_term="MP3-daily-$DATE"
poetry run scrapy crawl rarbg -a search_term="FLAC-daily-$DATE"
mv "MP3-daily-$DATE.auto.csv" 2023
mv "FLAC-daily-$DATE.auto.csv" 2023
python3 last_field.py "2023/MP3-daily-$DATE.auto.csv" | ssh rsstorrent@ba.local "cat > /archive/torrents/MP3-daily/01-hot/MP3-daily-$DATE.txt"
python3 last_field.py "2023/FLAC-daily-$DATE.auto.csv" | ssh rsstorrent@ba.local "cat > /archive/torrents/MP3-daily/01-hot/FLAC-daily-$DATE.txt"
