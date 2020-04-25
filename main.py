from loader import FileLoader
from processor import build_statistics
import sys
import argparse


if __name__ == "__main__":
    argv = sys.argv

    parser = argparse.ArgumentParser(description='Log analysator')
    parser.add_argument('--filename', nargs='?', required=True,
                        help='filename of log file')
    parser.add_argument('--our_domain', nargs='?', required=False,
                        default="ours.com", help='our domain')            # ours.com
    parser.add_argument('--shop_domain', nargs='?', required=False,
                        default="shop.com", help='shop domain')            # shop.com
    parser.add_argument('--another_domains', nargs='+', required=False,
                        default=["theirs1.com", "theirs2.com"], help='another domains')
    parser.add_argument('--finish_url', nargs='?', required=False,
                        default="https://shop.com/checkout",
                        help='filename of log file')            # https://shop.com/checkout

    args = parser.parse_args()
    # TODO: check domains and url

    loader = FileLoader(args.filename)
    data = loader.load()

    data = sorted(data, key=lambda x: x.datetime)
    stat = build_statistics(data, args.shop_domain, args.finish_url, args.our_domain, args.another_domains)
    print("\n".join(map(str, stat)))
