#!/bin/bash
# Verification script for evening-44-architect-breath audio delivery
# Run this after 6:00 PM to verify the implementation

set -e

JOB_ID="98022cf8-ff83-4c7d-aa86-ca3a455ca40d"
JOB_NAME="evening-44-architect-breath"
RUNS_FILE="$HOME/.openclaw/cron/runs/${JOB_ID}.jsonl"
ARCHIVE_DIR="/Volumes/madara/2026/twc-vault/01-Projects/Products/Churned-Content/Audio"
TODAY=$(date +%Y-%m-%d)

echo "🔍 Verifying evening-44-architect-breath execution..."
echo ""

# Check if job ran today
if [ -f "$RUNS_FILE" ]; then
    echo "✅ Run log file exists: $RUNS_FILE"
    
    # Get last run info
    LAST_RUN=$(tail -1 "$RUNS_FILE")
    echo ""
    echo "📋 Last run details:"
    echo "$LAST_RUN" | jq -r '
        "   Time: " + (.startedAtMs / 1000 | strftime("%Y-%m-%d %H:%M:%S")) +
        "\n   Status: " + .status +
        "\n   Duration: " + ((.endedAtMs - .startedAtMs) / 1000 | tostring) + "s"
    ' 2>/dev/null || echo "$LAST_RUN"
    
    echo ""
    echo "📝 Checking for errors in last run:"
    if echo "$LAST_RUN" | grep -qi "error\|fail\|missing"; then
        echo "⚠️  Potential issues found in log"
        echo "$LAST_RUN" | jq '.error // .message' 2>/dev/null || echo "$LAST_RUN"
    else
        echo "✅ No obvious errors detected"
    fi
else
    echo "❌ Run log file not found: $RUNS_FILE"
    echo "   Job may not have executed yet"
fi

echo ""
echo "📁 Checking audio archive..."

# Check for today's archive file
ARCHIVE_PATTERN="evening-44-architect-${TODAY}.m4a"
if ls "$ARCHIVE_DIR"/$ARCHIVE_PATTERN 2>/dev/null; then
    echo "✅ Archive file found:"
    ls -lh "$ARCHIVE_DIR"/$ARCHIVE_PATTERN
else
    echo "⚠️  Archive file not found: $ARCHIVE_DIR/$ARCHIVE_PATTERN"
    echo "   Listing recent files in archive directory:"
    ls -lht "$ARCHIVE_DIR" | head -10
fi

echo ""
echo "📊 Job configuration check:"
jq -r --arg job_id "$JOB_ID" '
    .jobs[] | select(.id == $job_id) | 
    "   Name: " + .name + 
    "\n   Enabled: " + (.enabled | tostring) +
    "\n   Schedule: " + .schedule.expr +
    "\n   Next run: " + ((.state.nextRunAtMs / 1000) | strftime("%Y-%m-%d %H:%M:%S")) +
    "\n   Last run: " + ((.state.lastRunAtMs / 1000) | strftime("%Y-%m-%d %H:%M:%S")) +
    "\n   Last status: " + .state.lastStatus
' "$HOME/.openclaw/cron/jobs.json"

echo ""
echo "🎯 Verification complete!"
echo ""
echo "To verify Telegram delivery:"
echo "   1. Check Telegram chat 1371522080"
echo "   2. Look for message around 6:00 PM"
echo "   3. Verify TWO attachments: voice note + octave-8.opus"
echo ""
echo "To view full run log:"
echo "   cat $RUNS_FILE | jq '.'"
