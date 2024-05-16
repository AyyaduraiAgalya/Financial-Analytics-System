import unittest
from sqlalchemy import inspect
from database.db_connect import get_engine, Base
from database.schema.migrate import migrate_database

class TestMigrate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up an in-memory SQLite database for testing
        cls.engine = get_engine()
        Base.metadata.create_all(cls.engine)

    def test_migrate_database(self):
        # Run the migration script
        migrate_database()

        # Use SQLAlchemy inspector to check if tables were created
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()

        # Check that the required tables exist
        self.assertIn('currency_data', tables)
        self.assertIn('moving_average', tables)
        self.assertIn('prediction', tables)

if __name__ == '__main__':
    unittest.main()
