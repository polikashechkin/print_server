import os, sys
from domino.core import log, IS_LINUX

if __name__ == "__main__":
    account_id = sys.argv[1]
    if IS_LINUX:
        import tables.postgres.printer
        import tables.postgres.print_queue_item
        import tables.postgres.print_template
        tables.postgres.printer.on_activate(account_id, print)
        tables.postgres.print_queue_item.on_activate(account_id, print)
        tables.postgres.print_template.on_activate(account_id, print)
