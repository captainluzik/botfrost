"""
    Class for working with PerfectMoney API
"""
import urllib.request
import hashlib
import re

BASE_URL = 'https://perfectmoney.is/acct/{0}.asp?AccountID={1}&PassPhrase={2}&{3}'


class PerfectMoney:
    """
        API functions class
    """

    def __init__(self, account, passwd):
        """
            Initialise internal parameters
        """
        self.__account = account
        self.__passwd = passwd
        self.__error_re = re.compile("<input name='ERROR' type='hidden' value='(.*)'>")
        self.__value_re = re.compile("<input name='(.*)' type='hidden' value='(.*)'>")
        self.error = None

    def _fetch(self, url, params):
        """
           internal URL fetch function
        """
        res = None
        try:
            response = urllib.request.urlopen(url)
        except:
            self.error = 'API request failed'
            return None
        if response:
            res = response.read().decode('utf-8')
        return res

    def _get_dict(self, string):
        """
            response to dictionary parser
        """
        rdict = {}
        if not string:
            return {}
        match = self.__error_re.search(string)
        if match:
            self.error = match.group(1)
            return rdict
        for match in self.__value_re.finditer(string):
            rdict[match.group(1)] = match.group(2)
        return rdict

    def _get_list(self, string):
        """
            response to list parser, removes CSV list headers
        """

        def f(x):
            return x != '' and \
                   x != 'Created,e-Voucher number,Activation code,Currency,Batch,Payer Account,Payee Account,Activated,Amount' and \
                   x != 'Time,Type,Batch,Currency,Amount,Fee,Payer Account,Payee Account,Payment ID,Memo'

        if not string:
            return []
        rlist = string.split('\n')
        return list(filter(f, rlist))

    def balance(self):
        """
            Get account balance
            return: dictionary of account balances
            example:
                {
                    'E16123123': '0.00',
                    'G15123123': '0.00',
                    'U11231233': '190.00'}
                }
        """
        url = BASE_URL.format('balance', self.__account, self.__passwd, '')
        res = self._fetch(url, None)
        return self._get_dict(res)

    def history(self, startmonth, startday, startyear, endmonth, endday, endyear):
        """
            Transaction history
            return: list of transactions in CSV format
        """
        params = {
            'startmonth': startmonth,
            'startday': startday,
            'startyear': startyear,
            'endmonth': endmonth,
            'endday': endday,
            'endyear': endyear
        }
        url = BASE_URL.format('historycsv', self.__account, self.__passwd,
                              "&".join(["{0}={1}".format(key, str(value)) for key, value in params.items()]))
        res = self._fetch(url, None)
        return self._get_list(res)

    def transfer(self, payer, payee, amount, memo, payment_id):
        """
            Money transfer
            return: dictionary
            example:
                {
                  'PAYMENT_ID': '123',
                  'Payer_Account': 'U1911111',
                  'PAYMENT_AMOUNT': '0.01',
                  'PAYMENT_BATCH_NUM': '1166150',
                  'Payee_Account': 'U11232323'
                }
        """
        params = {
            'AccountID': self.__account,
            'PassPhrase': self.__passwd,
            'Payer_Account': payer,
            'Payee_Account': payee,
            'Amount': amount,
            'Memo': memo,
            'PAY_IN': 1,
            'PAYMENT_ID': payment_id
        }
        url = BASE_URL.format('confirm', self.__account, self.__passwd,
                              "&".join(["{0}={1}".format(key, str(value)) for key, value in params.items()]))
        res = self._fetch(url, None)
        return self._get_dict(res)

    def ev_create(self, payer, amount):
        """
            Create e-Voucher
            return: dictionary
            example:
                {
                    'Payer_Account' : 'U123123',
                    'PAYMENT_AMOUNT' : '123.00',
                    'PAYMENT_BATCH_NUM' : '12345',
                    'VOUCHER_NUM' : 1112222213,
                    'VOUCHER_CODE' : 3232323232323232,
                    'VOUCHER_AMOUNT' : ''123.00
                }
        """
        params = {
            'Payer_Account': payer,
            'Amount': amount,
        }
        url = BASE_URL.format('ev_create', self.__account, self.__passwd,
                              "&".join(["{0}={1}".format(key, str(value)) for key, value in params.items()]))
        res = self._fetch(url, None)
        return self._get_dict(res)

    def ev_remove(self, ev_number):
        """
            Remove e-Voucher
            return: dictionary
            example:
                {
                    'Payer_Account' : 'U123123',
                    'PAYMENT_AMOUNT' : '123.00',
                    'PAYMENT_BATCH_NUM' : '12345',
                    'VOUCHER_NUM' : 1112222213,
                    'VOUCHER_AMOUNT' : ''123.00
                }
        """
        url = BASE_URL.format('ev_remove', self.__account, self.__passwd, "{0}={1}".format('ev_number', ev_number))
        res = self._fetch(url, None)

        return self._get_dict(res)

    def evcsv(self):
        """
            e-Vouchers listing in CSV
            return: list
        """
        url = BASE_URL.format('evcsv', self.__account, self.__passwd, '')
        res = self._fetch(url, None)
        return self._get_list(res)

    def check(self, payee, payer, amount, units, batch_number, secret, timestamp, payment_id, v2_hash):
        """
            Validates SCI payment confirmation data from Perfectmoney server
            return: True/False
        """
        check = "%s:%s:%.2f:%s:%s:%s:%s:%s" % (
            payment_id,
            payee,
            amount,
            units,
            batch_number,
            payer,
            secret,
            timestamp
        )
        res = hashlib.md5(check).hexdigest().upper()
        if res == v2_hash:
            return True
        return False
