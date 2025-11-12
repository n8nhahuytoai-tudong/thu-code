#!/usr/bin/env python3
"""
Batch Process Multiple ComfyUI Workflows
Tận dụng CPU và GPU để chạy nhiều workflows song song
"""

import json
import os
import time
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
COMFYUI_URL = "http://127.0.0.1:8188"
MAX_CONCURRENT_JOBS = 3  # Số workflows chạy đồng thời
POLL_INTERVAL = 2  # Giây giữa các lần check status

def load_workflow(workflow_path):
    """Load workflow JSON file"""
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Cannot load workflow {workflow_path}: {e}")
        return None

def submit_workflow(workflow_data, workflow_name="workflow"):
    """Submit workflow to ComfyUI API"""
    try:
        # Prepare prompt
        prompt_data = {
            "prompt": workflow_data,
            "client_id": f"batch_processor_{int(time.time())}"
        }

        # Send request
        data = json.dumps(prompt_data).encode('utf-8')
        req = urllib.request.Request(
            f"{COMFYUI_URL}/prompt",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            prompt_id = result.get('prompt_id')

            if prompt_id:
                print(f"[OK] Submitted {workflow_name}: {prompt_id}")
                return prompt_id
            else:
                print(f"[ERROR] Failed to submit {workflow_name}: No prompt_id")
                return None

    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP Error for {workflow_name}: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"[ERROR] Response: {error_body}")
        except:
            pass
        return None
    except Exception as e:
        print(f"[ERROR] Cannot submit {workflow_name}: {e}")
        return None

def check_queue_status():
    """Check ComfyUI queue status"""
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/queue")
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode('utf-8'))

            queue_running = len(result.get('queue_running', []))
            queue_pending = len(result.get('queue_pending', []))

            return queue_running, queue_pending
    except Exception as e:
        print(f"[WARNING] Cannot check queue: {e}")
        return 0, 0

def wait_for_completion(prompt_id, workflow_name="workflow", timeout=600):
    """Wait for workflow to complete"""
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            print(f"[TIMEOUT] {workflow_name} exceeded {timeout}s")
            return False

        try:
            # Check history
            req = urllib.request.Request(f"{COMFYUI_URL}/history/{prompt_id}")
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))

                if prompt_id in result:
                    history_entry = result[prompt_id]
                    status = history_entry.get('status', {})

                    if status.get('completed', False):
                        print(f"[DONE] {workflow_name} completed in {elapsed:.1f}s")
                        return True
                    elif status.get('status_str') == 'error':
                        print(f"[ERROR] {workflow_name} failed: {status}")
                        return False
        except:
            pass

        time.sleep(POLL_INTERVAL)

def process_workflow_batch(workflow_files, max_concurrent=MAX_CONCURRENT_JOBS):
    """Process multiple workflows with concurrency control"""
    print("="*60)
    print(f"  Batch Processing {len(workflow_files)} workflows")
    print(f"  Max concurrent: {max_concurrent}")
    print("="*60)
    print()

    results = {}

    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        futures = {}

        for workflow_file in workflow_files:
            workflow_name = Path(workflow_file).stem
            workflow_data = load_workflow(workflow_file)

            if not workflow_data:
                results[workflow_name] = "LOAD_FAILED"
                continue

            # Submit workflow
            prompt_id = submit_workflow(workflow_data, workflow_name)

            if prompt_id:
                # Submit wait task
                future = executor.submit(wait_for_completion, prompt_id, workflow_name)
                futures[future] = workflow_name
            else:
                results[workflow_name] = "SUBMIT_FAILED"

            # Small delay to avoid overwhelming server
            time.sleep(0.5)

        # Wait for all to complete
        for future in as_completed(futures):
            workflow_name = futures[future]
            try:
                success = future.result()
                results[workflow_name] = "SUCCESS" if success else "FAILED"
            except Exception as e:
                print(f"[ERROR] Exception for {workflow_name}: {e}")
                results[workflow_name] = "EXCEPTION"

    return results

def print_summary(results):
    """Print batch processing summary"""
    print()
    print("="*60)
    print("  BATCH PROCESSING SUMMARY")
    print("="*60)
    print()

    success_count = sum(1 for v in results.values() if v == "SUCCESS")
    failed_count = len(results) - success_count

    print(f"Total: {len(results)}")
    print(f"Success: {success_count}")
    print(f"Failed: {failed_count}")
    print()

    if failed_count > 0:
        print("Failed workflows:")
        for name, status in results.items():
            if status != "SUCCESS":
                print(f"  - {name}: {status}")
        print()

def main():
    """Main function"""
    import sys

    print("="*60)
    print("  ComfyUI Batch Workflow Processor")
    print("  Tan dung CPU/GPU de chay nhieu workflows")
    print("="*60)
    print()

    # Check if ComfyUI is running
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
        urllib.request.urlopen(req, timeout=5)
        print("[OK] ComfyUI is running")
    except:
        print(f"[ERROR] ComfyUI is not running at {COMFYUI_URL}")
        print("Please start ComfyUI first!")
        return 1

    # Get workflow files from command line or default folder
    if len(sys.argv) > 1:
        workflow_files = sys.argv[1:]
    else:
        # Default: look for workflows in current directory
        workflow_dir = Path(".")
        workflow_files = list(workflow_dir.glob("workflow*.json"))

        if not workflow_files:
            print("[ERROR] No workflow files found!")
            print()
            print("Usage:")
            print("  python batch_process_workflows.py workflow1.json workflow2.json ...")
            print("  or put workflow*.json files in current directory")
            return 1

    print(f"[INFO] Found {len(workflow_files)} workflow(s)")
    for wf in workflow_files:
        print(f"  - {wf}")
    print()

    # Check queue status before starting
    running, pending = check_queue_status()
    print(f"[INFO] Current queue: {running} running, {pending} pending")
    print()

    # Process workflows
    start_time = time.time()
    results = process_workflow_batch(workflow_files, MAX_CONCURRENT_JOBS)
    elapsed = time.time() - start_time

    # Print summary
    print_summary(results)
    print(f"Total time: {elapsed:.1f}s")
    print()

    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
        exit(1)
