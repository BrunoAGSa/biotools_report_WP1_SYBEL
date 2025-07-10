set -euo pipefail

TOPIC="${1:-Systems biology}"

MODE="${2:-extract_and_save}"

LOAD_PATH="${3:-}"

# handy for testing
MAX_PAGES="${4:-}"

export TOPIC MODE LOAD_PATH MAX_PAGES

NOTEBOOK="report.ipynb"
DATE=$(date +'%B_%d_%Y')
FORMATTED_TOPIC="${TOPIC,,}"              
FORMATTED_TOPIC="${FORMATTED_TOPIC// /_}" 
OUTPUT="reports/report_${FORMATTED_TOPIC}_${DATE}"

echo "Executing & converting $NOTEBOOK (TOPIC=$TOPIC, MODE=$MODE) → $OUTPUT …"
jupyter nbconvert \
  --to webpdf \
  --no-input \
  --embed-images \
  --allow-chromium-download \
  --execute \
  --ExecutePreprocessor.timeout=600 \
  --output "$OUTPUT" \
  "$NOTEBOOK"

echo "Done! Generated $OUTPUT"