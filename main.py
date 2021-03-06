from src.loader import FileLoader
from src.processor import build_statistics
import sys
import argparse


if __name__ == "__main__":
    argv = sys.argv

    parser = argparse.ArgumentParser(description='Log analysator')
    parser.add_argument('--filename', nargs='?', required=True,
                        help='Input file name')
    parser.add_argument('--target_domain', nargs='?', required=False, default="ours.com",
                        help='Target domain. We count transmit from this domain')            # ours.com
    parser.add_argument('--shop_domain', nargs='?', required=False, default="shop.com",
                        help='Shop domain')            # shop.com
    parser.add_argument('--another_domains', nargs='+', required=False, default=["theirs1.com", "theirs2.com"],
                        help='Our competitors partner domains')
    parser.add_argument('--finish_url', nargs='?', required=False, default="https://shop.com/checkout",
                        help='URL where user trasmits after purchase')
    parser.add_argument('--ignore-errors', required=False, default=False, action="store_true",
                        help='Ignore validation errors')

    args = parser.parse_args()

    # load data
    loader = FileLoader(args.filename, args.ignore_errors)
    data = loader.load()
    data = sorted(data, key=lambda x: x.request_datetime)
    # process data
    stat = build_statistics(data, args.shop_domain, args.finish_url, args.target_domain, args.another_domains)
    print("\n".join(map(str, stat)))
