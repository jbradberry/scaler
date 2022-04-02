import argparse


def _list(args):
    _debug(args)


def _create(args):
    _debug(args)


def _edit(args):
    _debug(args)


def _compare(args):
    _debug(args)


def _compute(args):
    _debug(args)


def _debug(args):
    print(f"args: {args!r}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(func=_list)

    parser_create = subparsers.add_parser('create')
    parser_create.set_defaults(func=_create)

    parser_edit = subparsers.add_parser('edit')
    parser_edit.add_argument('list', type=int)
    parser_edit.set_defaults(func=_edit)

    parser_compare = subparsers.add_parser('compare')
    parser_compare.add_argument('list', type=int)
    parser_compare.set_defaults(func=_compare)

    parser_compute = subparsers.add_parser('compute')
    parser_compute.add_argument('list', type=int)
    parser_compute.set_defaults(func=_compute)

    args = parser.parse_args()
    args.func(args)
