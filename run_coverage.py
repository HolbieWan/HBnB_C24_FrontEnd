import os
import subprocess

# Define paths
COVERAGE_RC = "coverage/.coveragerc"
HTMLCOV_DIR = "coverage/htmlcov"
TEST_SCRIPT = "app/tests/run_all_tests.py"

# Ensure the coverage directory and required files exist
if not os.path.exists("coverage"):
    print("Error: 'coverage' directory does not exist.")
    exit(1)

if not os.path.exists(COVERAGE_RC):
    print(f"Error: Coverage configuration file '{COVERAGE_RC}' not found.")
    exit(1)

if not os.path.exists(TEST_SCRIPT):
    print(f"Error: Test script '{TEST_SCRIPT}' not found.")
    exit(1)

def run_coverage():
    """Run coverage on the specified test script and generate reports."""
    try:
        # Run the test script with coverage
        print(f"Running '{TEST_SCRIPT}' with coverage...")
        subprocess.run(
            ["coverage", "run", "--rcfile", COVERAGE_RC, TEST_SCRIPT],
            check=True,
        )

        # Generate text report
        print("Generating coverage report...")
        subprocess.run(
            ["coverage", "report", "-m", "--rcfile", COVERAGE_RC],
            check=True,
        )

        # Generate HTML report
        print("Generating HTML coverage report...")
        subprocess.run(
            ["coverage", "html", "--rcfile", COVERAGE_RC, "--directory", HTMLCOV_DIR],
            check=True,
        )

        print(f"HTML report generated in '{HTMLCOV_DIR}/index.html'")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    run_coverage()