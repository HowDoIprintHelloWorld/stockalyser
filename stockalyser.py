import yfinance as yf
from sys import argv, exit
import pandas
import time
from progress.bar import Bar

DEVMODE = False

def validatefile():
  try:
    with open("stocks.txt", "r"):
      pass
  except FileNotFoundError:
    print("[!] File 'stocks.txt' does not exist or can not be opened")
    exit(1)

def getdata(stock, period):
  stock, pricesstring = yf.Ticker(stock), stock
  for price in list(stock.history(period="30d")["Close"].values):
    pricesstring += " "+str(round(price, 3))
  if DEVMODE:
    pricesstring += " 32984902384"
  return pricesstring


def getstonks():
  validatefile()
  stocks = []

  with open("stocks.txt", "r") as stocksfile:
    for count, _ in enumerate(stocksfile):
        pass
    count += 1
    print(count)
    bar = Bar(f'Fetching stocks for {str(count)} companies', max=count)
    for line in stocksfile:
      if line:
        stocks.append(getdata(line.strip().upper(), "30d"))
      bar.next()
    bar.finish
    print("")
  with open("stocksdata.txt", "r") as stocksdatafile:
    try: 
      currentpercent = stocksdatafile.readline().split()[-1]
    except IndexError:
      print("[!] Something went wrong. Please run 'python3 stockalyser.py regen'")
      exit(1)
  with open("stocksdata.txt", "w") as stocksdatafile:
    if ":" in currentpercent:
      print("[!] Please regen and supply a percentage in 'stocksdata.txt' in line 1")
    else:
      stocksdatafile.write(str(time.time())+f" current and average difference in percent: {currentpercent}\n")
      for pricesstring in stocks:
        stocksdatafile.write(pricesstring+"\n")
  print("[D] Done updating scuffed database")

def getaverage(pricelist):
  avg = 0
  for price in pricelist:
    avg += float(price)
  return avg / len(pricelist)

def computediffs():
  begun, diff = False, 0
  with open("stocksdata.txt", "r") as stocksdatafile:
    for line in stocksdatafile:
      if begun:
        pricelist = line.split()[1:]
        development = float(pricelist[-1]) / getaverage(pricelist[:-1])
        if development > 1 + diff or development < 1 - diff:
          print(f"\n[!!!!!] Found a sussy stock:\n{line.split()[0]} has had a {round(development, 2)}% change in the last day!\n")
      else:
        diff = line.split()[-1]
        if diff[-1] == "%":
          diff = diff[:-1]
        try:
          diff = int(diff) / 100
          begun = True
        except Exception:
          print("[!] Please supply a percentage in 'stocksdata.txt' in line 1")
  print("[D] Done computing any irregularities")
  
def regen():
  with open("stocksdata.txt", "w") as file:
    file.write(str(time.time())+f" current and average difference in percent: {input('Percentage threshold: ')}\n")
  if input("[?] Remake 'stocks.txt' as well? This will wipe everything currently written there... [y/n]:   ").lower().strip() == "y":
    with open("stocks.txt", "w") as file:
      file.write("")
  print("[D] Done regenerating")

if __name__ == "__main__":
  funcd = {"update":getstonks, "calculate":computediffs, "regen":regen}
  funcl = [option for option, func in funcd.items()]
  try: 
    if argv[1] in funcl:
      funcd[argv[1]]()
      exit(0)
  except IndexError:
    pass
  print("[!] Usage: python3 stockalyser.py [update/calculate/regen]")
  exit(1)
