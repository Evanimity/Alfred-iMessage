# -*- coding: utf-8 -*-

import sys

from workflow import Workflow3, ICON_INFO
from utils.query_db import QueryDB


wf = Workflow3(update_settings={'version': '1.0.0'})
sys_mode_set = {
    't': {'attr': 'before_day', 'type': 'int'}, 
    's': {'attr': 'search_str', 'type': 'any'},
    'f': {'attr': 'sender', 'type': 'any'},
    'l': {'attr': 'digits', 'type': 'int'}
}
sys_args = sys.argv[1:]


def _parse_query(query: str):
    if query and query[0] in sys_mode_set and query[1:]:
        attr, value, value_type = sys_mode_set[query[0]]['attr'], query[1:], sys_mode_set[query[0]]['type']
        
        if value_type == 'int':
            if value.isdigit():
                return attr, value
            else:
                return None, None
        else:
            return attr, value

    return None, None
    
def main(wf: Workflow3):
    qr = QueryDB(wf)
    
    if sys_args:
        query = sys_args[0]
        attr, value = _parse_query(query)
        if attr:
            setattr(qr, attr, value)
        
    qr.parse_result()
    wf.send_feedback()

if __name__ == '__main__':
    sys.exit(wf.run(main))