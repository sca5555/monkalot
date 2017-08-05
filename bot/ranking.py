"""Stores points and ranking for games using a database."""

import sqlite3
import math

DATABASE_PATH = "data/monkalot.db"
LEGENDP = 750


class Ranking():
    """Manages spam points ranking."""

    # Set up connection to database and create tables if they do not yet exist.
    connection = sqlite3.connect(DATABASE_PATH)
    sql_create_command = """
        CREATE TABLE IF NOT EXISTS points (
        username TEXT PRIMARY_KEY,
        amount INTEGER
        );
        """
    cursor = connection.cursor()
    cursor.execute(sql_create_command)
    cursor.close()
    connection.commit()
    connection.close()

    def getPoints(self, username):
        """Get the points of a user."""
        sql_command = "SELECT amount FROM points WHERE username = ?;"
        username = username.lower()

        cursor, connection = self.executeCommandGetConnection(sql_command, [username])
        one = cursor.fetchone()
        print("One: " + str(one))

        if(one is None):
            sql_command = "INSERT INTO points (username, amount) VALUES (?, 0);"
            cursor.execute(sql_command, [username])
            connection.commit()
            output = 0
        else:
            output = one[0]

        cursor.close()
        connection.close()
        return output

    def incrementPoints(self, username, amount):
        """Increment points of a user by a certain value."""
        username = username.lower()
        points = int(self.getPoints(username)) + amount
        sql_command = "UPDATE points SET amount = ? WHERE username = ?;"
        self.executeCommand(sql_command, [points, username])

    def getRank(self, points):
        """Get the absolute for a certain amount of points."""
        sql_command = "SELECT * FROM points WHERE amount > ?;"
        cursor, connection = self.executeCommandGetConnection(sql_command, [points])

        all = cursor.fetchall()
        cursor.close()
        connection.close()
        return len(all) + 1

    def getTopSpammers(self, n):
        """Get the n top spammers."""
        sql_command = "SELECT * FROM points ORDER BY amount DESC;"
        cursor, connection = self.executeCommandGetConnection(sql_command, [])
        all = cursor.fetchall()

        return all

    def getHSRank(self, points):
        """Return spam rank of a user in hearthstone units."""
        if points < LEGENDP:
            return str(math.ceil(25 - (points * 25 / LEGENDP)))
        else:
            return "Legend " + str(self.getRank(points))

    def executeCommandGetConnection(self, sql_command, args):
        """Execute a command and return the cursor and connection.

        Use this if you need the output of the command, or need the cursor and connection.
        Since different threads will try to access this method, a connection has to be reopened everytime.
        """
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute(sql_command, args)
        connection.commit()
        return cursor, connection

    def executeCommand(self, sql_command, args):
        """Execute an sql command and closes all connections.

        Does not return output.
        """
        cursor, connection = self.executeCommandGetConnection(sql_command, args)
        cursor.close()
        connection.close()
