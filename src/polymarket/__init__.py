"""Polymarket paper-trading strategies for Aurora Trader.

Paper mode only: nothing in this package places real orders or moves funds.
Pipeline: scan -> estimate probability -> net-edge filter -> fractional Kelly
-> risk veto -> simulated fill.
"""
