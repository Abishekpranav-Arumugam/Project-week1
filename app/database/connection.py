import mysql.connector
from mysql.connector import Error

from app.config.settings import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
)
from app.utils.logger import logger


class DatabaseManager:
    """
    Handles MySQL database connection and SQL execution.
    """

    def __init__(self):
        self.connection = None

    def connect(self):
        """
        Establish connection with MySQL.
        """

        try:
            if self.connection and self.connection.is_connected():
                return self.connection

            self.connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
            )

            if self.connection.is_connected():
                logger.info("Database connection established.")
                return self.connection

        except Error as error:
            logger.error(
                "Database connection failed: %s",
                error,
            )
            self.connection = None
            raise

        return None

    def get_connection(self):
        """
        Return an active database connection.
        """

        if not self.connection or not self.connection.is_connected():
            return self.connect()

        return self.connection

    def execute_query(self, query, parameters=None):
        """
        Execute INSERT, UPDATE or DELETE queries.

        Returns:
            int: Number of affected rows.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()

            if connection is None:
                raise ConnectionError(
                    "Unable to establish database connection."
                )

            cursor = connection.cursor()

            cursor.execute(query, parameters or ())
            connection.commit()

            affected_rows = cursor.rowcount

            logger.info(
                "SQL modification executed successfully. "
                "Affected rows: %s",
                affected_rows,
            )

            return affected_rows

        except Error as error:
            if connection:
                connection.rollback()

            logger.error(
                "SQL modification failed. "
                "Transaction rolled back: %s",
                error,
            )

            raise

        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query, parameters=None):
        """
        Execute SELECT query and return all rows.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()

            if connection is None:
                raise ConnectionError(
                    "Unable to establish database connection."
                )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, parameters or ())

            results = cursor.fetchall()

            logger.info(
                "SELECT query executed successfully. "
                "Rows returned: %s",
                len(results),
            )

            return results

        except Error as error:
            logger.error(
                "SELECT query failed: %s",
                error,
            )
            raise

        finally:
            if cursor:
                cursor.close()

    def fetch_one(self, query, parameters=None):
        """
        Execute SELECT query and return one row.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()

            if connection is None:
                raise ConnectionError(
                    "Unable to establish database connection."
                )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, parameters or ())

            result = cursor.fetchone()

            logger.info(
                "Single-record SELECT executed successfully."
            )

            return result

        except Error as error:
            logger.error(
                "Single-record SELECT failed: %s",
                error,
            )
            raise

        finally:
            if cursor:
                cursor.close()

    def disconnect(self):
        """
        Close the MySQL connection.
        """

        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger.info("Database connection closed.")

        except Error as error:
            logger.error(
                "Error while closing database connection: %s",
                error,
            )

        finally:
            self.connection = None