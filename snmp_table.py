import re
import sys


class SnmpTable:

    def __init__(self, table_oid, row_status_column_oid, row_oids):
        self.table_oid = table_oid
        self.row_status_column_oid = row_status_column_oid
        self.row_oids = row_oids

    def parse_row_oid(self, oid):
        return re.sub(re.escape(r'' + self.table_oid) + r'\.1\.\d+\.', '', oid)

    def set(self, oid, type_value):
        index = 0
        current_oid = oid
        current_type_value = type_value
        print(f'oid[{index}] = ' + current_oid)
        print(f'type_value[{index}] = ' + current_type_value)
        current_row_oid = self.parse_row_oid(current_oid)
        print(f'row_oid[{index}] = ' + current_row_oid)

        # If the row OID already exists then only support single OID SET request
        if current_row_oid in self.row_oids:
            return True
        else:
            while not current_oid.startswith(self.row_status_column_oid):
                current_oid = sys.stdin.readline().strip()
                current_type_value = sys.stdin.readline().strip()
                current_type = current_type_value.split()[0]
                current_value = current_type_value.lstrip(current_type).strip().strip('"')
                index += 1
                print(f'oid[{index}] = ' + current_oid)
                print(f'type_value[{index}] = ' + current_type_value)
                pp.add_oid_entry(current_oid, current_type, current_value)
