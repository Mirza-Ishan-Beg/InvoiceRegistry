import inspect
import sqlite3
from typing import Optional, List, Dict, Union, Tuple


class Modulation:
    """
    Central class containing nested database utilities with improved CRUD operations
    """

    class SQLiteDatabase:
        """Enhanced database handler with dictionary support"""

        def __init__(self, db_path: str):
            self.db_path = db_path
            self.row_factory = sqlite3.Row  # Enable dictionary-like access
            self._set_pragma_settings()

        def _set_pragma_settings(self):
            """Configure database durability settings"""
            try:
                with self._get_connection() as conn:
                    conn.execute("PRAGMA journal_mode = WAL;")
                    conn.execute("PRAGMA synchronous = FULL;")
                    conn.execute("PRAGMA foreign_keys = ON;")
            except sqlite3.Error as e:
                self._log_error(e)

        def _get_connection(self):
            """Get connection with dictionary row factory"""
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = self.row_factory
            return conn

        def _log_error(self, error: Exception):
            """Centralized error logging using inspect module"""
            # Get the current function name
            current_function = inspect.currentframe().f_back.f_code.co_name
            print(f"\n⚠️ Error in {current_function}: {str(error)}\n")

        def execute_dict(
                self,
                sql: str,
                parameters: Optional[Dict] = None,
                commit: bool = True
        ) -> int:
            """
            Execute write operation with dictionary parameters
            Returns number of affected rows
            """
            try:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(sql, parameters or {})
                    if commit:
                        conn.commit()
                    return cursor.rowcount
            except sqlite3.Error as e:
                self._log_error(e)
                return 0

        def fetch_all_dict(
                self,
                sql: str,
                parameters: Optional[Dict] = None
        ) -> List[Dict]:
            """Fetch all results as dictionaries"""
            try:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(sql, parameters or {})
                    return [dict(row) for row in cursor.fetchall()]
            except sqlite3.Error as e:
                self._log_error(e)
                return []

        def fetch_one_dict(
                self,
                sql: str,
                parameters: Optional[Dict] = None
        ) -> Optional[Dict]:
            """Fetch single result as dictionary"""
            try:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(sql, parameters or {})
                    result = cursor.fetchone()
                    return dict(result) if result else None
            except sqlite3.Error as e:
                self._log_error(e)
                return None

        def transaction_dict(self, operations: List[Tuple[str, Optional[Dict]]]) -> bool:
            """
            Execute multiple dictionary-parameter operations in transaction
            Returns True if successful
            """
            try:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    for sql, params in operations:
                        cursor.execute(sql, params or {})
                    conn.commit()
                    return True
            except sqlite3.Error as e:
                self._log_error(e)
                return False

    class CRUDOperations:
        """Generic CRUD operations using dictionary input/output"""

        def __init__(self, db: 'Modulation.SQLiteDatabase'):
            self.db = db

        def create(self, table: str, data: Dict) -> int:
            """Insert new record, returns inserted row ID"""
            columns = ", ".join(data.keys())
            placeholders = ", ".join(f":{k}" for k in data.keys())
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.db.execute_dict(sql, data)
            return self.db.fetch_one_dict("SELECT last_insert_rowid() AS id")['id']

        def read(self, table: str, filters: Optional[Dict] = None) -> List[Dict]:
            """Read records with optional filters"""
            sql = f"SELECT * FROM {table}"
            params = {}
            if filters:
                where_clause = " AND ".join(f"{k} = :{k}" for k in filters.keys())
                sql += f" WHERE {where_clause}"
                params = filters
            return self.db.fetch_all_dict(sql, params)

        def update(self, table: str, updates: Dict, conditions: Dict) -> int:
            """Update records, returns number of affected rows"""
            set_clause = ", ".join(f"{k} = :{k}" for k in updates.keys())
            where_clause = " AND ".join(f"{k} = :cond_{k}" for k in conditions.keys())

            # Separate update values and condition values
            params = updates.copy()
            params.update({f"cond_{k}": v for k, v in conditions.items()})

            sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            return self.db.execute_dict(sql, params)

        def delete(self, table: str, conditions: Dict) -> int:
            """Delete records, returns number of affected rows"""
            where_clause = " AND ".join(f"{k} = :{k}" for k in conditions.keys())
            sql = f"DELETE FROM {table} WHERE {where_clause}"
            return self.db.execute_dict(sql, conditions)

        def get_table_schema(self, table: str) -> list[Dict]:
            """Get column information for a table"""
            return self.db.fetch_all_dict(f"PRAGMA table_info({table})")

        def get_primary_key(self, table: str) -> Union[str, List[str]]:
            """Get primary key column(s) for a table"""
            schema = self.get_table_schema(table)
            pk = [col['name'] for col in schema if col['pk'] > 0]
            return pk[0] if len(pk) == 1 else pk
