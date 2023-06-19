import requests
from bs4 import BeautifulSoup
import alpaca_trade_api as tradeapi
import config

api = tradeapi.REST(key_id= config.PUB_KEY, secret_key=config.SEC_KEY, base_url=config.BASE_URL) # For real trading, don't enter a base_url

def getLastUsed():
    with open("lastUsed.txt","r") as reader:
        return reader.read()

def updateLastUsed(r):
    with open("lastUsed.txt", "w") as writer:
        return writer.write(r)

def main():
    lastUsedRow = getLastUsed()
    page = requests.get(config.POL_URL)

    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.select("table.q-table.trades-table-embedded.skip-politician tbody")[0]
    
    rows = table.find_all("tr")
    for i, row in enumerate(rows):
        if row.text == lastUsedRow:
            rows = rows[:i]
            break

    # TODO: do actual share stuff
    for row in rows:
        # print(row.prettify())
        print(row.select('span.q-field.issuer-ticker')[0].text)
        print(row.select('span.q-field.tx-type')[0].text)
#         api.submit_order(
#             symbol=row.find('span.q-field.issuer-ticker').text, # Replace with the ticker of the stock you want to buy
#             qty=1,
#             side=row.find('span.q-field.tx-type').text,
#             type='market', 
#             time_in_force='gtc' # Good 'til cancelled
# )

    if rows:
        updateLastUsed(rows[0].text)

main()