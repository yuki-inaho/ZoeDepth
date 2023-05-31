#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: batch_process.sh IMAGE_DIR OUTPUT_DIR"
    exit 1
fi

IMAGE_DIR="$1"
OUTPUT_DIR="$2"
OUTPUT_EXTENSION=".png"

for file in "${IMAGE_DIR}"/*; do
    if [[ -f "${file}" ]]; then
        extension="${file##*.}"
        if [[ "${extension,,}" != "png" && "${extension,,}" != "jpg" ]]; then
            echo "Skipping: ${file}"
            continue
        fi

        input="${file}"
        filename=$(basename "${file}")
        filename="${filename%.*}"
        output="${OUTPUT_DIR}/${filename}${OUTPUT_EXTENSION}"
        python estimate_depth.py -i "${input}" -o "${output}" -c
        echo "Processed: ${file}"
        if [[ ${WITH_COLORED_OUTPUT} -eq 1 ]]; then
            echo "Colorized output saved to: ${colored_output}"
        fi
        echo ""
    fi
done