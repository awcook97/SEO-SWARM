import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import measurement_intake_generator


class MeasurementIntakeGeneratorTests(unittest.TestCase):
    def test_scaffold_and_render(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "measurement-intake-input.json"
            measurement_intake_generator.scaffold_input(path)
            data = measurement_intake_generator.load_input(path)
            md = measurement_intake_generator.render_markdown(data)
            self.assertIn("Measurement intake", md)
            self.assertIn("Primary services", md)

    def test_missing_file_error(self):
        with self.assertRaises(SystemExit):
            measurement_intake_generator.load_input(Path("nonexistent.json"))


if __name__ == "__main__":
    unittest.main()
