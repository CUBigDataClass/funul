import math
from yahoo_finance import Share

kindex_number_of_shares = 0
kindex_avg_price_per_share = 1
'''
manages a dict named port
port is a dict of one key matched with a tupla of ()
In the tuple the kindex_number_of_shares index matches to the index where the number of shares are stored
the kindex_ave_price_per_share matches to the index where the average price per share is
Right now short selling is allowed to infinity and BuyStock/SellStock can take the oppisite signs which would be equavialant to the opposite with not control on how much you can
    neg sell meaning buy. I.e. you can buy beyond the capital limit with short selling number_of_share below zero

'''
def portfolio(capital):
    cur_capital = capital
    start_capital = capital
    portfol = {}
    def _portfolio():
        return 1
    def get_number_of_shares(name_of_stock):
        return portfol[name_of_stock][kindex_number_of_shares]
    def get_weight_of_shares_in_port(name_of_stock):
        port_worth = get_port_worth()
        stock = Share(name_of_stock)
        return stock.get_price() / stock
    def get_stock_price(name_of_stock):
        stock = Share(name_of_stock)
        return stock.get_price()
    def BuyStock(name_of_stock, number_of_shares):
        stock = Share(name_of_stock)
        total_exp = stock.get_price() * number_of_shares
        if total_exp > cur_capital:
            number_of_shares = math.floor(cur_capital/stock.get_price())
            total_exp = stock.get_price() * number_of_shares
            if number_of_shares == 0:
                return 0
        if name_of_stock in portfol:
            total_number_of_shares_owned = portfol[name_of_stock][kindex_number_of_shares] + number_of_shares
            portfol[name_of_stock][kindex_avg_price_per_share] = (portfol[name_of_stock][kindex_avg_price_per_share] * portfol[name_of_stock][kindex_number_of_shares] + stock,get_price() * number_of_shares) / total_number_of_shares_owned
            portfol[name_of_stock][kindex_number_of_shares] = total_number_of_shares_owned
        else:
            portfol[name_of_stock] = (0.0,0.0)
            portfol[name_of_stock][kindex_number_of_shares] = number_of_shares
            portfol[name_of_stock][kindex_avg_price_per_share] = stock.get_price()
        cur_capital = cur_capital - total_exp
        return(portfol, cur_capital)
    def SellStock(name_of_stock, number_of_shares):
        stock = Share(name_of_stock)
        if name_of_stock in portfol:
            portfol[name_of_stock] = (0.0,0.0)
            portfol[name_of_stock][kindex_number_of_shares] = -number_of_shares
            portfol[name_of_stock][kindex_avg_price_per_share] = -stock.get_price()
        else:
            total_number_of_shares_owned = portfol[name_of_stock][kindex_number_of_shares] - number_of_shares
            portfol[name_of_stock][kindex_avg_price_per_share] = (portfol[name_of_stock][kindex_avg_price_per_share] * portfol[name_of_stock][kindex_number_of_shares] - stock,get_price() * number_of_shares) / total_number_of_shares_owned
            portfol[name_of_stock][kindex_number_of_shares] = total_number_of_shares_owned
        cur_capital = cur_capital + number_of_shares * stock.get_price()
        return(portfol, cur_capital)
    def get_port_worth():
        cur_value_of_port = 0.0
        for key in portfol:
            stock = Share(key)
            cur_value_of_port += portfol[key][kindex_number_of_shares] * stock.get_price()
        return cur_value_of_port + cur_capital

