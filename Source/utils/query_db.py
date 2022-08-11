# -*- coding: utf-8 -*-


import re
import json
import sqlite3
from os.path import expanduser, dirname, abspath


with open(dirname(dirname(abspath(__file__))) + '/conf.json', 'r') as f:
    CONF = json.load(f)

class QueryDB:
    
    ignore_set = set(CONF['IGNORE'])
    
    def __init__(self, wf, search_str: str = None, digits: str = '5',  before_day: str = '1', sender: str = None):
        self.wf = wf
        self.search_str, self.digits, self.before_day, self.sender = search_str, digits, before_day, sender
        self.conn = sqlite3.connect(expanduser("~") + "/Library/Messages/chat.db")
        self.cur = self.conn.cursor()
        
    def __del__(self):
        self.cur.close()
        self.conn.close()
        
    def _parse_where(self):
        r = [f"rcv_time > datetime('now', '-{self.before_day} day')"]
        
        if self.search_str:
            r.append('text LIKE "%{}%"'.format(self.search_str.replace("'", '').replace('"', '')))
        
        if self.sender:
            r.append('handle.id like "%{}%"'.format(self.sender))
        
        return ' AND '.join(r)
        
    def _query_db(self):
        
        self.cur.execute((
            "SELECT "
            "text, "
            "datetime((date / 1000000000) + 978307200, 'unixepoch', 'localtime') as rcv_time, "
            "handle.id, "
            "handle.service, "
            "message.destination_caller_id, "
            "message.is_from_me "
            "FROM message "
            "JOIN handle on message.handle_id=handle.ROWID "
            "WHERE {} "
            "ORDER BY rcv_time DESC "
        ).format(self._parse_where()))
        return self.cur.fetchall()

    def parse_result(self):
        for row in self._query_db():
            codes = set(re.findall(r'\d{%s,}' % self.digits, row[0])).difference(self.ignore_set)
            for code in codes:
                self.wf.add_item(title=code, subtitle=row[0], arg=code, icon='item.png', copytext=code, valid=True, largetext=f'[From] {row[2]}\n[To] {row[4]}\n[Type] {row[3]}\n[Content] {row[0]}')