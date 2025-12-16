#!/usr/bin/env bash
set -euo pipefail

[[ $# -ge 2 ]] || {
  echo "Usage: $0 <data_structures|algorithms|leetcode> <file_name_without_ext> [program args...]" >&2
  exit 1
}

project="$1"; name="$2"; shift 2
case "$project" in data_structures|algorithms|leetcode) ;; *) echo "Unknown project: $project" >&2; exit 1 ;; esac

if [[ -x "/opt/homebrew/opt/llvm/bin/clang++" ]]; then
    export CC="/opt/homebrew/opt/llvm/bin/clang"
    export CXX="/opt/homebrew/opt/llvm/bin/clang++"
    export LDFLAGS="-L/opt/homebrew/opt/llvm/lib/c++ -Wl,-rpath,/opt/homebrew/opt/llvm/lib/c++"
    export CXXFLAGS="-stdlib=libc++ -I/opt/homebrew/opt/llvm/include/c++/v1"
else
    echo "Warning: Homebrew LLVM not found. Falling back to system compiler (C++23 features may fail)." >&2
fi

root_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
build_dir="$root_dir/build"

if [[ -f "$build_dir/CMakeCache.txt" && -n "${CXX:-}" ]]; then
    if ! grep -q "CMAKE_CXX_COMPILER:FILEPATH=$CXX" "$build_dir/CMakeCache.txt"; then
        echo "Compiler changed to $CXX. Cleaning build directory..."
        rm -rf "$build_dir"
    fi
fi

cmake -S "$root_dir" -B "$build_dir"

target_name="${project}__${name//\//__}"
cmake --build "$build_dir" --target "$target_name" --parallel || cmake --build "$build_dir" --parallel

exe_path="$root_dir/$project/outputs/$(basename -- "$name")"
[[ -x "$exe_path" ]] || { echo "Executable not found: $exe_path" >&2; exit 1; }
exec "$exe_path" "$@"
