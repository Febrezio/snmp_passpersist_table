from unittest import TestCase

from snmp_table import SnmpTable
import snmp_passpersist as snmp

table_oid = '.1.3.6.1.3.53.8'  # Some table OID
row_status_column_oid = table_oid + '.1.3'
pp = snmp.PassPersist(table_oid)
snmp_table = SnmpTable(table_oid, row_status_column_oid, pp=pp)


class TestSnmpTable(TestCase):

    def test_parse_row_oid(self):
        row_oid = snmp_table.parse_row_oid('.1.3.6.1.3.53.8.1.1.1')
        self.assertEqual('1', row_oid)

    def test_set_oid_value(self):
        snmp_table.set_oid_value('1.1.1', snmp.Type.Integer, 1)

    def test_set_oid_value_exception(self):
        try:
            snmp_table.set_oid_value('1.1.1', 'BOGUS', 1)
            self.fail('Expected ValueError exception.')
        except ValueError:
            print('GOOD')
