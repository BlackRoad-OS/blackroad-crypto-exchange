#!/usr/bin/env python3
"""BlackRoad Crypto Exchange — order book simulation and price feed."""
import json, urllib.request, time, collections

class OrderBook:
    def __init__(self, pair: str = "BTC/USD"):
        self.pair = pair
        self.bids: list[tuple[float,float]] = []  # (price, size)
        self.asks: list[tuple[float,float]] = []

    def add_bid(self, price: float, size: float):
        self.bids.append((price, size))
        self.bids.sort(reverse=True)  # highest first

    def add_ask(self, price: float, size: float):
        self.asks.append((price, size))
        self.asks.sort()  # lowest first

    def best_bid(self) -> float: return self.bids[0][0] if self.bids else 0
    def best_ask(self) -> float: return self.asks[0][0] if self.asks else 0
    def spread(self) -> float: return self.best_ask() - self.best_bid()

    def display(self):
        print(f"\\n📊 Order Book: {self.pair}\\n")
        print("  ASKS (lowest first):")
        for p, s in self.asks[:5]: print(f"    ${p:>12,.2f}  {s:>8.4f}")
        print(f"  {─*30}")
        print(f"  Spread: ${self.spread():,.2f}")
        print(f"  {─*30}")
        print("  BIDS (highest first):")
        for p, s in self.bids[:5]: print(f"    ${p:>12,.2f}  {s:>8.4f}")

def get_btc_price() -> float:
    try:
        with urllib.request.urlopen("https://blockstream.info/api/fee-estimates", timeout=5) as r:
            pass
    except: pass
    try:
        with urllib.request.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=5) as r:
            d = json.loads(r.read())
            return float(d["bpi"]["USD"]["rate"].replace(",",""))
    except: return 0.0

if __name__ == "__main__":
    import random
    mid = get_btc_price() or 95000.0
    book = OrderBook("BTC/USD")
    for i in range(10):
        spread = random.uniform(10, 50)
        book.add_bid(mid - spread - i*20, random.uniform(0.01, 0.5))
        book.add_ask(mid + spread + i*20, random.uniform(0.01, 0.5))
    book.display()

