from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import aiosqlite
from contextlib import asynccontextmanager

@asynccontextmanager
async def create_async_sqlite_saver(db_file="sidekick_memory.sqlite"):
    """
    Create an async SQLite saver for persistent memory storage.
    
    Args:
        db_file: Path to the SQLite database file.
        
    Yields:
        AsyncSqliteSaver: An instance of AsyncSqliteSaver.
    """
    async with aiosqlite.connect(db_file) as conn:
        yield AsyncSqliteSaver(conn)