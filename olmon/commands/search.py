import sys

from olmon.db import get_connection, search_models
from olmon.display import print_error, print_search_results


def search_command(query: str | None = None, limit: int | None = None) -> None:
    if not query:
        print_error("Please provide a search query, e.g. olmon search vision")
        sys.exit(2)

    conn = get_connection()
    models = search_models(conn, query, limit=limit or 20)
    conn.close()

    print_search_results(models, query)
    sys.exit(0 if models else 1)
