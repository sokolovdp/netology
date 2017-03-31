import sys
import argparse
import osa
import os

SOAP_URL_CURRENCY = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
SOAP_URL_LENGTH = 'http://www.webservicex.net/length.asmx?WSDL'
SOAP_URL_TEMPERATURE = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'

LENGTH_CODES = {'KM': "Kilometers", 'MI': "Miles", 'NM': "Nauticalmile"}
TEMPERATURE_CODES = {'C': "degreeCelsius", 'F': "degreeFahrenheit", 'K': 'kelvin'}

currency_client = None
length_client = None
temperature_client = None


def start_currency_service():
    global currency_client
    if currency_client is None:
        try:
            currency_client = osa.client.Client(SOAP_URL_CURRENCY)
        except:
            print("Currency converter service is not available")
            currency_client = None
            return False
    return True


def convert_currency(fr='USD', to='RUB', am=1.0):
    if not currency_client.service.CurrencyExists(currency=fr):
        print("invalid currency code: " + str(fr))
        return -1
    if not currency_client.service.CurrencyExists(currency=to):
        print("invalid currency code: " + str(to))
        return -2
    res = currency_client.service.ConvertToNum(fromCurrency=fr, toCurrency=to,
                                               amount=am, rounding=False)
    if res > 0:
        return round(res, 2)
    else:
        print("currency service error, return value: " + str(res))
        return -3


def currency_data(file):
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
    except IOError as err:
        print("currency file {} read error {}".format(file, err))
        return
    if not start_currency_service():
        return
    sum_rub = 0.
    for line in lines:
        data = line.split()
        rubs = convert_currency(fr=data[-1].upper(), to='RUB', am=float(data[-2].replace(',', '')))
        sum_rub += rubs
        print("{} or {} RUBS".format(' '.join(data), rubs))
    print('-' * 20)
    print("total sum in rubles is", sum_rub, end='\n\n')


def start_length_service():
    global length_client
    if length_client is None:
        try:
            length_client = osa.client.Client(SOAP_URL_LENGTH)
        except:
            print("length converter service is not available")
            length_client = None
            return False
    return True


def convert_length(fr='MI', to='KM', am=1.0):
    if fr not in LENGTH_CODES.keys():
        print("invalid length code: " + str(fr))
        return -1
    if to not in LENGTH_CODES.keys():
        print("invalid length code: " + str(to))
        return -2
    res = length_client.service.ChangeLengthUnit(am, LENGTH_CODES[fr], LENGTH_CODES[to])
    if res > 0:
        return round(res, 2)
    else:
        print("length service error, return value: " + str(res))
        return -3


def length_data(file):
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
    except IOError as err:
        print("travel data file {} read error {}".format(file, err))
        return
    if not start_length_service():
        return
    sum_km = 0.
    for line in lines:
        data = line.split()
        kms = convert_length(fr=data[-1].upper(), to='KM', am=float(data[-2].replace(',', '')))
        sum_km += kms
        print("{} or {} km".format(' '.join(data), kms))
    print('-' * 20)
    print("total distance in kilometers is", sum_km, end='\n\n')


def start_temperature_service():
    global temperature_client
    if temperature_client is None:
        try:
            temperature_client = osa.client.Client(SOAP_URL_TEMPERATURE)
        except:
            print("temperature converter service is not available")
            temperature_client = None
            return False
    return True


def convert_temperature(fr='F', to='C', am=100.):
    if fr not in TEMPERATURE_CODES.keys():
        print("invalid temperature code: " + str(fr))
        return -1
    if to not in TEMPERATURE_CODES.keys():
        print("invalid temperature code: " + str(to))
        return -2
    res = temperature_client.service.ConvertTemp(am, TEMPERATURE_CODES[fr], TEMPERATURE_CODES[to])
    if res > 0:
        return round(res, 1)
    else:
        print("temperature service error, return value: " + str(res))
        return -3


def temperature_data(file):
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
    except IOError as err:
        print("temperature data file {} read error {}".format(file, err))
        return
    if not start_temperature_service():
        return
    sum_tmp = 0.
    for line in lines:
        data = line.split()
        t = convert_temperature(fr=data[-1].upper(), to='C', am=float(data[-2]))
        sum_tmp += t
        print("{} or {}C".format(' '.join(data), t))
    print('-'*20)
    print("average temperature is {}C".format(round(sum_tmp/len(lines))), end='\n\n')


def main(files):
    for f in files:
        func = f[0]
        func(f[1])


if __name__ == "__main__":
    files_to_convert = list()
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--currency", dest="c_file", action="store",
                    help="file with currencies to convert")
    ap.add_argument("-t", "--temperature", dest="t_file", action="store",
                    help="file with temperature to convert")
    ap.add_argument("-l", "--length", dest="l_file", action="store",
                    help="file with temperature to convert")
    args = ap.parse_args(sys.argv[1:])
    if args.c_file and os.path.exists(args.c_file):
        files_to_convert.append((currency_data, args.c_file))
    else:
        print("currency data file {} doesn't exist".format(args.c_file))
    if args.t_file and os.path.exists(args.t_file):
        files_to_convert.append((temperature_data, args.t_file))
    else:
        print("temperature data file {} doesn't exist".format(args.t_file))
    if args.l_file and os.path.exists(args.l_file):
        files_to_convert.append((length_data, args.l_file))
    else:
        print("travel distance data file {} doesn't exist".format(args.l_file))
    if len(files_to_convert):
        main(files_to_convert)
