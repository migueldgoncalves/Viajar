import unittest
import os

from travel.support.sqlite_interface import SQLiteDBInterface
from travel.main import paths_and_files


class TestSQLiteDBInterface(unittest.TestCase):
    def setUp(self):
        if os.path.exists(paths_and_files.ANDROID_DB_FILE_PATH):
            os.remove(paths_and_files.ANDROID_DB_FILE_PATH)

    def test_create_sqlite_db(self):
        SQLiteDBInterface(return_instead_of_exit=True)  # Will create and populate the DB

        if not os.path.exists(paths_and_files.ANDROID_DB_FILE_PATH):
            self.fail("SQLite DB was not created")

        file_size: int = os.path.getsize(paths_and_files.ANDROID_DB_FILE_PATH)
        min_expected_size: int = 1000000  # DB can be expected to have >1 MB. As of JUN2024, size is 3.7 MB
        self.assertTrue(file_size > min_expected_size)
