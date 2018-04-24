import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
stocks = ['KWEB', 'QQQ', 'ARKW', 'BABA','SHOP','NVDA','V','FB','ATVI','LRCX','AMAT','MU','AAPL','AMD']
stocks=[]

correct=0
while correct==0:
    n = int(input("Enter the NUMBER OF STOCKS and press enter \n"))
    stocks=[]
    for i in range(0,n):
        stock_i=str((raw_input("enter stock "+str(i+1)+" of "+str(n)+" ")))
        #stock_i=raw_input("Please enter a number:")
        print (stock_i)
        stocks.append(str(stock_i))
    correct=int(input("press 0 if you entered something wrong and want to restart or else press 1 \n"))


num_iter=int(input("enter the number of stock simulations \n"))
def calculate(num_port=5000):
    #my_weights = np.asarray([0.0515, 0.0638, 0.1077, 0.0394, .1065, .0791, .0701, .0376, .0565, .0391, .0106, .0320, .1008, 0])
    #my_weights=my_weights*100
    #a=zip(stocks,my_weights)
    #portfolio=sorted(a, key=lambda a_entry: a_entry[0])
    stocks.sort()
    data=web.DataReader(stocks[0], data_source='iex', start='01/01/2015').close
    for i in range(1, len(stocks)):
        data = pd.concat([data, web.DataReader(stocks[i], data_source='iex', start='01/01/2015').close], axis=1)

    #data = web.DataReader(stocks, data_source='iex', start='01/01/2015')['close']


    returns = data.pct_change()


    mean_daily_returns = returns.mean()
    cov_matrix = returns.cov()


    my_weights = np.asarray([0.0515, 0.0638, 0.1077, 0.0394,.1065,.0791,.0701,.0376,.0565,.0391,.0106,.0320,.1008,0])
    my_weights=my_weights*100
    num_portfolios = num_port


    results = np.zeros((4 + len(stocks) - 1, num_portfolios))

    for i in xrange(num_portfolios):

        weights = np.array(np.random.random(len(stocks)))

        weights /= np.sum(weights)


        portfolio_return = np.sum(mean_daily_returns * weights) * 252
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)


        results[0, i] = portfolio_return
        results[1, i] = portfolio_std_dev

        results[2, i] = results[0, i] / results[1, i]
        # iterate through the weight vector and add data to results array
        for j in range(len(weights)):
            results[j + 3, i] = weights[j]

    name=['ret', 'stdev', 'sharpe']
    for i in stocks:
        name.append(i)
    results_frame = pd.DataFrame(results.T, columns=name)


    max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]

    min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]

    return(max_sharpe_port)
#plt.scatter(results_frame.stdev, results_frame.ret, c=results_frame.sharpe, cmap='RdYlBu')
#plt.xlabel('Volatility')
#plt.ylabel('Returns')
#plt.colorbar()
#iteration=[5000,10000,15000]
#for i in iteration:
#    new = calculate(i)
#    if i!= iteration[0]:

#        diff= prev-new
#    prev=new


max_sharpe_port=calculate(num_iter)
#plt.scatter(max_sharpe_port[1], max_sharpe_port[0], marker=(5, 1, 0), color='r', s=100)

#plt.scatter(min_vol_port[1], min_vol_port[0], marker=(5, 1, 0), color='g', s=100)
#print(max_sharpe_port)
percentage = max_sharpe_port.as_matrix()[3:]*100
#print percentage
#print max_sharpe_port.as_matrix()[0:]
ind = np.arange(len(stocks))
width = 0.35
print (max_sharpe_port)
fig, ax = plt.subplots(figsize=(6,6))
ax.annotate('Return = '+str(np.round(max_sharpe_port[0]*100,2))+"%"+'\nStd dev = '+str(np.round(max_sharpe_port[1],2))+'\nSharpe = '+str(np.round(max_sharpe_port[2],2)), (-.1, 1.01), textcoords='axes fraction', size=10)
ax.pie(percentage, labels=stocks, autopct='%1.1f%%')
plt.savefig('Portfolio.png', bbox_inches='tight')
plt.show()
# rects1 = ax.bar(ind, percentage, width, color='r')
# rects2 = ax.bar(ind+width, zip(*portfolio)[1], width, color='y')
# ax.set_ylabel('percentage')
# ax.set_title('perotfolio analysis')
# ax.set_xticks(ind + width / 2)
# ax.set_xticklabels((stocks))
# ax.legend((rects1[0], rects2[0]), ('calculated', 'actual'))
# def autolabel(rects):
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                 '%d' % int(height),
#                 ha='center', va='bottom')
#
# autolabel(rects1)
# autolabel(rects2)



#print "\n".join(str(x) for x in my_weights)