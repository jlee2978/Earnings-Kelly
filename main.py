import math
from scipy import stats
from scipy.stats import norm
# from numpy import array

def main():
    capital = float(input("Starting capital: "));
    s = float(input("Stock spot price: "));
    r = float(input("Risk free rate (%): "));
    r = r/100;
    vol = float(input("Volatility post earnings (%): "));

    # ask how many contracts user is opening
    cLong = int(input("Number of long call contracts opening: "));
    pLong = int(input("Number of long put contracts opening: "));
    cShort = int(input("Number of short call contracts opening: "));
    pShort = int(input("Number of short put contracts opening: "));
    premium = float(input("Premium received (-paid): "));   # can be negative
    capital += premium;

    # lists to holds strikes and days to expiry of call and put contracts
    clk, clt, csk, cst = [];
    plk, plt, psk, pst = [];

    # for each long call contract, enter strike and days to expiry
    for i in range(cLong):
        clk[i] = float(input("Long call #" + i + " strike price: "));
        clt[i] = float(input("Long call #" + i + " days to expiry: "));

    # for each long put contract, enter strike and days to expiry
    for i in range(pLong):
        plk[i] = float(input("Long put #" + i + " strike price: "));
        plt[i] = float(input("Long put #" + i + " days to expiry: "));

    # for each short call contract, enter strike and days to expiry
    for i in range(cShort):
        csk[i] = float(input("Short call #" + i + " strike price: "));
        cst[i] = float(input("Short call #" + i + " days to expiry: "));

    # for each short put contract, enter strike and days to expiry
    for i in range(pShort):
        psk[i] = float(input("Short put #" + i + " strike price: "));
        pst[i] = float(input("Short put #" + i + " days to expiry: "));

    # for loop iterating X (eg. 1000) times for Monte Carlo simulation
    # randomize stock price based on historical movements and calculate payout of each contract and net it to capital
    iterations = int(input("Iterations to run: "));

    for i in range(iterations):
        profit = 0;
        # randomize stock price post earnings movement
        # setting s to 100 for now, to randomize later (eg. s * randomized historical move %)
        s = 100;

        # close open long call contracts
        for j in range(cLong):
            profit += call(s, clk[j], r, clt[j], vol);

        # close open short call contracts
        for j in range(cShort):
            profit -= call(s, csk[j], r, cst[j], vol);

        # close open long put contracts
        for j in range(pLong):
            profit += put(s, plk[j], r, plt[j], vol);

        # close open short put contracts
        for j in range(pShort):
            profit -= put(s, psk[j], r, pst[j], vol);

        capital += profit;

    # append all profits to capital to make a list of movements to graph

    print(capital);

    # TESTING BSM MODEL BELOW

    # s = stock price, k = strike price, r = interest rate in %, t = years to expiry, vol annual volatility in %    
    s = float(input("Stock spot price: "));
    k = float(input("Strike price: "));
    r = float(input("Risk free rate (%): "));
    t = float(input("Days to expiry: "));
    vol = float(input("Volatility (%): "));

    # call(s, k, r/100, t/365, vol/100);
    # put(s, k, r/100, t/365, vol/100);

def call (s, k, r, t, vol):    
    d1 = (math.log(s/k) + (r + (vol**2)/2) * t) / (vol * math.sqrt(t));
    d2 = d1 - vol * math.sqrt(t);
    c = norm.cdf(d1) * s - norm.cdf(d2) * k * math.exp(-r*t);
    print(c);
    return c;

def put (s, k, r, t, vol):
    d1 = (math.log(s/k) + (r + (vol**2)/2) * t) / (vol * math.sqrt(t));
    d2 = d1 - vol * math.sqrt(t);
    p = norm.cdf(-d2) * k * math.exp(-r*t) - norm.cdf(-d1) * s;
    print(p);
    return p;

main();