---
description: Fetch newest unworked leads from Close, brief each, output call order
---
1. Read close-map.md. In Close, find leads with status New Lead / New Webby Opt ins / New Webby Sign Ups that have no call activity yet (use `search`, e.g. "leads with status New Lead and no calls", newest first). Cap at 10 unless I say otherwise.
2. Skip DNC and obvious test leads (name contains "test"). List what you skipped.
3. Run the lead-researcher agent on each one.
4. Output a call order table: # · name · created · fit score · hook · phone. Newest inbound first (speed to lead), then by fit score.
