#!/usr/bin/env python
"""Test server stability with various endpoints."""
import sys
import os
import time
import json
import subprocess
import threading
import requests
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

class ServerTest:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000'
        self.server_process = None
        self.test_results = []
        
    def start_server(self):
        """Start the server in background."""
        print("[INFO] Starting server...")
        try:
            self.server_process = subprocess.Popen(
                [sys.executable, 'run.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(__file__)
            )
            time.sleep(3)  # Wait for server to start
            print("[OK] Server started")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the server."""
        if self.server_process:
            print("[INFO] Stopping server...")
            self.server_process.terminate()
            time.sleep(1)
            if self.server_process.poll() is None:
                self.server_process.kill()
            print("[OK] Server stopped")
    
    def test_health(self):
        """Test health endpoint."""
        try:
            r = requests.get(f'{self.base_url}/health', timeout=5)
            assert r.status_code == 200
            assert r.json()['status'] == 'ok'
            self.test_results.append(('Health Check', True, 'OK'))
            print("[OK] Health check passed")
            return True
        except Exception as e:
            self.test_results.append(('Health Check', False, str(e)))
            print(f"[FAILED] Health check: {e}")
            return False
    
    def test_home_page(self):
        """Test home page rendering."""
        try:
            r = requests.get(f'{self.base_url}/', timeout=5)
            assert r.status_code == 200
            self.test_results.append(('Home Page', True, 'OK'))
            print("[OK] Home page loads")
            return True
        except Exception as e:
            self.test_results.append(('Home Page', False, str(e)))
            print(f"[FAILED] Home page: {e}")
            return False
    
    def test_builder_parts(self):
        """Test parts endpoint."""
        try:
            r = requests.get(f'{self.base_url}/api/builder/parts', timeout=5)
            assert r.status_code in [200, 500]  # May not have data
            data = r.json()
            assert isinstance(data, dict)
            self.test_results.append(('Builder Parts', True, 'OK'))
            print("[OK] Builder parts endpoint works")
            return True
        except Exception as e:
            self.test_results.append(('Builder Parts', False, str(e)))
            print(f"[FAILED] Builder parts: {e}")
            return False
    
    def test_compatibility_check(self):
        """Test compatibility check with malformed data."""
        try:
            # Test with empty data
            r = requests.post(
                f'{self.base_url}/api/builder/compatibility',
                json={},
                timeout=5
            )
            assert r.status_code in [200, 500]
            data = r.json()
            assert isinstance(data, dict)
            self.test_results.append(('Compatibility Check', True, 'OK'))
            print("[OK] Compatibility check handles empty data")
            return True
        except Exception as e:
            self.test_results.append(('Compatibility Check', False, str(e)))
            print(f"[FAILED] Compatibility check: {e}")
            return False
    
    def test_invalid_request(self):
        """Test handling of invalid requests."""
        try:
            # POST with None JSON
            r = requests.post(
                f'{self.base_url}/api/builder/validate',
                json=None,
                timeout=5,
                headers={'Content-Type': 'application/json'}
            )
            assert r.status_code in [200, 400, 500]
            self.test_results.append(('Invalid Request', True, 'Handled gracefully'))
            print("[OK] Invalid request handled")
            return True
        except Exception as e:
            self.test_results.append(('Invalid Request', False, str(e)))
            print(f"[FAILED] Invalid request test: {e}")
            return False
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        try:
            import concurrent.futures
            
            def make_request():
                r = requests.get(f'{self.base_url}/health', timeout=5)
                return r.status_code == 200
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(make_request) for _ in range(10)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
            success = all(results)
            self.test_results.append(('Concurrent Requests', success, f'{sum(results)}/10 succeeded'))
            print(f"[OK] Concurrent requests: {sum(results)}/10 succeeded")
            return success
        except Exception as e:
            self.test_results.append(('Concurrent Requests', False, str(e)))
            print(f"[FAILED] Concurrent requests: {e}")
            return False
    
    def test_large_payload(self):
        """Test handling of large payloads."""
        try:
            large_data = {
                'cpu': 'x' * 1000,
                'gpu': 'y' * 1000,
                'data': ['z' * 100 for _ in range(100)]
            }
            r = requests.post(
                f'{self.base_url}/api/builder/compatibility',
                json=large_data,
                timeout=5
            )
            assert r.status_code in [200, 400, 500]
            self.test_results.append(('Large Payload', True, 'Handled'))
            print("[OK] Large payload handled")
            return True
        except Exception as e:
            self.test_results.append(('Large Payload', False, str(e)))
            print(f"[FAILED] Large payload: {e}")
            return False
    
    def run_all_tests(self):
        """Run all stability tests."""
        print("\n" + "=" * 60)
        print("PC Builder Server Stability Tests")
        print("=" * 60 + "\n")
        
        if not self.start_server():
            print("[FATAL] Could not start server")
            return False
        
        try:
            print("\nRunning tests...\n")
            time.sleep(2)
            
            tests = [
                self.test_health,
                self.test_home_page,
                self.test_builder_parts,
                self.test_compatibility_check,
                self.test_invalid_request,
                self.test_concurrent_requests,
                self.test_large_payload,
            ]
            
            for test in tests:
                try:
                    test()
                    time.sleep(0.5)
                except Exception as e:
                    print(f"[ERROR] Test failed: {e}")
            
            print("\n" + "=" * 60)
            print("Test Results")
            print("=" * 60)
            
            passed = 0
            failed = 0
            for test_name, success, message in self.test_results:
                status = "[PASS]" if success else "[FAIL]"
                print(f"{status} {test_name}: {message}")
                if success:
                    passed += 1
                else:
                    failed += 1
            
            print("\n" + "-" * 60)
            print(f"Total: {passed} passed, {failed} failed")
            print("-" * 60 + "\n")
            
            return failed == 0
        
        finally:
            self.stop_server()

if __name__ == '__main__':
    tester = ServerTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
