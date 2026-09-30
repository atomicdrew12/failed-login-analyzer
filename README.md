# Failed Login Analyzer

A beginner-friendly Python command-line tool that reads Linux `auth.log` files and flags suspicious login activity: brute-force attempts, username spraying, and the dangerous "many failures, then a success" pattern.

## What & Why

Every internet-facing Linux server gets hammered by automated SSH login attempts. The evidence sits in `/var/log/auth.log`, but reading thousands of lines by hand is slow and error-prone. **Failed Login Analyzer** parses those logs, tallies failed logins by IP address and username, and highlights the sources that look like attacks, so a defender can quickly decide what to block or investigate. I'm building it as a hands-on defensive security project to practice Python (file I/O, regular expressions, data structures, CLI design, testing) while learning how real-world authentication attacks show up in logs.

> 🚧 **Status: in development.** The features below are planned and tracked as milestones in [Issues](../../issues). Boxes get checked as each milestone is completed.

## Features (planned)

- [ ] **Parse auth.log entries.** Extract timestamp, username, source IP, and success/failure from sshd lines, including `Invalid user` attempts *(Milestone 1)*
- [ ] **Count and flag brute force.** Tally failures per IP and per username; flag IPs that exceed a threshold within a sliding time window, e.g. 5 failures in 10 minutes *(Milestone 2)*
- [ ] **Spot fail-then-succeed.** Flag IPs with repeated failures followed by a successful login, a possible compromised password *(Milestone 3)*
- [ ] **Reports.** Clean terminal summary plus CSV and JSON export *(Milestone 4)*
- [ ] **A real CLI tool.** `argparse` options, `pytest` test suite, GitHub Actions CI *(Milestone 5)*
- [ ] **Stretch goals.** Windows event log export support, IP geolocation lookup, live tail mode *(Milestone 6)*

## How It Works

1. **Read** the log file line by line (memory-friendly, even for large files).
2. **Parse** each line with regular expressions to pull out the timestamp, username, source IP, and result (`Accepted`, `Failed password`, `Invalid user`). Lines that aren't login events are skipped.
3. **Aggregate** events per source IP and per username using dictionaries / `collections.Counter`.
4. **Detect** patterns:
   - *Brute force:* an IP with at least `--threshold` failures inside any `--window`-minute sliding window.
   - *Username spray:* one IP trying many different (often nonexistent) usernames.
   - *Fail-then-succeed:* an IP with several failures followed by an `Accepted` login.
5. **Report** the findings to the terminal, and optionally export them to CSV or JSON.

## Usage (planned)

```bash
python analyzer.py samples/auth.log --threshold 5 --window 10
```

Planned options:

| Option | Description | Default (planned) |
|---|---|---|
| `logfile` | Path to the auth log to analyze | *(required)* |
| `--threshold` | Failed attempts that trigger a brute-force flag | `5` |
| `--window` | Sliding window size in minutes | `10` |
| `--format` | Output format: `text`, `csv`, or `json` | `text` |

**Example output (illustrative mock-up only, not real results):**

```text
=== Failed Login Analyzer: EXAMPLE OUTPUT ===
[!] BRUTE FORCE      <ip-address>   <N> failures in <M> min   users: root, admin
[!] USERNAME SPRAY   <ip-address>   <N> invalid usernames tried
[!] FAIL→SUCCESS     <ip-address>   <N> failures, then accepted login for <user>
```

## Project Structure (planned)

```text
failed-login-analyzer/
├── analyzer.py              # Main CLI script
├── samples/
│   └── auth.log             # Synthetic sample log for testing/demo
├── tests/                   # pytest tests using the sample log
├── .github/
│   └── workflows/           # GitHub Actions CI (runs pytest on push/PR)
├── README.md
└── LICENSE
```

## Roadmap

1. **Milestone 1: Parse auth.log entries.** Read the log line by line; regex out timestamp, username, source IP, success/failure; handle `Invalid user` lines.
2. **Milestone 2: Count failures and flag brute-force IPs.** Tally failures per IP and per username; flag IPs over a threshold within a sliding window.
3. **Milestone 3: Detect fail-then-succeed logins.** Flag IPs with many failures followed by a success (possible compromised password).
4. **Milestone 4: Terminal report with CSV and JSON export.**
5. **Milestone 5: Make it a real tool.** `argparse` options, `pytest` tests, GitHub Actions CI.
6. **Milestone 6: Stretch goals.** Windows event log export support, IP geolocation lookup, live tail mode.

Progress is tracked in the repo's [Issues](../../issues).

## Sample Data & Responsible Use

- The file `samples/auth.log` is **entirely synthetic**. It was written by hand for testing. All IP addresses come from the reserved documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, per RFC 5737) and do not belong to real hosts.
- This is a **defensive** tool. Only analyze logs from systems you own or are authorized to administer.

## License

Released under the [MIT License](LICENSE).
