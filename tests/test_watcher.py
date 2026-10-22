
import unittest
from unittest.mock import patch

from watcher import IntegrityEventHandler


class TestPeriodicScan(unittest.TestCase):

    def test_periodic_scan_calls_integrity_check(self):
        handler = IntegrityEventHandler("documents", {})

        with patch("watcher.check_integrity") as mock_check:
            handler.run_integrity_check()

        mock_check.assert_called_once_with("documents", {})


if __name__ == "__main__":
    unittest.main()
