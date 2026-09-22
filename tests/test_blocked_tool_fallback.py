import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cognition_engine import CognitionEngine

class TestBlockedToolFallback(unittest.TestCase):
    def setUp(self):
        contract = {
            "contract_id": "rc_002",
            "agent_genome_ref": "OA.EMAIL.12",
            "epistemic_mode": "EXECUTION",
            "rationale_limit_words": 100,
            "prohibited_cognitive_patterns": ["raw_cot"]
        }
        self.engine = CognitionEngine(contract)

    def test_fallback_route_trigger(self):
        route_plan = self.engine.generate_route("Automated email send", ["smtp"])
        
        fallback_routes = route_plan["fallback_routes"]
        self.assertTrue(len(fallback_routes) > 0)
        
        # Ensure that fallback is specifically triggered when blocked
        blocked_trigger_found = any(f["trigger_condition"] == "tool_blocked" for f in fallback_routes)
        self.assertTrue(blocked_trigger_found, "Engine must generate a tool_blocked fallback route.")

if __name__ == '__main__':
    unittest.main()
