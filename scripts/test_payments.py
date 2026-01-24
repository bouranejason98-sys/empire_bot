#!/usr/bin/env python3
"""
Payment Sandbox Test Script
Tests all payment providers in sandbox mode before production
"""

import asyncio
import requests
from datetime import datetime

class PaymentSandboxTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = []
    
    async def test_mpesa_stk_push(self):
        """Test M-Pesa STK Push"""
        try:
            response = requests.post(
                f"{self.base_url}/payments/mpesa/stk-push",
                json={
                    "phone": "254700000000",  # Test number
                    "amount": 10,
                    "reference": f"TEST_{datetime.now().timestamp()}",
                    "callback_url": f"{self.base_url}/webhooks/mpesa"
                },
                headers={"Authorization": "Bearer sandbox_token"}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"M-Pesa test failed: {e}")
            return False
    
    async def test_tron_transfer(self):
        """Test TRON USDT transfer"""
        try:
            response = requests.post(
                f"{self.base_url}/payments/tron/transfer",
                json={
                    "to_address": "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb",
                    "amount": 0.1,
                    "token": "USDT"
                }
            )
            return response.status_code == 200
        except Exception as e:
            print(f"TRON test failed: {e}")
            return False
    
    async def test_fraud_detection(self):
        """Test fraud detection system"""
        try:
            # Test with suspicious transaction
            response = requests.post(
                f"{self.base_url}/payments/validate",
                json={
                    "sender": "test_fraud@example.com",
                    "amount": 100000,
                    "frequency": 100
                }
            )
            data = response.json()
            return data.get("is_fraudulent", False) == True
        except Exception as e:
            print(f"Fraud test failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all payment tests"""
        print("🚀 Starting Payment Sandbox Tests...")
        
        tests = [
            ("M-Pesa STK Push", self.test_mpesa_stk_push),
            ("TRON Transfer", self.test_tron_transfer),
            ("Fraud Detection", self.test_fraud_detection)
        ]
        
        for name, test_func in tests:
            result = await test_func()
            self.results.append((name, result))
            print(f"✅ {name}: {'PASS' if result else 'FAIL'}")
        
        # Generate report
        passed = sum(1 for _, result in self.results if result)
        total = len(self.results)
        
        print(f"\n📊 Test Results: {passed}/{total} passed")
        
        if passed == total:
            print("🎉 All tests passed! Ready for production.")
            return True
        else:
            print("⚠️ Some tests failed. Check configuration.")
            return False

if __name__ == "__main__":
    tester = PaymentSandboxTester()
    asyncio.run(tester.run_all_tests())
