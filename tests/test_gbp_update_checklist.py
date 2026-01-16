import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import gbp_update_checklist


SAMPLE_INPUTS = """
# Sample - Approved Inputs

## Approved business facts

- Business name: Sample HVAC
- Website: https://example.com
- Phone: (555) 111-2222
- Email: info@example.com
- Address:
  - Line 1: 123 Main St
  - City: Denver
  - State: CO
  - Postal code: 80202
  - Country: US
- Hours:
  - Monday: 8 AM-5 PM
  - Tuesday: 8 AM-5 PM
- Areas served (verified list):
  - Denver
  - Boulder

## Approved profile details

- Short description: Short desc.
- Long description: Long desc.
- Keywords (approved list): heating, cooling
- Price range: $$
- Payment forms: Cash, Visa
- Social:
  - Facebook: https://facebook.com/sample

## Approved service list (descriptions)

- Heating: Heating service description.
- Cooling: Cooling service description.
"""


class GbpUpdateChecklistTests(unittest.TestCase):
    def test_parse_inputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "inputs.md"
            path.write_text(SAMPLE_INPUTS, encoding="utf-8")

            parsed = gbp_update_checklist.parse_inputs(path)

            self.assertEqual(parsed.business_name, "Sample HVAC")
            self.assertEqual(parsed.website, "https://example.com")
            self.assertEqual(parsed.phone, "(555) 111-2222")
            self.assertEqual(parsed.address.get("City"), "Denver")
            self.assertEqual(parsed.hours.get("Monday"), "8 AM-5 PM")
            self.assertIn("Denver", parsed.service_areas)
            self.assertEqual(parsed.short_description, "Short desc.")
            self.assertIn("heating", parsed.keywords)
            self.assertEqual(parsed.price_range, "$$")
            self.assertEqual(len(parsed.services), 2)

    def test_post_plan_rotation(self):
        inputs = gbp_update_checklist.ApprovedInputs(
            service_areas=["Denver", "Boulder"],
            services=[{"name": "Heating", "description": ""}],
        )
        plan = gbp_update_checklist.build_post_plan(inputs, count=3)
        self.assertEqual(plan[0]["area"], "Denver")
        self.assertEqual(plan[1]["area"], "Boulder")
        self.assertEqual(plan[2]["service"], "Heating")


if __name__ == "__main__":
    unittest.main()
