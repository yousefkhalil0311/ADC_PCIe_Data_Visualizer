#!/bin/bash
# Make executable: chmod +x captureDataTool.sh
# compile c++ file: g++ -O3 -march=native -std=c++17 pcie_read.cpp -o pcie_read
# Sequential execution: Python first, then C++ shim

# Initialize argument variables
PY_CONFIG=""
CPP_OUTPUT=""
CPP_TIME=""
CPP_NUMBYTES=""

# --- Help message function ---
function usage() {
    echo "Usage: $0 -c configFile -o outputFile [-t time_ms | -n numBytes]"
    echo ""
    echo "Arguments:"
    echo "  -c  configFile      Path to Python config file (required for Python script)"
    echo "  -o  outputFile      Path to shared memory output file (required for C++ shim)"
    echo "  -t  time_ms         Number of milliseconds to capture (mutually exclusive with -n)"
    echo "  -n  numBytes        Number of bytes to capture (mutually exclusive with -t)"
    echo "  -h, --help          Show this help message and exit"
    echo ""
    echo "Example:"
    echo "  $0 -c config.json -o output.bin -t 100"
    echo "  $0 -c config.json -o output.bin -n 1048576"
    exit 0
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -c)
            PY_CONFIG="$2"
            shift 2
            ;;
        -o)
            CPP_OUTPUT="$2"
            shift 2
            ;;
        -t)
            if [[ -n "$CPP_NUMBYTES" ]]; then
                echo "Error: -t and -n are mutually exclusive"
                exit 1
            fi
            CPP_TIME="$2"
            shift 2
            ;;
        -n)
            if [[ -n "$CPP_TIME" ]]; then
                echo "Error: -t and -n are mutually exclusive"
                exit 1
            fi
            CPP_NUMBYTES="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# --- Run Python script first ---
echo "Running Python script with config: $PY_CONFIG"
python3 qc_cli_tool.py -c "$PY_CONFIG"
PY_STATUS=$?
if [ $PY_STATUS -ne 0 ]; then
    echo "Python script failed with exit code $PY_STATUS. Aborting."
    exit $PY_STATUS
fi

# --- Run C++ shim next ---
echo "Running C++ shim with output: $CPP_OUTPUT, time: $CPP_TIME, numBytes: $CPP_NUMBYTES"
./pcie_read -o "$CPP_OUTPUT" -t "$CPP_TIME" -n "$CPP_NUMBYTES"
CPP_STATUS=$?
if [ $CPP_STATUS -ne 0 ]; then
    echo "C++ shim failed with exit code $CPP_STATUS."
    exit $CPP_STATUS
fi

echo "Capture complete."
