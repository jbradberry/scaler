import argparse
import datetime
import os
import sqlite3


def _list(args, cur):
    cur.execute(
        """
        SELECT l.id, l.name, count(1)
        FROM list l
        LEFT OUTER JOIN item i
          ON l.id = i.list_id
        GROUP BY l.id, l.name
        ORDER BY l.id ASC;
        """
    )
    data = list(cur)
    if not data:
        print("No lists have been created yet.")
        return
    for row in data:
        print(f"{row[0]}: {row[1]} ({row[2]} items)")


def _create(args, cur):
    name = input("list name: ")
    items = []
    print("input items (empty to stop)...")
    while True:
        item = input("item: ")
        if not item:
            break
        items.append(item)

    timestamp = datetime.datetime.now(datetime.timezone.utc)
    cur.execute(
        "INSERT INTO list (name, created, updated) VALUES (?, ?, ?);",
        (name, timestamp, timestamp)
    )
    _id = cur.lastrowid
    for i, item in enumerate(items, start=1):
        cur.execute(
            "INSERT INTO item (list_id, id, name, timestamp) VALUES (?, ?, ?, ?);",
            (_id, i, item, timestamp)
        )


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
