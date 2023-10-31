import re
import sys
import snmp_passpersist as snmp


class SnmpTable:

    def __init__(self, table_oid, row_status_column_oid, row_oids=None, pp=None):
        if row_oids is None:
            row_oids = []
        self.pp = pp
        self.table_oid = table_oid
        self.row_status_column_oid = row_status_column_oid
        self.row_oids = row_oids

    def parse_row_oid(self, oid):
        return re.sub(re.escape(r'' + self.table_oid) + r'\.1\.\d+\.', '', oid)

    def parse_sub_index(self, oid):
        return re.sub(re.escape(r'' + self.table_oid) + r'\.', '', oid)

    def set(self, oid, type_, value):
        index = 0
        current_oid = oid
        current_type = type_
        current_value = value
        print(f'oid[{index}] = ' + current_oid)
        print(f'type[{index}] = ' + current_type)
        print(f'value[{index}] = ' + current_value)
        current_row_oid = self.parse_row_oid(current_oid)
        print(f'row_oid[{index}] = ' + current_row_oid)
        print(f'row_status_column_oid = {self.row_status_column_oid}')

        if current_row_oid not in self.row_oids:
            self.row_oids.append(current_row_oid)
            self.set_oid_value(self.parse_sub_index(current_oid), current_type, current_value)
            while not current_oid.startswith(self.row_status_column_oid):
                current_oid = sys.stdin.readline().strip()
                current_type_value = sys.stdin.readline().strip()
                current_type = current_type_value.split()[0]
                current_value = current_type_value.lstrip(current_type).strip().strip('"')
                index += 1
                print(f'oid[{index}] = ' + current_oid)
                print(f'type[{index}] = ' + current_type)
                print(f'value[{index}] = ' + current_value)
                self.set_oid_value(self.parse_sub_index(current_oid), current_type, current_value)
            # Commit requires all current MIB table entries be added to pending, else they will be overwritten
            self.pp.pending.update(self.pp.data)
            self.pp.commit()
            print('Done handling rows...')
        # If the row OID does not exist then just return default response
        return True

    def set_oid_value(self, oid, type_, value):
        print(f'Adding OID entry {oid} to table {self.table_oid} with value {value}')
        if snmp.Type.Integer == type_.lower():
            self.pp.add_int(oid, value)
        elif snmp.Type.String == type_.lower():
            self.pp.add_str(oid, value)
        elif snmp.Type.Octet == type_.lower():
            self.pp.add_oct(oid, value)
        elif snmp.Type.IPAddress == type_.lower():
            self.pp.add_ip(oid, value)
        elif snmp.Type.TimeTicks == type_.lower():
            self.pp.add_tt(oid, value)
        elif snmp.Type.Counter == type_.lower():
            self.pp.add_cnt_64bit(oid, value)
        elif snmp.Type.Gauge == type_.lower():
            self.pp.add_gau(oid, value)
        elif snmp.Type.ObjectID == type_.lower():
            self.pp.add_oid(oid, value)
        elif snmp.Type.OID == type_.lower():
            self.pp.add_oid(oid, value)
        else:
            raise ValueError(f'MIB object type not supported: {type_}')
