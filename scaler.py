import argparse


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_list = subparsers.add_parser('list')

parser_create = subparsers.add_parser('create')

parser_edit = subparsers.add_parser('edit')
parser_edit.add_argument('list')

parser_compare = subparsers.add_parser('compare')
parser_compare.add_argument('list')

parser_compute = subparsers.add_parser('compute')
parser_compute.add_argument('list')


if __name__ == '__main__':
    args = parser.parse_args()
    print(f"args: {args!r}")
