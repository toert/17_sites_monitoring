import requests
import whois
from datetime import datetime, timedelta
import argparse


AMOUNT_DAYS = 30


def parse_path():
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        help='enter the filepath to file with URLs')
    return parser.parse_args()


def load_urls4check(path):
    with open(path, 'r') as url_data:
        return [url for url in url_data.read().splitlines()]


def is_server_respond_with_200(url):
    return requests.get(url).status_code == 200


def get_domain_expiration_date(domain_name):
    whois_obj = whois.whois(domain_name)
    exper_datetime = whois_obj.expiration_date
    if type(exper_datetime) is list:
        return exper_datetime[0]
    else:
        return exper_datetime


def is_it_pay_for_month(exp_date):
    if exp_date is None:
        return False
    return (exp_date - datetime.today() > timedelta(days=AMOUNT_DAYS))


def print_state(url, paid, available):
    if paid and available:
        print('{} is OK'.format(url))
    elif not paid and available:
        print('{} needs payments'.format(url))
    elif paid and not available:
        print('{} isn\'t available'.format(url))
    else:
        print('{} isn\'t available and needs payments'.format(url))


if __name__ == '__main__':
    parser = parse_path()
    filepath = parser.path
    urls = load_urls4check(filepath)
    urls = list(filter(lambda url: url, urls)) #delete empty lines
    for url in urls:
        exp = get_domain_expiration_date(url)
        print_state(url, is_it_pay_for_month(exp), is_server_respond_with_200(url))