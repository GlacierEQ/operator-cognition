import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cognition_engine import CognitionEngine

class TestRouteGeneration(unittest.TestCase):
    def setUp(self):
        contract = {
            "contract_id": "rc_001",
            "agent_genome_ref": "OA.EMAIL.12",
            "epistemic_mode": "EXECUTION",
            "rationale_limit_words": 50,
            "prohibited_cognitive_patterns": ["raw_cot"]
        }
        self.engine = CognitionEngine(contract)

    def test_route_generation_structure(self):
        route_plan = self.engine.generate_route("Deploy application to production", ["git", "docker"])
        
        self.assertIn("generation_id", route_plan)
        self.assertEqual(route_plan["target_objective"], "Deploy application to production")
        self.assertIn("primary_route", route_plan)
        self.assertIn("steps", route_plan["primary_route"])
        self.assertIn("fallback_routes", route_plan)

    def test_decision_record_rationale_enforcement(self):
        # Should raise error if raw chain-of-thought is passed
        with self.assertRaises(ValueError) as context:
            self.engine.record_decision(
                "mission_xyz", 
                "primary_route", 
                ["alternative_1"], 
                "This is a raw_cot dump containing unrefined thinking..."
            )
        self.assertTrue("Prohibited cognitive pattern detected" in str(context.exception))

    def test_valid_decision_record(self):
        record = self.engine.record_decision(
            "mission_xyz", 
            "primary_route", 
            ["alternative_1"], 
            "Selected primary route due to direct dependency satisfaction."
        )
        self.assertEqual(record["selected_route"], "primary_route")
        self.assertNotIn("raw_cot", record["concise_rationale"])
        self.assertIsNotNone(record["context_hash"])

if __name__ == '__main__':
    unittest.main()
