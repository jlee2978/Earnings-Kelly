import math
from scipy import stats
from scipy.stats import norm
# from numpy import array

def main():
    capital = float(input("Starting capital: "));
    s = float(input("Stock spot price: "));

    # ask how many contracts user is opening
    c = int(input("Number of call contracts opening: "));
    p = int(input("Number of put contracts opening: "));
    premium = float(input("Premium received (-paid): "));   # can be negative
    capital += premium;

    # lists to holds strikes and days to expiry of call and put contracts
    ck, ct, pk, pt = [];

    # for each call contract, enter strike and days to expiry
    for i in range(c):
        ck[i] = float(input("Strike price: "));
        ct[i] = float(input("Days to expiry: "));

    # for each put contract, enter strike and days to expiry
    for i in range(p):
        pk[i] = float(input("Strike price: "));
        pt[i] = float(input("Days to expiry: "));

    # for loop iterating X (eg. 1000) times for Monte Carlo simulation
    # randomize stock price based on historical movements and calculate payout of each contract and net it to capital
    iterations = int(input("Iterations to run: "));
    
    for i in range(iterations):
        # randomize stock price post earnings movement
        # close open call contracts




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

# unused
def cdf(d):
    # to fix
    # N = math.erf(d / math.sqrt(2.0));
    # return (1 + erf(d / sqrt(2.0))) / 2.0;
    return stats.norm.cdf(d);
    # return N;

main();