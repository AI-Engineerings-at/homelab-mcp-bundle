#!/usr/bin/env python3
"""
Quick Test fuer Proxmox MCP Server.
Testet alle 6 Tools direkt gegen die echte PVE API.
"""

import os
import sys
import json

# Set PVE_PASSWORD before running: export PVE_PASSWORD=yourpassword
if not os.environ.get("PVE_PASSWORD"):
    print("ERROR: Set PVE_PASSWORD environment variable before running tests.")
    sys.exit(1)

from server import nodes_list, vms_list, vm_status, vm_resources

PASS = 0
FAIL = 0


def ok(msg):
    global PASS
    PASS += 1
    print(f"  OK — {msg}")


def fail(msg):
    global FAIL
    FAIL += 1
    print(f"  FAIL — {msg}")


def run_tests():
    print("=" * 60)
    print("Proxmox MCP Server — Test")
    print("=" * 60)

    first_vm = None

    # Test 1: nodes_list
    print("\n[1/4] nodes_list...")
    try:
        result = nodes_list()
        data = json.loads(result)
        assert isinstance(data, list), "Expected list"
        assert len(data) > 0, "No nodes returned"
        for n in data:
            status = "online" if n["status"] == "online" else n["status"]
            print(f"  Node: {n['node']} | {status} | CPU: {n['cpu_usage_pct']}% | "
                  f"RAM: {n['mem_used_gb']}/{n['mem_total_gb']} GB ({n['mem_pct']}%)")
        ok(f"{len(data)} Nodes gefunden")
    except Exception as e:
        fail(f"nodes_list: {e}")

    # Test 2: vms_list (alle Nodes)
    print("\n[2/4] vms_list (alle Nodes)...")
    try:
        result = vms_list()
        data = json.loads(result)
        assert isinstance(data, list), "Expected list"
        running = [v for v in data if v["status"] == "running"]
        print(f"  Gesamt: {len(data)} VMs/LXCs | Laufend: {len(running)}")
        for v in data[:5]:
            print(f"  [{v['vmid']}] {v['name']} ({v['type']}) @ {v['node']} — {v['status']}")
        ok(f"{len(data)} VMs/LXCs gefunden")
        if data:
            first_vm = data[0]
    except Exception as e:
        fail(f"vms_list: {e}")

    # Test 3: vm_status (erste laufende VM)
    if first_vm:
        print(f"\n[3/4] vm_status (vmid={first_vm['vmid']}, node={first_vm['node']})...")
        try:
            result = vm_status(
                node=first_vm["node"],
                vmid=first_vm["vmid"],
                vm_type=first_vm["type"]
            )
            data = json.loads(result)
            assert "status" in data, "Missing 'status' field"
            print(f"  Name: {data.get('name')} | Status: {data['status']}")
            print(f"  CPU: {data.get('cpu_usage_pct')}% | "
                  f"RAM: {data.get('mem_used_mb')}/{data.get('mem_max_mb')} MB")
            ok(f"vm_status OK fuer vmid {first_vm['vmid']}")
        except Exception as e:
            fail(f"vm_status: {e}")
    else:
        print("\n[3/4] vm_status — SKIP (keine VM gefunden)")

    # Test 4: vm_resources
    print("\n[4/4] vm_resources...")
    try:
        result = vm_resources()
        data = json.loads(result)
        assert "cluster_summary" in data, "Missing 'cluster_summary'"
        assert "top_cpu" in data, "Missing 'top_cpu'"
        assert "top_mem" in data, "Missing 'top_mem'"
        s = data["cluster_summary"]
        print(f"  Laufende VMs: {s['running_vms']}/{s['total_vms']}")
        print(f"  Cluster CPU: {s['total_cpu_pct']}% | "
              f"RAM: {s['total_mem_used_gb']}/{s['total_mem_max_gb']} GB ({s['mem_pct']}%)")
        if data["top_cpu"]:
            top = data["top_cpu"][0]
            print(f"  Top CPU: [{top['vmid']}] {top['name']} @ {top['cpu_pct']}%")
        if data["top_mem"]:
            top = data["top_mem"][0]
            print(f"  Top RAM: [{top['vmid']}] {top['name']} @ {top['mem_used_mb']} MB")
        ok("vm_resources OK")
    except Exception as e:
        fail(f"vm_resources: {e}")

    # Summary
    print("\n" + "=" * 60)
    total = PASS + FAIL
    print(f"Ergebnis: {PASS}/{total} Tests bestanden")
    if FAIL == 0:
        print("Alle Tests GRUEN!")
    else:
        print(f"{FAIL} Test(s) FEHLGESCHLAGEN!")
    print("=" * 60)

    return FAIL == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
