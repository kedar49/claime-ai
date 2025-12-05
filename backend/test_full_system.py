#!/usr/bin/env python3
"""
Claime AI Full System Test Suite

Run all tests: uv run python test_full_system.py
"""

import os
import sys
import unittest

# Ensure we can import from the project
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestEnvironment(unittest.TestCase):
    """Test 1: Environment Setup"""
    
    def test_env_file_exists(self):
        """Check .env file exists"""
        self.assertTrue(os.path.exists('.env'), "Missing .env file")
        print("✅ .env file exists")
    
    def test_google_api_key(self):
        """Check Google API key is set"""
        from dotenv import load_dotenv
        load_dotenv()
        key = os.getenv("GOOGLE_API_KEY")
        self.assertIsNotNone(key, "GOOGLE_API_KEY not set in .env")
        self.assertTrue(len(key) > 10, "GOOGLE_API_KEY looks invalid")
        print("✅ GOOGLE_API_KEY is set")
    
    def test_tavily_api_key(self):
        """Check Tavily API key is set"""
        from dotenv import load_dotenv
        load_dotenv()
        key = os.getenv("TAVILY_API_KEY")
        self.assertIsNotNone(key, "TAVILY_API_KEY not set in .env")
        self.assertTrue(len(key) > 10, "TAVILY_API_KEY looks invalid")
        print("✅ TAVILY_API_KEY is set")


class TestAgents(unittest.TestCase):
    """Test 2: AI Agents"""
    
    @classmethod
    def setUpClass(cls):
        from dotenv import load_dotenv
        load_dotenv()
    
    def test_fact_checker_import(self):
        """Test Fact Checker agent can be imported"""
        from agents.fact_checker import FactChecker
        agent = FactChecker()
        self.assertIsNotNone(agent, "Should create agent")
        print("✅ Fact Checker agent imports correctly")
    
    def test_forensic_expert_import(self):
        """Test Forensic Expert agent can be imported"""
        from agents.forensic_expert import ForensicExpert
        agent = ForensicExpert()
        self.assertIsNotNone(agent, "Should create agent")
        print("✅ Forensic Expert agent imports correctly")
    
    def test_judge_import(self):
        """Test Judge agent can be imported"""
        from agents.judge import TheJudge
        agent = TheJudge()
        self.assertIsNotNone(agent, "Should create agent")
        print("✅ Judge agent imports correctly")


class TestEndToEnd(unittest.TestCase):
    """Test 3: End-to-End Pipeline Test"""
    
    def test_full_pipeline_dry_run(self):
        """Test the full pipeline can be initialized"""
        from dotenv import load_dotenv
        load_dotenv()
        
        # Import main components
        from agents.fact_checker import FactChecker
        from agents.forensic_expert import ForensicExpert
        from agents.judge import TheJudge
        
        # Initialize all components
        fact_checker = FactChecker()
        forensic_expert = ForensicExpert()
        judge = TheJudge()
        
        print("✅ All pipeline components initialized successfully")
        print("   - Fact Checker: Ready")
        print("   - Forensic Expert: Ready")
        print("   - Judge: Ready")


def run_tests():
    """Run all tests with nice output"""
    print("\n" + "="*70)
    print("🛡️  Claime AI - Full System Test Suite")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes in order
    test_classes = [
        TestEnvironment,
        TestAgents,
        TestEndToEnd,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("📊 Test Summary")
    print("="*70)
    print(f"   Tests Run: {result.testsRun}")
    print(f"   ✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   ❌ Failed: {len(result.failures)}")
    print(f"   ⚠️  Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result


if __name__ == "__main__":
    # Allow running specific test class
    if len(sys.argv) > 1:
        # Run specific test class
        unittest.main(verbosity=2)
    else:
        # Run all tests
        result = run_tests()
        sys.exit(0 if result.wasSuccessful() else 1)
