from workflow.pentest_workflow import start_scan
from core.dependency_checker import run_dependency_check


def main():

    print("=" * 60)
    print("                 FLOW")
    print("        A PentestAI Framework")
    print("=" * 60)

    print("\n[FLOW] Checking system dependencies...\n")

    if not run_dependency_check():
        print("\n[FLOW] Dependency check failed.")
        print("[FLOW] Please install the missing dependencies and try again.")
        return

    print("\n[FLOW] Dependency check passed.")

    target = input("\nEnter Target: ")

    start_scan(target)


if __name__ == "__main__":
    main()
