#!/usr/bin/env python3
from argparse import ArgumentParser

from lolcatt.app import LolCatt


def main():
    parser = ArgumentParser(description='LolCatt')
    parser.add_argument('url_or_path', nargs='?', help='URL or path to be casted')
    parser.add_argument('-d', '--device', default='default', help='Device name or alias to cast to')
    parsed = parser.parse_args()

    lolcatt = LolCatt(device_name=parsed.device)

    if parsed.url_or_path is not None:
        lolcatt.cast(parsed.url_or_path)
    lolcatt.run()


if __name__ == '__main__':
    main()
