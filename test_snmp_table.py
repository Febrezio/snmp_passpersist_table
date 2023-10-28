from unittest import TestCase

from snmp_table import SnmpTable

table_oid = '.1.3.6.1.3.53.8'  # Some table OID
row_status_column_oid = table_oid + '1.3'
snmp_table = SnmpTable(table_oid, row_status_column_oid)


class Test(TestCase):
    def test_parse_row_oid(self):
        row_oid = snmp_table.parse_row_oid('.1.3.6.1.3.53.8.1.1.1')
        self.assertEqual('1', row_oid)
