from workflow.pentest_workflow import start_scan


def main():

    print("=" * 60)
    print("                 FLOW")
    print("        A PentestAI Framework")
    print("=" * 60)

    target = input("\nEnter Target: ")

    start_scan(target)


if __name__ == "__main__":
    main()