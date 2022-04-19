import math, random, csv, os
from scipy import stats
from scipy.stats import norm
# from numpy import array
import pandas as pd

# list of # moves post-earnings of stock
# moves = [10.47,1.61,2.09,2.26,2.04,4.91,6.83,6.63,5.89,4.42,4.34,2.61,4.73,0.31,6.1,2.25,6.5,6.26,6.57,4.12,4.23,1.58,5.65,2.72,2.61,8.2,7.99,2.49,5.14,0.16,12.35,0.91,4.32,8.87,6.24,5.59,2.67,2.42,0.53,2.68,0.93,5.98,1.41,4.69];   # AAPL
moves = [0];

# sizing of trades
# sizing = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
sizing = [10, 100];

def main():
    stock = input("Stock ticker: ");
    capital = float(input("Starting capital: "));
    iCapital = capital;
    s = float(input("Stock spot price: "));
    r = float(input("Risk free rate (%): "));
    r = r/100;
    vol = float(input("Volatility post earnings (%): "));
    vol = vol/100;

    # ask how many contracts user is opening
    cLong = int(input("Number of long call contracts opening: "));
    pLong = int(input("Number of long put contracts opening: "));
    cShort = int(input("Number of short call contracts opening: "));
    pShort = int(input("Number of short put contracts opening: "));
    premium = float(input("Premium received (-paid): "));   # can be negative
    maxLoss = float(input("Max loss based on trade structure (enter as positive number): "));
    # portfolio = [[] for i in range(len(sizing))];
    portfolio = [];

    # lists to holds strikes and days to expiry of call and put contracts
    clk, clt = ([] * cLong for i in range(2));      # call long strike, call long time to expiry
    csk, cst = ([] * cShort for i in range(2));     # call short strike, call short time to expiry
    plk, plt = ([] * pLong for i in range(2));      # put long strike, put long time to expiry
    psk, pst = ([] * pShort for i in range(2));     # put short strike, put short time to expiry

    # set up trade structure
    # for each long call contract, enter strike and days to expiry
    for i in range(cLong):     
        clk.append(float(input("Long call #" + str(i+1) + " strike price: ")));
        clt.append(float(input("Long call #" + str(i+1) + " days to expiry: ")));

    # for each long put contract, enter strike and days to expiry
    for i in range(pLong):
        plk.append(float(input("Long put #" + str(i+1) + " strike price: ")));
        plt.append(float(input("Long put #" + str(i+1) + " days to expiry: ")));

    # for each short call contract, enter strike and days to expiry
    for i in range(cShort):
        csk.append(float(input("Short call #" + str(i+1) + " strike price: ")));
        cst.append(float(input("Short call #" + str(i+1) + " days to expiry: ")));

    # for each short put contract, enter strike and days to expiry
    for i in range(pShort):
        psk.append(float(input("Short put #" + str(i+1) + " strike price: ")));
        pst.append(float(input("Short put #" + str(i+1) + " days to expiry: ")));

    # for loop iterating x (eg. 1000) times for Monte Carlo simulation
    # randomize stock price based on historical movements and calculate payout of each contract and net it to capital
    iterations = int(input("Iterations to run per sizing: "));

    # trade sizing
    for k in range(len(sizing)):
        sizeIteration = [];    
        for i in range(iterations):
            # size is adjusted for each iteration
            size = capital * sizing[k]/100;
            # n = number of contracts for this iteration
            n = math.floor(size/maxLoss);

            # apply premium for each iteration and multiply by number of contracts for that iteration
            capital += n * premium;
            print("capital: " + str(capital));
            profit = 0;

            # randomize stock price post earnings movement
            post = s * (1 + random.choice(moves)/100);

            # close open long call contracts
            for j in range(cLong):
                profit += n * call(post, clk[j], r, clt[j]/365, vol);

            # close open short call contracts
            for j in range(cShort):
                profit -= n * call(post, csk[j], r, cst[j]/365, vol);

            # close open long put contracts
            for j in range(pLong):
                profit += n * put(post, plk[j], r, plt[j]/365, vol);

            # close open short put contracts
            for j in range(pShort):
                profit -= n * put(post, psk[j], r, pst[j]/365, vol);

            print("profit: " + str(profit));
            capital += profit;
            print("capital after profits: " + str(capital));
            # portfolio.append(capital);
            sizeIteration.append(capital);

        print(sizeIteration);

        # reset capital after all iterations are complete for a particular trade sizing simulation run
        capital = iCapital;

        # starting new row in 2D array to represent next iteration with different trade sizing
        # portfolio.append([capital])
        portfolio.append(sizeIteration);


    # print(portfolio[0][0]);
    print(portfolio);

    # print portfolio array to check if accurate
    # for i in range(len(portfolio)):
    #     for j in range(len(portfolio[i])):
    #         print(portfolio[i][j]);

    fileName = stock + ".csv";
    filedir = os.path.join(os.path.dirname(__file__), '..', 'Exports', 'Earnings - Kelly', fileName);

    for i in range(len(sizing)):
        sizing[i] = str(sizing[i]) + "%";

    # convert sizing list to dataframe
    sizingDF = pd.DataFrame(sizing);
    
    # convert portfolio list to dataframe
    portfolioDF = pd.DataFrame(portfolio);
    # portfolioDF.T.to_csv(filedir);

    # write header
    # with open(filedir, 'w') as f:
    #     writer = csv.writer(f);
    #     writer.writerow(sizing);

    sizingDF.T.to_csv(filedir, index = False, header = False);
    portfolioDF.T.to_csv(filedir, mode = 'a', index = False, header = False);

    # write data
    # with open(filedir, 'a') as f:
    #     writer = csv.writer(f);
    #     for i in range(iterations):
    #         # f.write('\n');        # works, but unneeded as already goes to new row
    #         writer.writerow(sizing);
    #         # writer.writerow('\n');
    #         for j in range(len(sizing)):
    #             writer.writerow(portfolio[j][i]);       # error: _csv.Error: iterable expected, not numpy.float64

        # writer.writerow(sizing);

    # print(capital);

    # make a list of movements to graph and export to csv


def call (s, k, r, t, vol):    
    d1 = (math.log(s/k) + (r + (vol**2)/2) * t) / (vol * math.sqrt(t));
    d2 = d1 - vol * math.sqrt(t);
    c = norm.cdf(d1) * s - norm.cdf(d2) * k * math.exp(-r*t);
    # print(c);
    return c * 100;

def put (s, k, r, t, vol):
    d1 = (math.log(s/k) + (r + (vol**2)/2) * t) / (vol * math.sqrt(t));
    d2 = d1 - vol * math.sqrt(t);
    p = norm.cdf(-d2) * k * math.exp(-r*t) - norm.cdf(-d1) * s;
    # print(p);
    return p * 100;

main();