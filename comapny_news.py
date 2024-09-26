import yfinance as yf

def get_additional_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    
    sustainability = ticker.sustainability
    institutional_holders = ticker.institutional_holders
    mutualfund_holders = ticker.mutualfund_holders
    news = ticker.news
    calendar = ticker.calendar
    actions = ticker.actions
    history = ticker.history(period="1mo")
    major_holders = ticker.major_holders
    
    return sustainability, institutional_holders, mutualfund_holders, news, calendar, actions, history, major_holders

_,_,_,news,_,_,_,_ = get_additional_data('TITAN.NS')
print(news)