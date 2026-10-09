import os
import psycopg2


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=os.environ.get("DB_NAME", "workdatabase1"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", "postgresql"),
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", "5432"),
            connect_timeout=5,
        )
        self.curr = self.conn.cursor()

    def _commit(self):
        self.conn.commit()

    def _fetchall(self):
        return self.curr.fetchall()

    def _run(self, q):
        self.curr.execute(q)

    def close(self):
        self.curr.close()
        self.conn.close()

    def select(self, q):
        try:
            self._run(q)
            return self._fetchall()
        finally:
            self.close()

    def insert(self, q):
        try:
            self._run(q)
            self._commit()
            return "ok inserted task"
        except Exception:
            self.conn.rollback()
            raise
        finally:
            self.close()
    