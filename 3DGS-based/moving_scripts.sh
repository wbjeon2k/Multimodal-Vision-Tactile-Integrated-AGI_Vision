#!/bin/bash

ROOT_DIR="./results"   # change if necessary
RESULTS_DIR="./ply_lists"

# mkdir -p "$RESULTS_DIR"

# for dir in "$ROOT_DIR"/*/; do
#     # if glob didn't match any directory, skip
#     [ -d "$dir" ] || continue

#     # remove trailing slash and get basename
#     dir=${dir%/}
#     name=$(basename "$dir")

#     # skip the Results folder itself
#     if [ "$name" = "Results" ]; then
#         continue
#     fi

#     SRC="$dir/point_cloud/iteration_4000/point_cloud.ply"

#     if [ -f "$SRC" ]; then
#         DEST="$RESULTS_DIR/${name}_point_cloud.ply"

#         # avoid overwriting: if DEST exists, append numeric suffix
#         if [ -e "$DEST" ]; then
#             i=1
#             while [ -e "${RESULTS_DIR}/${name}_point_cloud_$i.ply" ]; do
#                 i=$((i + 1))
#             done
#             DEST="${RESULTS_DIR}/${name}_point_cloud_$i.ply"
#         fi

#         # copy preserving metadata; change to 'mv' to move instead of copy
#         if cp -p "$SRC" "$DEST"; then
#             printf "Copied: %s -> %s\n" "$SRC" "$DEST"
#         else
#             printf "Failed to copy: %s\n" "$SRC" >&2
#         fi
#     else
#         printf "Warning: not found: %s\n" "$SRC"
#     fi
# done


# Step 2: Create split folders
WITH_TEX="$RESULTS_DIR/with_tex"
WITHOUT_TEX="$RESULTS_DIR/without_tex"
mkdir -p "$WITH_TEX" "$WITHOUT_TEX"

# Step 3: Split files based on name including 'tex'
for file in "$RESULTS_DIR"/*.ply; do
    [ -f "$file" ] || continue

    if [[ "$(basename "$file")" == *tex* ]]; then
        mv "$file" "$WITH_TEX/"
        printf "Grouped into with_tex: %s\n" "$(basename "$file")"
    else
        mv "$file" "$WITHOUT_TEX/"
        printf "Grouped into without_tex: %s\n" "$(basename "$file")"
    fi
done

printf "\nCompleted.\n"
printf "With 'tex': %s\n" "$WITH_TEX"
printf "Without 'tex': %s\n" "$WITHOUT_TEX"