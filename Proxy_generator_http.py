"""
Function for scraping a list of proxies from https://free-proxy-list.net/

Author: Jamie Bamforth
"""

import requests
import bs4


def proxy_generator_http():
    """Scrapes the site sslproxies.org for proxy details and returns a list of proxies. Each proxy is a string in the
    format 'https://[IP ADDRESS].[PORT]'."""
    url = 'https://free-proxy-list.net/'
    proxy_page = requests.get(url)
    proxy_page_soup = bs4.BeautifulSoup(proxy_page.text, 'html.parser')
    proxy_table = proxy_page_soup.find('table', {'class': "table table-striped table-bordered"}).find_all('tr')
    # take first two row entries, IP address and port and concat into https address
    first_data_row = 1
    empty_row = -1
    ip_entry = 0
    port_entry = 1
    proxy_rows_split = [proxy.find_all('td')[:port_entry + 1] for proxy in proxy_table[first_data_row:empty_row]]
    proxy_IP_ports = [proxy[ip_entry].text + ':' + proxy[port_entry].text for proxy in proxy_rows_split]
    return proxy_IP_ports


def main():
    # no way to test for specific proxies as they may change
    proxies = proxy_generator_http()
    print(len(proxies))
    print(proxies)


if __name__ == '__main__':
    main()
