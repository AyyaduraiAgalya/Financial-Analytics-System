import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError

# Import the module and functions to be tested
import database.db_connect as db_connect


class TestDatabaseConnection(unittest.TestCase):

    @patch('database.db_connect.create_engine')
    @patch('database.db_connect.os.getenv')
    def test_get_database_url(self, mock_getenv, mock_create_engine):
        """Test constructing the database URL from environment variables."""
        # Setup mock environment variables
        mock_getenv.side_effect = lambda key: {
            'DB_USER': 'user',
            'DB_PASS': 'pass',
            'DB_HOST': 'localhost',
            'DB_PORT': '5432',
            'DB_NAME': 'dbname'
        }[key]

        # Call the function
        result = db_connect.get_database_url()

        # Assert the expected database URL
        expected = 'postgresql+psycopg2://user:pass@localhost:5432/dbname'
        self.assertEqual(result, expected)

    @patch('database.db_connect.get_database_url')
    @patch('database.db_connect.create_engine')
    def test_get_engine(self, mock_create_engine, mock_get_database_url):
        """Test getting the SQLAlchemy engine."""
        # Setup mock return value for get_database_url
        mock_get_database_url.return_value = 'mock_database_url'

        # Call the function
        db_connect.get_engine()

        # Assert create_engine was called with the correct database URL
        mock_create_engine.assert_called_once_with('mock_database_url', echo=True)

    @patch('database.db_connect.get_engine')
    @patch('database.db_connect.sessionmaker')
    def test_get_session(self, mock_sessionmaker, mock_get_engine):
        """Test creating a new session."""
        # Setup mock engine and sessionmaker
        mock_engine = MagicMock()
        mock_get_engine.return_value = mock_engine
        mock_session_factory = MagicMock()
        mock_sessionmaker.return_value = mock_session_factory
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session

        # Call the function
        result = db_connect.get_session()

        # Assert sessionmaker was called with the correct engine
        mock_sessionmaker.assert_called_once_with(bind=mock_engine)

        # Assert the returned session is as expected
        self.assertEqual(result, mock_session)

    @patch('database.db_connect.get_engine')
    def test_test_connection_success(self, mock_get_engine):
        """Test successful database connection."""
        # Setup mock engine and connection
        mock_engine = MagicMock()
        mock_get_engine.return_value = mock_engine
        mock_connection = mock_engine.connect.return_value.__enter__.return_value

        # Call the function
        db_connect.test_connection()

        # Assert engine.connect was called
        mock_engine.connect.assert_called_once()

    @patch('database.db_connect.get_engine')
    def test_test_connection_failure(self, mock_get_engine):
        """Test database connection failure."""
        # Setup mock engine and connection to raise an exception
        mock_engine = MagicMock()
        mock_get_engine.return_value = mock_engine
        mock_engine.connect.side_effect = SQLAlchemyError("Connection error")

        # Assert the SQLAlchemyError is raised during test_connection call
        with self.assertRaises(SQLAlchemyError):
            db_connect.test_connection()


if __name__ == "__main__":
    unittest.main()
