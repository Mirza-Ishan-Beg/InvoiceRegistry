import os
from db.Modulated_Database_Constructor import Modulation

class TableMaker(Modulation.CRUDOperations, Modulation.SQLiteDatabase):
    def __init__(self, db):
        Modulation.SQLiteDatabase.__init__(self, db)   # Initialized the main SQLite Database operations
        Modulation.CRUDOperations.__init__(self, self) # Initialized the CRUD operations and gave self
        # We give self because prior syntax initializes and makes the TableMaker have SQLiteDatabase
        # methods entirely, satisfying the params.
        Table1 = """
                    CREATE TABLE IF NOT EXISTS invoices(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_number TEXT,
                        vendor_name TEXT,
                        date TEXT,
                        due_date TEXT,
                        price INTEGER
                    )
                    """
        Table2 = """
                    CREATE TABLE IF NOT EXISTS credits_debits_notes(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_id INTEGER,
                        note_number TEXT,
                        note_type TEXT,
                        transaction_mode TEXT,
                        price INTEGER,
                        reason TEXT,
                        FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
                    )
                    """
        Table3 = """
                    CREATE TABLE IF NOT EXISTS outstanding_table(
                        invoice_id INTEGER,
                        invoice_number TEXT,
                        initial_price INTEGER,
                        total_credits INTEGER DEFAULT 0,
                        total_debits INTEGER DEFAULT 0,
                        due_date TEXT,
                        payment INTEGER,
                        outstanding INTEGER
                    )
                    """
        Table4 = """
                    CREATE TABLE IF NOT EXISTS logs(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        role TEXT,
                        event TEXT,
                        event_type TEXT,
                        date INTEGER
                    )
                    """
        Table5 = """
                    CREATE TABLE IF NOT EXISTS roles(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        role TEXT,
                        date_of_creation TEXT,
                        last_active TEXT,
                        total_insertions INTEGER,
                        total_deletions INTEGER,
                        total_modifications INTEGER
                    )
                    """
        Table6 =    """
                    CREATE VIEW IF NOT EXISTS daily_summary AS
                        SELECT
                            invoices.due_date AS due_date,
                            COALESCE(SUM(outstanding_table.outstanding), 0) AS total_outstanding,
                            COALESCE(SUM(outstanding_table.payment), 0) AS total_payment,
                            COUNT(invoices.ID) AS total_invoices
                        FROM invoices
                        LEFT JOIN outstanding_table
                            ON invoices.due_date = outstanding_table.due_date
                        GROUP BY invoices.due_date;
                    """
        self.list_of_tables = [Table1, Table2, Table3, Table4, Table5, Table6]
        self.make_tables(self.list_of_tables)
        # putting names of the tables for easing testing functions...
        self.list_of_tables = [
            "invoices", "credits_debits_notes",
            "outstanding_table", "logs",
            "roles", "daily_summary"
                                  ]

    def make_tables(self, tables: list):
        for i in tables:
            self.execute_dict(i)
    
    
