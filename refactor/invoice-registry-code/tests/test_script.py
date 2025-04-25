"""
THIS SCRIPT IS TO CONDUCT MANUAL TESTS, I MAY OR MAY NOT STACK THE TESTS HERE.
"""

import os
from db.Inv_DB import TableMaker

class Tester(TableMaker):
    def __init__(self, db):
        super().__init__(db)

    def read_all(self):
        """
        Test function to read all the tables...
        """
        for i in self.list_of_tables:
            specific_table_contents = self.read(i)
            print("-"*64)
            print(i)
            table_col = self.fetch_all_dict(f"SELECT * FROM {i};")
            print(table_col)
            print("-"*64)
            """for j in specific_table_contents:
                print(f"")"""
        print("Execution Successful!")
        return None


if __name__ == "__main__":
    obj_test = Tester(db="testing_db.db")
    obj_test.read_all()
