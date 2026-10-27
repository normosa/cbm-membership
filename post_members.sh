#!/usr/bin/env bash

set -u

API_URL="https://cbmnigeria.org/api/auth/register"
DATA_FILE="patani.json"

USER_AGENTS=(
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15"
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
)

usage() {
  echo "Usage: $0 <start-index> <max-records>" >&2
  echo "Example: $0 100 10" >&2
}

if [[ $# -ne 2 || ! $1 =~ ^[0-9]+$ || ! $2 =~ ^[1-9][0-9]*$ ]]; then
  usage
  exit 1
fi

for command in jq curl; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Error: required command '$command' is not installed." >&2
    exit 1
  fi
done

if [[ ! -f "$DATA_FILE" ]]; then
  echo "Error: '$DATA_FILE' was not found in the current directory." >&2
  exit 1
fi

if ! total_records=$(jq -e 'if type == "array" then length else error("expected a JSON array") end' "$DATA_FILE"); then
  echo "Error: '$DATA_FILE' must contain a valid JSON array." >&2
  exit 1
fi

start_index=$1
max_records=$2

if (( start_index >= total_records )); then
  echo "Error: start index $start_index is outside '$DATA_FILE', which contains $total_records records." >&2
  exit 1
fi

end_index=$((start_index + max_records))
if (( end_index > total_records )); then
  end_index=$total_records
fi

records_to_post=$((end_index - start_index))

response_file=$(mktemp)
trap 'rm -f "$response_file"' EXIT

successful=0
failed=0

for ((index = start_index; index < end_index; index++)); do
  record=$(jq -c --argjson index "$index" '.[$index]' "$DATA_FILE")
  user_agent=${USER_AGENTS[RANDOM % ${#USER_AGENTS[@]}]}

  if http_status=$(curl --silent --show-error \
    --output "$response_file" \
    --write-out '%{http_code}' \
    --request POST \
    --user-agent "$user_agent" \
    --header 'Content-Type: application/json' \
    --header 'Accept: application/json' \
    --data-binary "$record" \
    "$API_URL"); then
    if [[ $http_status =~ ^2[0-9][0-9]$ ]]; then
      echo "Record index $index posted successfully."
      ((successful += 1))
    else
      echo "Record index $index failed with HTTP status $http_status." >&2
      jq -c . "$response_file" 2>/dev/null || sed -n '1p' "$response_file" >&2
      ((failed += 1))
    fi
  else
    echo "Record index $index failed: curl could not complete the request." >&2
    ((failed += 1))
  fi

  if (( index + 1 < end_index )); then
    delay=$((RANDOM % 3 + 1))
    #sleep "$delay"
  fi
done

echo "Finished: processed $records_to_post records from index $start_index; $successful successful, $failed failed."

if (( failed > 0 )); then
  exit 1
fi
