#!/bin/bash
# File: run_all_trainings.sh

BASE_DIR="/nfs4/jjlee/datasets/immertix/images_relative_lit"
RESULTS_DIR="results"
CSV_FILE="no_tactile_training_metrics_all.csv"


echo "Starting all trainings in $BASE_DIR..."
# Optional: create results directory if not exists
mkdir -p "$RESULTS_DIR"

# Remove old CSV if exists (start fresh)
if [ -f "$CSV_FILE" ]; then
    echo "Removing old $CSV_FILE..."
    rm "$CSV_FILE"
fi

# Iterate through subdirectories
for subdir in "$BASE_DIR"/*; do
    if [ ! -d "$subdir" ]; then
        continue
    fi

    name=$(basename "$subdir")
    model_path="${RESULTS_DIR}/${name}"

    echo "========================================================"
    echo "Starting training for dataset: $name"
    echo "========================================================"

    python train.py -s "$subdir" -m "$model_path" --eval

    echo "Training for $name completed."
    echo
done

echo "========================================================"
echo "All trainings completed. Results saved to $CSV_FILE"
echo "========================================================"