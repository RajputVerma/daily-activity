name: Daily Commit (Human Style)

on:
  schedule:
    - cron: "15 5 * * *"
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - name: Random delay to look human
        run: |
          delay=$(( RANDOM % 2400 ))
          echo "Waiting for $delay seconds before acting..."
          sleep $delay

      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Maybe skip today
        id: skipcheck
        run: |
          SKIP_CHANCE=$(( RANDOM % 10 ))
          if [ $SKIP_CHANCE -eq 0 ]; then
            echo "skip=yes" >> $GITHUB_OUTPUT
          else
            echo "skip=no" >> $GITHUB_OUTPUT
          fi

      - name: Stop workflow if skipping today
        if: steps.skipcheck.outputs.skip == 'yes'
        run: echo "Skipping today's commit to look natural."

      - name: Make update
        if: steps.skipcheck.outputs.skip == 'no'
        run: |
          messages=("Updated notes" "Minor tweak" "Small improvement" "Daily log update" "Tiny cleanup" "Progress recorded" "Keeping track" "Routine update" "Little adjustment")
          msg=${messages[$RANDOM % ${#messages[@]}]}

          echo "$msg on $(date '+%Y-%m-%d %H:%M:%S')" >> daily_update.txt

      - name: Commit changes
        if: steps.skipcheck.outputs.skip == 'no'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "Update: $(date '+%Y-%m-%d')" || echo "Nothing to commit"

      - name: Push changes
        if: steps.skipcheck.outputs.skip == 'no'
        run: git push
