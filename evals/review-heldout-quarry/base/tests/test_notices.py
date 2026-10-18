import tempfile
import unittest

from blastplan import notices
from blastplan.notices import NoticeError
from tests.support import blast, make_config, utc


class NoticesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = make_config(outbox=self.tmp.name)

    def test_notice_lead(self):
        b = blast("B1", utc(2030, 6, 18, 11))
        self.assertEqual(notices.notice_lead(b, utc(2030, 6, 17, 9)), 26)

    def test_one_notice_per_receptor(self):
        b = blast("B1", utc(2030, 6, 18, 11))
        paths = notices.issue_notices(b, self.cfg, utc(2030, 6, 17, 9))
        self.assertEqual([p.name for p in paths], ["notice-B1-R1.txt", "notice-B1-R2.txt"])
        self.assertIn("Tuesday 18 June 2030 at 11:00", paths[0].read_text(encoding="utf-8"))

    def test_short_notice_refused(self):
        b = blast("B1", utc(2030, 6, 18, 11))
        with self.assertRaises(NoticeError):
            notices.issue_notices(b, self.cfg, utc(2030, 6, 17, 12))

    def test_notice_is_not_rewritten(self):
        b = blast("B1", utc(2030, 6, 18, 11))
        notices.issue_notices(b, self.cfg, utc(2030, 6, 17, 9))
        with self.assertRaises(NoticeError):
            notices.issue_notices(b, self.cfg, utc(2030, 6, 17, 9))


if __name__ == "__main__":
    unittest.main()
