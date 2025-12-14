#!/usr/bin/env bash
set -euo pipefail

[[ $# -ge 2 ]] || {
  echo "Usage: $0 <data_structures|algorithms> <file_name_without_ext> [program args...]" >&2
  exit 1
}

project="$1"; name="$2"; shift 2
case "$project" in data_structures|algorithms) ;; *) echo "Unknown project: $project" >&2; exit 1 ;; esac

root_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
build_dir="$root_dir/build"

cmake -S "$root_dir" -B "$build_dir"

target_name="${project}__${name//\//__}"
cmake --build "$build_dir" --target "$target_name" --parallel || cmake --build "$build_dir" --parallel

exe_path="$root_dir/$project/outputs/$(basename -- "$name")"
[[ -x "$exe_path" ]] || { echo "Executable not found: $exe_path" >&2; exit 1; }
exec "$exe_path" "$@"
