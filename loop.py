import subprocess
import sys

def main():
    try:
        user_input = input("Enter the number of loops to run: ").strip()
        total_runs = int(user_input)
        if total_runs <= 0:
            print("Error: Please enter a number greater than 0.")
            sys.exit(1)
    except ValueError:
        print("Error: Invalid input. Please enter a valid integer.")
        sys.exit(1)

    print(f"[*] Starting loop for {total_runs} run(s)...")

    for i in range(1, total_runs + 1):
        print(f"\n[+] Running iteration {i} of {total_runs}...")
        
        result = subprocess.run([sys.executable, "pandacut.py"])
        
        if result.returncode != 0:
            print(f"[!] Error detected in iteration {i}. Stopping the loop.")
            sys.exit(result.returncode)
            
        print(f"[ok] Iteration {i} finished successfully.")

    print("\n[ok] All loops completed successfully!")

if __name__ == "__main__":
    main()