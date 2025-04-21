import unittest
import os, sys
import sqlite3
from db.Modulated_Database_Constructor import Modulation


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

TEST_DB = os.path.join(os.path.dirname(__file__), "test.db")

def setup_test_table():
    """Prepare a dummy invoices table for testing"""
    with sqlite3.connect(TEST_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor TEXT,
                amount REAL,
                status TEXT
            )
        """)

class TestModulationCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_test_table()
        cls.db = Modulation.SQLiteDatabase(TEST_DB)
        cls.crud = Modulation.CRUDOperations(cls.db)

    def test_create_and_read(self):
        data = {"vendor": "Acme", "amount": 1000.5, "status": "Pending"}
        new_id = self.crud.create("invoices", data)
        result = self.crud.read("invoices", {"id": new_id})
        self.assertEqual(result["vendor"], data["vendor"])
        self.assertEqual(result["amount"], data["amount"])
        self.assertEqual(result["status"], data["status"])

    def test_update(self):
        row_id = self.crud.create("invoices", {"vendor": "Old", "amount": 300, "status": "Pending"})
        updated = self.crud.update("invoices", {"vendor": "New"}, {"id": row_id})
        self.assertEqual(updated, 1)
        updated_row = self.crud.read("invoices", {"id": row_id})
        self.assertEqual(updated_row["vendor"], "New")

    def test_delete(self):
        row_id = self.crud.create("invoices", {"vendor": "DeleteMe", "amount": 200, "status": "Paid"})
        deleted = self.crud.delete("invoices", {"id": row_id})
        self.assertEqual(deleted, 1)
        result = self.crud.read("invoices", {"id": row_id})
        self.assertEqual(len(result), 0)

    def test_schema_fetch(self):
        schema = self.crud.get_table_schema("invoices")
        self.assertTrue(any(col["name"] == "vendor" for col in schema))

    def test_primary_key_detection(self):
        pk = self.crud.get_primary_key("invoices")
        self.assertEqual(pk, "id")

    @classmethod
    def tearDownClass(cls):
        os.remove(TEST_DB)

if __name__ == "__main__":
    unittest.main()
