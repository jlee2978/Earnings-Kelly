import math
from scipy import stats
from scipy.stats import norm
# from numpy import array
import random

# list of # moves post-earnings of stock
moves = [10.47,1.61,2.09,2.26,2.04,4.91,6.83,6.63,5.89,4.42,4.34,2.61,4.73,0.31,6.1,2.25,6.5,6.26,6.57,4.12,4.23,1.58,5.65,2.72,2.61,8.2,7.99,2.49,5.14,0.16,12.35,0.91,4.32,8.87,6.24,5.59,2.67,2.42,0.53,2.68,0.93,5.98,1.41,4.69];   # AAPL

# sizing of trades
sizing = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

def main():
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
    portfolio = [[] for i in range(len(sizing))];

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
        for i in range(iterations):
            # size is adjusted for each iteration
            size = capital * sizing[k]/100;
            # n = number of contracts for this iteration
            n = math.floor(size/maxLoss);

            # apply premium for each iteration
            # capital += premium * n;       # n = number of contracts = (iCapital * sizing/100)/maxLoss
            capital += n * premium;
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

            capital += profit;
            portfolio.append(capital);

        # reset capital after all iterations are complete for a particular trade sizing simulation run
        capital = iCapital;

        # starting new row in 2D array to represent next iteration with different trade sizing
        portfolio.append([capital])


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