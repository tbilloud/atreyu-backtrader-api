import backtrader as bt
import math


# Sizer to go all in with forex trading with EUR.XXX pairs
# My base account currency is EUR
# Thus, I sell EUR and buy USD
# TODO: commissions lead to negative cash balances. I need to anticipate them somehow to avoid order rejections...
# TODO: the commission is 2 USD with IB below 20K USD.

class AllInSizerInt_FX_IB(bt.Sizer):
    params = (
        ('base_currency', 'EUR'),
    )

    def _getsizing(self, comminfo, cash, data, isbuy):
        cash_balances = self.broker.ib.get_acc_cash_fx()
        if isbuy:
            size = cash_balances['USD']
            size = math.floor(size * 10) / 10  # truncate to lower 0.1 digit
            size = size - 2  # anticipate commission to avoid negative cash values
            print('_getsizing / buy /', size, 'USD', cash_balances)
        else:
            if cash_balances['EUR'] > 1.8:
                size = cash_balances['EUR'] - 1.8  # the commission given by IB is 2 USD (not 2 EUR)
                size = math.floor(size)  # TODO: IB API rejects 'fractional sell', although TWS does not!
                print('_getsizing / sell /', size, 'EUR', cash_balances)
            else:
                print('ERROR: trying to sell more EUR than I have')
        return size
