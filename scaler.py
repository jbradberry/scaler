import argparse
import os
import sqlite3


def _list(args, cur):
    _debug(args)


def _create(args, cur):
    _debug(args)


def _edit(args, cur):
    _debug(args)


def _compare(args, cur):
    _debug(args)


def _compute(args, cur):
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

    db_filename = 'scaler.db3'
    with sqlite3.connect(db_filename) as conn:
        cur = conn.cursor()
        cur.executescript(
            """
            create table if not exists list (
                id           integer primary key autoincrement not null,
                name         text,
                created      timestamptz,
                updated      timestamptz,
                calculated   timestamptz,
                new_data     bool not null default false
            );

            create table if not exists item (
                list_id      integer not null,
                id           integer not null,
                name         text,
                timestamp    timestamptz
            );

            create table if not exists score (
                list_id      integer not null,
                id           integer not null,
                value        real
            );

            create table if not exists comparison (
                list_id      integer not null,
                item1        integer not null,
                item2        integer not null,
                result       tinyint not null,
                timestamp    timestamptz
            );
            """
        )

        args.func(args, cur)
