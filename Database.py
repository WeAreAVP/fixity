import collections
import sqlite3


class SqliteDict(collections.MutableMapping):
    @classmethod
    def create(cls, path, columns):
        conn = sqlite3.connect(path)
        conn.execute('DROP TABLE IF EXISTS SqliteDict')
        conn.execute('CREATE TABLE SqliteDict ({0})'.format(','.join(columns.split())))
        conn.commit()
        return cls(conn)
    
    @classmethod
    def open(cls, path):
        conn = sqlite3.connect(path)
        return cls(conn)
    
    def __init__(self, conn):
        # looks like for sime weird reason you want str, not unicode, when feasible, so...:
        conn.text_factory = sqlite3.OptimizedUnicode
        c = conn.cursor()
        c.execute('SELECT * FROM SqliteDict LIMIT 0')
        self.cols = [x[0] for x in c.description]
        self.conn = conn
        # start with a keyname (==column name) of `ID`
        self.set_key('ID')
    
    def set_key(self, key):
        self.i = self.cols.index(key)
        self.kn = key
    
    def __len__(self):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM SqliteDict')
        return c.fetchone()[0]
    
    def __iter__(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM SqliteDict')
        while True:
            result = c.fetchone()
            if result is None: break
            k = result.pop(self.i)
            return k, result
    
    def __getitem__(self, k):
        c = self.conn.cursor()
        # print 'doing:', 'SELECT * FROM SqliteDict WHERE {0}=?'.format(self.kn)
        # print ' with:', repr(k)
        c.execute('SELECT * FROM SqliteDict WHERE {0}=?'.format(self.kn), (k,))
        result = [list(r) for r in c.fetchall()]
        # print ' resu:', repr(result)
        for r in result: del r[self.i]
        return result
    
    def __contains__(self, k):
        c = self.conn.cursor()
        c.execute('SELECT * FROM SqliteDict WHERE {0}=?'.format(self.kn), (k,))
        return c.fetchone() is not None
    
    def __delitem__(self, k):
        c = self.conn.cursor()
        c.execute('DELETE FROM SqliteDict WHERE {0}=?'.format(self.kn), (k,))
        self.conn.commit()
    
    def __setitem__(self, k, v):
        r = list(v)
        r.insert(self.i, k)
        if len(r) != len(self.cols):
            raise ValueError, 'len({0}) is {1}, must be {2} instead'.format(r, len(r), len(self.cols))
        c = self.conn.cursor()
        # print 'doing:', 'REPLACE INTO SqliteDict VALUES({0})'.format(','.join(['?']*len(r)))
        # print ' with:', r
        c.execute('REPLACE INTO SqliteDict VALUES({0})'.format(','.join(['?']*len(r))), r)
        self.conn.commit()
    
    def close(self):
        self.conn.close()


def main():
    d = SqliteDict.create('student_table', 'ID NAME BIRTH AGE SEX')
    d['1'] = ["Joe", "01011980", "30", "M"]    
    d['2'] = ["Rose", "12111986", "24", "F"]
    print len(d), 'items in table created.'
    print d['2']
    print d['1']
    d.close()
    
    d = SqliteDict.open('student_table')
    d.set_key('NAME')
    print len(d), 'items in table opened.'
    print d['Joe']


if __name__ == '__main__':
  main()