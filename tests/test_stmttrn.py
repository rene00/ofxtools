# coding: utf-8

# stdlib imports
import unittest
from datetime import datetime
from decimal import Decimal
from xml.etree.ElementTree import (
    Element,
    SubElement,
)


# local imports
from . import common
from ofxtools.models import (
    Aggregate,
    STMTTRNRS, STMTTRN,
    STATUS,
    PAYEE,
    BANKACCTFROM, BANKACCTTO, CCACCTTO,
    BANKTRANLIST, BALLIST,
    LEDGERBAL, AVAILBAL,

)


class StmttrnTestCase(unittest.TestCase, common.TestAggregate):
    """ STMTTRN with CURRENCY """
    __test__ = True
    requiredElements = ('DTPOSTED', 'TRNAMT', 'FITID', 'TRNTYPE',)
    optionalElements = ('DTUSER', 'DTAVAIL', 'CORRECTFITID', 'CORRECTACTION',
                        'SRVRTID', 'CHECKNUM', 'REFNUM', 'SIC', 'PAYEEID',
                        'NAME', 'MEMO', 'INV401KSOURCE', 'CURSYM', 'CURRATE',)

    @property
    def root(self):
        root = Element('STMTTRN')
        SubElement(root, 'TRNTYPE').text = 'CHECK'
        SubElement(root, 'DTPOSTED').text = '20130615'
        SubElement(root, 'DTUSER').text = '20130614'
        SubElement(root, 'DTAVAIL').text = '20130616'
        SubElement(root, 'TRNAMT').text = '-433.25'
        SubElement(root, 'FITID').text = 'DEADBEEF'
        SubElement(root, 'CORRECTFITID').text = 'B00B5'
        SubElement(root, 'CORRECTACTION').text = 'REPLACE'
        SubElement(root, 'SRVRTID').text = '101A2'
        SubElement(root, 'CHECKNUM').text = '101'
        SubElement(root, 'REFNUM').text = '5A6B'
        SubElement(root, 'SIC').text = '171103'
        SubElement(root, 'PAYEEID').text = '77810'
        SubElement(root, 'NAME').text = 'Tweet E. Bird'
        SubElement(root, 'MEMO').text = 'Protection money'
        currency = SubElement(root, 'CURRENCY')
        SubElement(currency, 'CURSYM').text = 'CAD'
        SubElement(currency, 'CURRATE').text = '1.1'
        SubElement(root, 'INV401KSOURCE').text = 'PROFITSHARING'
        return root

    def testConvert(self):
        root = Aggregate.from_etree(self.root)
        self.assertIsInstance(root, STMTTRN)
        self.assertEqual(root.trntype, 'CHECK')
        self.assertEqual(root.dtposted, datetime(2013, 6, 15))
        self.assertEqual(root.dtuser, datetime(2013, 6, 14))
        self.assertEqual(root.dtavail, datetime(2013, 6, 16))
        self.assertEqual(root.trnamt, Decimal('-433.25'))
        self.assertEqual(root.fitid, 'DEADBEEF')
        self.assertEqual(root.correctfitid, 'B00B5')
        self.assertEqual(root.correctaction, 'REPLACE')
        self.assertEqual(root.srvrtid, '101A2')
        self.assertEqual(root.checknum, '101')
        self.assertEqual(root.refnum, '5A6B')
        self.assertEqual(root.sic, 171103)
        self.assertEqual(root.payeeid, '77810')
        self.assertEqual(root.name, 'Tweet E. Bird')
        self.assertEqual(root.memo, 'Protection money')
        self.assertEqual(root.curtype, 'CURRENCY')
        self.assertEqual(root.cursym, 'CAD')
        self.assertEqual(root.currate, Decimal('1.1'))
        self.assertEqual(root.inv401ksource, 'PROFITSHARING')


class StmttrnOrigcurrencyTestCase(StmttrnTestCase):
    """ STMTTRN with ORIGCURRENCY """
    @property
    def root(self):
        root = super(self.__class__, self).root

        currency = root.find('CURRENCY')
        currency.tag = 'ORIGCURRENCY'

        return root

    def testConvert(self):
        root = Aggregate.from_etree(self.root)
        self.assertIsInstance(root, STMTTRN)
        self.assertEqual(root.trntype, 'CHECK')
        self.assertEqual(root.dtposted, datetime(2013, 6, 15))
        self.assertEqual(root.dtuser, datetime(2013, 6, 14))
        self.assertEqual(root.dtavail, datetime(2013, 6, 16))
        self.assertEqual(root.trnamt, Decimal('-433.25'))
        self.assertEqual(root.fitid, 'DEADBEEF')
        self.assertEqual(root.correctfitid, 'B00B5')
        self.assertEqual(root.correctaction, 'REPLACE')
        self.assertEqual(root.srvrtid, '101A2')
        self.assertEqual(root.checknum, '101')
        self.assertEqual(root.refnum, '5A6B')
        self.assertEqual(root.sic, 171103)
        self.assertEqual(root.payeeid, '77810')
        self.assertEqual(root.name, 'Tweet E. Bird')
        self.assertEqual(root.memo, 'Protection money')
        self.assertEqual(root.curtype, 'ORIGCURRENCY')
        self.assertEqual(root.cursym, 'CAD')
        self.assertEqual(root.currate, Decimal('1.1'))
        self.assertEqual(root.inv401ksource, 'PROFITSHARING')


class StmttrnPayeeTestCase(StmttrnTestCase):
    """ STMTTRN with PAYEE """
    requiredElements = ('DTPOSTED', 'TRNAMT', 'FITID', 'TRNTYPE', 'NAME',
                        'ADDR1', 'CITY', 'STATE', 'POSTALCODE', 'PHONE',)
    optionalElements = ('DTUSER', 'DTAVAIL', 'CORRECTFITID', 'CORRECTACTION',
                        'SRVRTID', 'CHECKNUM', 'REFNUM', 'SIC', 'PAYEEID',
                        'MEMO', 'INV401KSOURCE', 'CURSYM', 'CURRATE', 'ADDR2',
                        'ADDR3', 'COUNTRY',)

    @property
    def root(self):
        root = super(self.__class__, self).root

        name = root.find('NAME')
        root.remove(name)

        payee = SubElement(root, 'PAYEE')
        SubElement(payee, 'NAME').text = 'Wrigley Field'
        SubElement(payee, 'ADDR1').text = '3717 N Clark St'
        SubElement(payee, 'ADDR2').text = 'Dugout Box, Aisle 19'
        SubElement(payee, 'ADDR3').text = 'Seat A1'
        SubElement(payee, 'CITY').text = 'Chicago'
        SubElement(payee, 'STATE').text = 'IL'
        SubElement(payee, 'POSTALCODE').text = '60613'
        SubElement(payee, 'COUNTRY').text = 'USA'
        SubElement(payee, 'PHONE').text = '(773) 309-1027'

        return root

    def testConvert(self):
        root = Aggregate.from_etree(self.root)
        self.assertIsInstance(root, STMTTRN)
        self.assertEqual(root.trntype, 'CHECK')
        self.assertEqual(root.dtposted, datetime(2013, 6, 15))
        self.assertEqual(root.dtuser, datetime(2013, 6, 14))
        self.assertEqual(root.dtavail, datetime(2013, 6, 16))
        self.assertEqual(root.trnamt, Decimal('-433.25'))
        self.assertEqual(root.fitid, 'DEADBEEF')
        self.assertEqual(root.correctfitid, 'B00B5')
        self.assertEqual(root.correctaction, 'REPLACE')
        self.assertEqual(root.srvrtid, '101A2')
        self.assertEqual(root.checknum, '101')
        self.assertEqual(root.refnum, '5A6B')
        self.assertEqual(root.sic, 171103)
        self.assertEqual(root.payeeid, '77810')
        self.assertEqual(root.memo, 'Protection money')
        self.assertEqual(root.curtype, 'CURRENCY')
        self.assertEqual(root.cursym, 'CAD')
        self.assertEqual(root.currate, Decimal('1.1'))
        self.assertEqual(root.inv401ksource, 'PROFITSHARING')
        payee = root.payee
        self.assertIsInstance(payee, PAYEE)
        self.assertEqual(payee.name, 'Wrigley Field')
        self.assertEqual(payee.addr1, '3717 N Clark St')
        self.assertEqual(payee.city, 'Chicago')
        self.assertEqual(payee.state, 'IL')
        self.assertEqual(payee.postalcode, '60613')
        self.assertEqual(payee.phone, '(773) 309-1027')


class StmttrnBankaccttoTestCase(StmttrnTestCase):
    """ STMTTRN with BANKACCTTO """
    requiredElements = ('DTPOSTED', 'TRNAMT', 'FITID', 'TRNTYPE', 'BANKID',
                        'ACCTID', 'ACCTTYPE',)
    optionalElements = ('DTUSER', 'DTAVAIL', 'CORRECTFITID', 'CORRECTACTION',
                        'SRVRTID', 'CHECKNUM', 'REFNUM', 'SIC', 'PAYEEID',
                        'NAME', 'MEMO', 'INV401KSOURCE', 'CURSYM', 'CURRATE',
                        'BRANCHID', 'ACCTKEY',)

    @property
    def root(self):
        root = super(self.__class__, self).root

        bankacctto = SubElement(root, 'BANKACCTTO')
        SubElement(bankacctto, 'BANKID').text = '111000614'
        SubElement(bankacctto, 'BRANCHID').text = 'N/A'
        SubElement(bankacctto, 'ACCTID').text = '9876543210'
        SubElement(bankacctto, 'ACCTTYPE').text = 'CHECKING'
        SubElement(bankacctto, 'ACCTKEY').text = 'NONE'

        return root

    def testConvert(self):
        root = Aggregate.from_etree(self.root)
        self.assertIsInstance(root, STMTTRN)
        self.assertEqual(root.trntype, 'CHECK')
        self.assertEqual(root.dtposted, datetime(2013, 6, 15))
        self.assertEqual(root.dtuser, datetime(2013, 6, 14))
        self.assertEqual(root.dtavail, datetime(2013, 6, 16))
        self.assertEqual(root.trnamt, Decimal('-433.25'))
        self.assertEqual(root.fitid, 'DEADBEEF')
        self.assertEqual(root.correctfitid, 'B00B5')
        self.assertEqual(root.correctaction, 'REPLACE')
        self.assertEqual(root.srvrtid, '101A2')
        self.assertEqual(root.checknum, '101')
        self.assertEqual(root.refnum, '5A6B')
        self.assertEqual(root.sic, 171103)
        self.assertEqual(root.payeeid, '77810')
        self.assertEqual(root.memo, 'Protection money')
        self.assertEqual(root.curtype, 'CURRENCY')
        self.assertEqual(root.cursym, 'CAD')
        self.assertEqual(root.currate, Decimal('1.1'))
        self.assertEqual(root.inv401ksource, 'PROFITSHARING')
        bankacctto = root.bankacctto
        self.assertIsInstance(bankacctto, BANKACCTTO)
        self.assertEqual(bankacctto.bankid, '111000614')
        self.assertEqual(bankacctto.branchid, 'N/A')
        self.assertEqual(bankacctto.acctid, '9876543210')
        self.assertEqual(bankacctto.accttype, 'CHECKING')
        self.assertEqual(bankacctto.acctkey, 'NONE')


class StmttrnCcaccttoTestCase(StmttrnTestCase):
    """ STMTTRN with CCACCTTO """
    requiredElements = ('DTPOSTED', 'TRNAMT', 'FITID', 'TRNTYPE', 'ACCTID')
    optionalElements = ('DTUSER', 'DTAVAIL', 'CORRECTFITID', 'CORRECTACTION',
                        'SRVRTID', 'CHECKNUM', 'REFNUM', 'SIC', 'PAYEEID',
                        'NAME', 'MEMO', 'INV401KSOURCE', 'CURSYM', 'CURRATE',
                        'ACCTKEY',)

    @property
    def root(self):
        root = super(self.__class__, self).root

        ccacctto = SubElement(root, 'CCACCTTO')
        SubElement(ccacctto, 'ACCTID').text = '9876543210'
        SubElement(ccacctto, 'ACCTKEY').text = 'NONE'

        return root

    def testConvert(self):
        root = Aggregate.from_etree(self.root)
        self.assertIsInstance(root, STMTTRN)
        self.assertEqual(root.trntype, 'CHECK')
        self.assertEqual(root.dtposted, datetime(2013, 6, 15))
        self.assertEqual(root.dtuser, datetime(2013, 6, 14))
        self.assertEqual(root.dtavail, datetime(2013, 6, 16))
        self.assertEqual(root.trnamt, Decimal('-433.25'))
        self.assertEqual(root.fitid, 'DEADBEEF')
        self.assertEqual(root.correctfitid, 'B00B5')
        self.assertEqual(root.correctaction, 'REPLACE')
        self.assertEqual(root.srvrtid, '101A2')
        self.assertEqual(root.checknum, '101')
        self.assertEqual(root.refnum, '5A6B')
        self.assertEqual(root.sic, 171103)
        self.assertEqual(root.payeeid, '77810')
        self.assertEqual(root.memo, 'Protection money')
        self.assertEqual(root.curtype, 'CURRENCY')
        self.assertEqual(root.cursym, 'CAD')
        self.assertEqual(root.currate, Decimal('1.1'))
        self.assertEqual(root.inv401ksource, 'PROFITSHARING')
        ccacctto = root.ccacctto
        self.assertIsInstance(ccacctto, CCACCTTO)
        self.assertEqual(ccacctto.acctid, '9876543210')
        self.assertEqual(ccacctto.acctkey, 'NONE')


class StmttrnBankaccttoCcaccttoTestCase(StmttrnTestCase):
    """ STMTTRN with both BANKACCTTO and CCACCTTO - not allowed per OFX spec """
    # required/optional have already been tested in parent; skip here
    requiredElements = ()
    optionalElements = ()

    @property
    def root(self):
        root = super(self.__class__, self).root

        bankacctto = SubElement(root, 'BANKACCTTO')
        SubElement(bankacctto, 'BANKID').text = '111000614'
        SubElement(bankacctto, 'BRANCHID').text = 'N/A'
        SubElement(bankacctto, 'ACCTID').text = '9876543210'
        SubElement(bankacctto, 'ACCTTYPE').text = 'CHECKING'
        SubElement(bankacctto, 'ACCTKEY').text = 'NONE'

        ccacctto = SubElement(root, 'CCACCTTO')
        SubElement(ccacctto, 'ACCTID').text = '9876543210'
        SubElement(ccacctto, 'ACCTKEY').text = 'NONE'

        return root

    def testConvert(self):
        with self.assertRaises(ValueError):
            Aggregate.from_etree(self.root)


class StmttrnNamePayeeTestCase(StmttrnTestCase):
    """ STMTTRN with both NAME and PAYEE - not allowed per OFX spec """
    # required/optional have already been tested in parent; skip here
    requiredElements = ()
    optionalElements = ()

    @property
    def root(self):
        root = super(self.__class__, self).root

        payee = SubElement(root, 'PAYEE')
        SubElement(payee, 'NAME').text = 'Wrigley Field'
        SubElement(payee, 'ADDR1').text = '3717 N Clark St'
        SubElement(payee, 'ADDR2').text = 'Dugout Box, Aisle 19'
        SubElement(payee, 'ADDR3').text = 'Seat A1'
        SubElement(payee, 'CITY').text = 'Chicago'
        SubElement(payee, 'STATE').text = 'IL'
        SubElement(payee, 'POSTALCODE').text = '60613'
        SubElement(payee, 'COUNTRY').text = 'USA'
        SubElement(payee, 'PHONE').text = '(773) 309-1027'

        return root

    def testConvert(self):
        with self.assertRaises(ValueError):
            Aggregate.from_etree(self.root)


class StmttrnCurrencyOrigCurrencyTestCase(StmttrnTestCase):
    """
    STMTTRN with both CURRENCY and ORIGCURRENCY - not allowed per OFX spec
    """
    # required/optional have already been tested in parent; skip here
    requiredElements = ()
    optionalElements = ()

    @property
    def root(self):
        root = super(self.__class__, self).root

        origcurrency = SubElement(root, 'ORIGCURRENCY')
        SubElement(origcurrency, 'CURSYM').text = 'USD'
        SubElement(origcurrency, 'CURRATE').text = '1.0'

        return root

    def testConvert(self):
        with self.assertRaises(ValueError):
            Aggregate.from_etree(self.root)


class StmttrnrsTestCase(StmttrnTestCase):
    """
    """
    requiredElements = ('TRNUID', 'CODE', 'SEVERITY', 'CURDEF',
                        'BANKACCTFROM', 'LEDGERBAL',)
    optionalElements = ('BANKTRANLIST', 'AVAILBAL', 'CASHADVBALAMT', 'INTRATE',
                        'BALLIST', 'MKTGINFO',)

    @property
    def root(self):
        root = Element('STMTTRNRS')
        SubElement(root, 'TRNUID').text = '1001'
        status = SubElement(root, 'STATUS')
        SubElement(status, 'CODE').text = '0'
        SubElement(status, 'SEVERITY').text = 'INFO'
        stmtrs = SubElement(root, 'STMTRS')
        SubElement(stmtrs, 'CURDEF').text = 'USD'
        acctfrom = SubElement(stmtrs, 'BANKACCTFROM')
        SubElement(acctfrom, 'BANKID').text = '111000614'
        SubElement(acctfrom, 'ACCTID').text = '3456789012'
        SubElement(acctfrom, 'ACCTTYPE').text = 'SAVINGS'
        tranlist = SubElement(stmtrs, 'BANKTRANLIST')
        SubElement(tranlist, 'DTSTART').text = '20010601'
        SubElement(tranlist, 'DTEND').text = '20010630'
        stmttrn = super(self.__class__, self).root
        tranlist.append(stmttrn)
        ledgerbal = SubElement(stmtrs, 'LEDGERBAL')
        SubElement(ledgerbal, 'BALAMT').text = '2350.51'
        SubElement(ledgerbal, 'DTASOF').text = '20010630'
        availbal = SubElement(stmtrs, 'AVAILBAL')
        SubElement(availbal, 'BALAMT').text = '13100.00'
        SubElement(availbal, 'DTASOF').text = '20010630'
        SubElement(stmtrs, 'CASHADVBALAMT').text = '10000.00'
        SubElement(stmtrs, 'INTRATE').text = '20.99'
        ballist = SubElement(stmtrs, 'BALLIST')
        bal1 = SubElement(ballist, 'BAL')
        SubElement(bal1, 'NAME').text = 'BAL1'
        SubElement(bal1, 'DESC').text = 'Balance 1'
        SubElement(bal1, 'BALTYPE').text = 'DOLLAR'
        SubElement(bal1, 'VALUE').text = '111.22'
        SubElement(bal1, 'DTASOF').text = '20010630'
        currency = SubElement(bal1, 'CURRENCY')
        SubElement(currency, 'CURRATE').text = '1.0'
        SubElement(currency, 'CURSYM').text = 'USD'
        bal2 = SubElement(ballist, 'BAL')
        SubElement(bal2, 'NAME').text = 'BAL2'
        SubElement(bal2, 'DESC').text = 'Balance 2'
        SubElement(bal2, 'BALTYPE').text = 'PERCENT'
        SubElement(bal2, 'VALUE').text = '1.39'
        SubElement(bal2, 'DTASOF').text = '20010630'
        currency = SubElement(bal2, 'CURRENCY')
        SubElement(currency, 'CURRATE').text = '8.00'
        SubElement(currency, 'CURSYM').text = 'CNY'
        SubElement(stmtrs, 'MKTGINFO').text = 'Get Free Stuff NOW!!'

        return root

    def testConvert(self):
        # Test *TRNRS wrapper and **RS Aggregate.
        # Everything below that is tested elsewhere.
        root = Aggregate.from_etree(self.root)
        self.assertIsInstance(root, STMTTRNRS)
        self.assertEqual(root.trnuid, '1001')
        self.assertIsInstance(root.status, STATUS)
        self.assertEqual(root.curdef, 'USD')
        self.assertIsInstance(root.bankacctfrom, BANKACCTFROM)
        self.assertIsInstance(root.banktranlist, BANKTRANLIST)
        self.assertEqual(len(root.banktranlist), 1)
        self.assertIsInstance(root.ledgerbal, LEDGERBAL)
        self.assertIsInstance(root.availbal, AVAILBAL)
        self.assertIsInstance(root.ballist, BALLIST)
        self.assertEqual(len(root.ballist), 2)

        # Unsupported
        for tag in STMTTRNRS._unsupported:
            self.assertIsNone(getattr(root, tag, None))



if __name__ == '__main__':
    unittest.main()
