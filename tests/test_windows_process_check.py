import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from fl_studio_mcp_server import FLStudioTrigger


class WindowsProcessCheckTests(unittest.TestCase):
    def setUp(self):
        self.trigger = FLStudioTrigger()
        self.trigger.system = "Windows"

    @patch("fl_studio_mcp_server.subprocess.run")
    @patch("ctypes.windll", create=True)
    def test_uses_tasklist_from_windows_system_directory(self, windll, run):
        system_directory = Path(sys.executable).parent / "system directory"

        def get_system_directory(buffer, capacity):
            self.assertEqual(capacity, len(buffer))
            buffer.value = str(system_directory)
            return len(buffer.value)

        windll.kernel32.GetSystemDirectoryW.side_effect = get_system_directory
        run.return_value.stdout = "FL.exe"

        self.assertTrue(self.trigger._is_fl_studio_running())
        run.assert_called_once_with(
            [str(system_directory / "tasklist.exe"), "/FI", "IMAGENAME eq FL.exe"],
            capture_output=True,
            text=True,
        )

        run.return_value.stdout = "INFO: No tasks are running which match the specified criteria."
        self.assertFalse(self.trigger._is_fl_studio_running())

    @patch("fl_studio_mcp_server.subprocess.run")
    @patch("ctypes.windll", create=True)
    def test_unavailable_system_directory_stops_before_subprocess(self, windll, run):
        for length in (0, 260):
            with self.subTest(length=length):
                windll.kernel32.GetSystemDirectoryW.return_value = length
                self.assertFalse(self.trigger._is_fl_studio_running())
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
