#!/usr/bin/env python3
"""Quick test of video_editing domain."""
import sys
sys.path.insert(0, '.')

from server.services.pc_build_agent import PCBuildAgent

result = PCBuildAgent.generate_build('video_editing', 75000)
print(f"Success: {result['success']}")
if result['success']:
    print(f"GPU: {result['parts'].get('gpu', {}).get('name')}")
    print(f"Total: {result['parts']}")
