import argparse
import datetime
import os
import random
import sqlite3
import sys


def _list_detail(args, cur):
    cur.execute("SELECT * FROM list WHERE id = ?;", (args.list,))
    row = cur.fetchone()
    if row is None:
        print(f"List {args.list} does not exist.")
        return

    cur.execute(
        """
        SELECT id, name
        FROM item
        WHERE list_id = ?
        ORDER BY id ASC;
        """,
        (args.list,)
    )
    items = list(cur)
    print(f"{row[1]} ({len(items)} items)\n")

    for i, item in items:
        print(f"{i}: {item}")


def _list(args, cur):
    if args.list is not None:
        _list_detail(args, cur)
        return

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
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    cur.execute(
        "INSERT INTO list (name, created, updated) VALUES (?, ?, ?);",
        (args.name, timestamp, timestamp)
    )
    _id = cur.lastrowid

    items = [(i, line.strip()) for i, line in enumerate(sys.stdin.readlines(), start=1)]
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    for i, item in items:
        cur.execute(
            "INSERT INTO item (list_id, id, name, timestamp) VALUES (?, ?, ?, ?);",
            (_id, i, item, timestamp)
        )


def _edit(args, cur):
    _debug(args)


def _compare(args, cur):
    cur.execute("SELECT * FROM list WHERE id = ?;", (args.list,))
    if cur.fetchone() is None:
        print(f"List {args.list} does not exist.")
        return

    cur.execute("SELECT id, name FROM item WHERE list_id = ? ORDER BY id ASC;", (args.list,))
    data = list(cur)
    if not data:
        print(f"List {args.list} has no items to compare.")
        return

    while True:
        (id1, name1), (id2, name2) = random.sample(data, 2)
        print("Which item is preferred?\n")
        print(f"1: {name1}")
        print(f"2: {name2}")
        print("0: both items are roughly equal\n")

        choice = 'z'
        while choice not in ('0', '1', '2', 'q'):
            choice = input("'q' to stop: ")
        if choice == 'q':
            break

        timestamp = datetime.datetime.now(datetime.timezone.utc)
        cur.execute(
            """
            INSERT INTO comparison (list_id, item1, item2, result, timestamp)
            VALUES (?, ?, ?, ?, ?);
            """,
            (args.list, id1, id2, int(choice), timestamp)
        )
        print()


def _compute(args, cur):
    _debug(args)


def _debug(args):
    print(f"args: {args!r}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('list', nargs='?', type=int, default=None)
    parser_list.set_defaults(func=_list)

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('name')
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
            CREATE TABLE IF NOT EXISTS list (
                id           integer PRIMARY KEY,
                name         text,
                created      timestamptz,
                updated      timestamptz,
                calculated   timestamptz,
                new_data     bool NOT NULL DEFAULT false
            );

            CREATE TABLE IF NOT EXISTS item (
                list_id      integer NOT NULL,
                id           integer NOT NULL,
                name         text,
                timestamp    timestamptz
            );

            CREATE TABLE IF NOT EXISTS score (
                list_id      integer NOT NULL,
                id           integer NOT NULL,
                value        real
            );

            CREATE TABLE IF NOT EXISTS comparison (
                list_id      integer NOT NULL,
                item1        integer NOT NULL,
                item2        integer NOT NULL,
                result       tinyint NOT NULL,
                timestamp    timestamptz
            );
            """
        )

        args.func(args, cur)
