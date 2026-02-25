#!/usr/bin/env python3
"""
Quick Test fuer n8n MCP Server.
Testet alle 5 Tools direkt (ohne MCP Protokoll).
"""

import os
import sys
import json

# API Key aus Datei laden
api_key_path = os.path.expanduser("~/.claude/.n8n-api-key")
if os.path.exists(api_key_path):
    with open(api_key_path) as f:
        os.environ.setdefault("N8N_API_KEY", f.read().strip())

from server import workflows_list, workflows_get, executions_list

def run_tests():
    print("=" * 60)
    print("n8n MCP Server — Test")
    print("=" * 60)

    first_workflow_id = None
    first_execution_id = None

    # Test 1: workflows_list
    print("\n[1/3] workflows_list...")
    try:
        result = workflows_list(limit=5)
        data = json.loads(result)
        workflows = data["workflows"]
        print(f"  OK — {data['total']} Workflows (erste 5)")
        for wf in workflows[:3]:
            status = "AKTIV" if wf["active"] else "inaktiv"
            print(f"  - [{wf['id']}] {wf['name']} ({status}, {wf['node_count']} Nodes)")
        if workflows:
            first_workflow_id = workflows[0]["id"]
    except Exception as e:
        print(f"  FEHLER: {e}")

    # Test 2: workflows_get
    if first_workflow_id:
        print(f"\n[2/3] workflows_get ({first_workflow_id})...")
        try:
            result = workflows_get(first_workflow_id)
            wf = json.loads(result)
            print(f"  OK — '{wf['name']}'")
            print(f"  Nodes: {[n['name'] for n in wf['nodes'][:4]]}")
        except Exception as e:
            print(f"  FEHLER: {e}")
    else:
        print("\n[2/3] workflows_get — SKIP (kein Workflow gefunden)")

    # Test 3: executions_list
    print("\n[3/3] executions_list...")
    try:
        result = executions_list(limit=5)
        data = json.loads(result)
        executions = data["executions"]
        print(f"  OK — {data['total']} Executions")
        for ex in executions[:3]:
            print(f"  - [{ex['id']}] Workflow {ex['workflow_id']} → {ex['status']}")
    except Exception as e:
        print(f"  FEHLER: {e}")

    print("\n" + "=" * 60)
    print("Test abgeschlossen!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
