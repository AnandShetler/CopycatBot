from bs4 import BeautifulSoup
import config
import utilities
import datetime
import math
import yfinance as yf

START_DATE = None # TODO: limit test data to trades from START_DATE to END_DATE
END_DATE = None


def main():
    money_spent = 0
    money_earned_selling = 0
    transactions = [] # [ticker, buy/sell, date, quantity, price]
    portfolio = dict() # ticker: quantity
    money_spent_pol = 0
    money_earned_selling_pol = 0
    transactions_pol = []
    portfolio_pol = dict()

    for i in range(utilities.getNumPages(),0,-1):
        # print(config.POL_URL+"&page="+str(i))
        soup = utilities.getSoup(config.POL_URL+"&page="+str(i))
        table = soup.select("div.q-table-wrapper > div.trades-table-scroll-wrapper > table > tbody")[0]
        rows = table.find_all("tr")
        rows.reverse()
        for row in rows:
            try:
                ticker = row.select('span.q-field.issuer-ticker')[0].text
                if ticker == "N/A":
                    continue
                ticker = ticker[:ticker.find(':')].replace("/","-")
                buy_sell = row.select('span.tx-type')[0].text
                date_string = row.select(".pub-date .q-value")[0].text.replace("Sept","Sep") + " " + row.select(".pub-date .q-label")[0].text
                pub_date = datetime.datetime.strptime(date_string, " %d %b %Y")
                pub_date_inc = pub_date + datetime.timedelta(days=5)
                real_date_string = row.select(".tx-date .q-value")[0].text + " " + row.select(".tx-date .q-label")[0].text
                real_date = datetime.datetime.strptime(real_date_string, " %d %b %Y")
                real_price = float(row.select('td.q-td.q-column--price > div > span')[0].text.replace(",",""))
                quantity = row.select('.q-column--value > div > div > span > div > span')[0].text
                if 'K' in quantity:
                    quantity = math.ceil(int(quantity[:quantity.find('K')])*1000 / real_price)
                else:
                    quantity = math.ceil(int(quantity[:quantity.find('M')])*1000000 / real_price)
                
                # print(ticker,pub_date.strftime("%Y-%m-%d"),pub_date_inc.strftime("%Y-%m-%d"))
                data = yf.download(ticker, pub_date.strftime("%Y-%m-%d"), pub_date_inc.strftime("%Y-%m-%d"))
                
                if (len(data.index) == 0):
                    print("No data found for",ticker)
                else:
                    open_price = data['Open'][0]
                    if buy_sell == 'buy':
                        # update my values
                        money_spent += quantity * open_price
                        transactions.append([ticker, buy_sell, datetime.date.today(), quantity, open_price])
                        if ticker in portfolio.keys():
                            portfolio[ticker] += quantity
                        else:
                            portfolio[ticker] = quantity
                        # update politician values
                        money_spent_pol += quantity * real_price
                        transactions_pol.append([ticker, buy_sell, real_date, quantity, real_price])
                        if ticker in portfolio_pol.keys():
                            portfolio_pol[ticker] += quantity
                        else:
                            portfolio_pol[ticker] = quantity
                    elif buy_sell == 'sell' and ticker in portfolio.keys():
                        # update my values
                        quantity_to_sell = min(quantity, portfolio[ticker])
                        money_earned_selling += quantity_to_sell * open_price
                        portfolio[ticker] -= quantity_to_sell
                        transactions.append([ticker, buy_sell, datetime.date.today(), quantity, open_price])
                        # update politician values
                        money_earned_selling_pol += quantity_to_sell * real_price
                        portfolio_pol[ticker] -= quantity_to_sell
                        transactions_pol.append([ticker, buy_sell, real_date, quantity, real_price])
            except:
                print("oops")

    portfolio_value = get_portfolio_value(portfolio, datetime.date.today())
    portfolio_value_pol = get_portfolio_value(portfolio_pol, datetime.date.today())
    print("---------BOT STATS---------")
    print("Portfolio:")
    print("Money Spent: $" + str(money_spent))
    print("Money Earned Selling: $" + str(money_earned_selling))
    print("Current Portfolio Value: $" + str(portfolio_value))

    print("\n---------POL STATS---------")
    print("Portfolio:")
    print("Money Spent: $" + str(money_spent_pol))
    print("Money Earned Selling: $" + str(money_earned_selling_pol))
    print("Current Portfolio Value: $" + str(portfolio_value_pol))

def get_portfolio_value(portfolio, date):
    value = 0
    date_inc = date + datetime.timedelta(days=5)
    for ticker, quantity in portfolio.items():
        data = yf.download(ticker, date.strftime("%Y-%m-%d"), date_inc.strftime("%Y-%m-%d"))
        if len(data.index) > 0:
            value += float(data['Open'][0])
        else:
            print(ticker, 'not found for given date')
    return value

main()
