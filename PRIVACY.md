# Proposed data handling policy

- Obtain explicit permission before accessing Reddit data and follow all approval conditions and applicable terms.
- Collect only necessary public gaming discussion data; do not collect usernames or profile histories, infer sensitive traits, or identify individual users.
- Use data only for approved personal, non-commercial analysis. No model training or fine-tuning, resale, or public redistribution.
- Current prototype processes data in memory and prints a review draft. Do not retain raw output by default. No external AI or email transfer is implemented.
- Before implementing persistent storage or email, confirm permission, define retention limits, and implement deletion and removal synchronization for stored content and derived records as required. Avoid sending raw user content in email; honor deletion obligations. Do not enable storage or delivery if these obligations cannot be met.
- Respect rate limits and access restrictions; stop or reduce requests when limited. Do not bypass access controls.
- Store credentials in local environment variables, never in source control. Restrict access to any approved stored data.
- Clearly label partial coverage, uncertainty, and analysis hypotheses. Do not treat Reddit discussions as representative of the whole market.
