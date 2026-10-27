"""Validate the published CV with Poppler (pdfinfo and pdftotext)."""
from pathlib import Path
import re
import shutil
import subprocess
import unittest

PDF = Path(__file__).resolve().parents[1] / "asset/cv/cv_mattia_fait.pdf"


@unittest.skipUnless(shutil.which("pdfinfo") and shutil.which("pdftotext"),
                     "CV validation requires Poppler: pdfinfo and pdftotext")
class CVTests(unittest.TestCase):
    def test_single_a4_page(self):
        info = subprocess.run(["pdfinfo", str(PDF)], check=True,
                              capture_output=True, text=True).stdout
        self.assertRegex(info, r"(?m)^Pages:\s+1\s*$")
        self.assertRegex(info, r"(?m)^Page size:.*\(A4\)")

    def test_readable_text_and_contract_profile(self):
        text = subprocess.run(["pdftotext", str(PDF), "-"], check=True,
                              capture_output=True, text=True).stdout
        text = re.sub(r"\s+", " ", text)
        for expected in ("Mattia Fait", "Linux Systems", "freelance contracts",
                         "BSc in progress", "Selected systems projects", "Languages",
                         "https://github.com/4137314/nixos-config",
                         "https://github.com/4137314/hack-workspace"):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        self.assertNotIn("\ufffd", text)


if __name__ == "__main__":
    unittest.main()
