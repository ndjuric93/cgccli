# Set CGC CLI on PATH
export CGCCLI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd )"/cgc-cli
export PATH=${CGCCLI_ROOT}:${PATH}
