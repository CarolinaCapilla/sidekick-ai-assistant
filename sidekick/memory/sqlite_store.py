from langgraph.checkpoint.sqlite import SqliteSaver

def create_sqlite_saver(db_file="sidekick_memory.sqlite"):
    """Create a SQLite saver for persistent memory storage."""
    return SqliteSaver(db_file=db_file)