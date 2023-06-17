from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2021, 4, 20)
end_date = date(2022, 1, 1)

cmds = []
for single_date in daterange(start_date, end_date):
    # MP3-daily-2019-January-26
    date_str = single_date.strftime("%Y-%B-%d")
    cmd = f"poetry run scrapy crawl rarbg -a search_term=MP3-daily-{date_str}"
    cmds.append(cmd)
print(' && sleep 5m && \\\n'.join(cmds))

