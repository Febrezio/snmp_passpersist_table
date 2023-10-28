import snmp_passpersist as snmp

from snmp_table import SnmpTable

table_oid = '.1.3.6.1.3.53.8'  # Some table OID
row_status_column_oid = table_oid + '1.3'
row_oids = []


def update():
    row_oid = '1'
    pp.add_int('1.1.' + row_oid, 123)
    pp.add_int('1.2.' + row_oid, 4)
    pp.add_int('1.3.' + row_oid, 1)  # MAC address as an octet string
    row_oids.append(row_oid)


pp = snmp.PassPersist(table_oid)
table = SnmpTable(table_oid, row_status_column_oid, row_oids)
# Add setter for entry OID
pp.register_setter(table_oid, table.set)
pp.start(update, 1800)  # Every 30 minutes
