"""Database layer — re-exports connect for backward compatibility."""
from database.connection import connect

__all__ = ["connect"]
