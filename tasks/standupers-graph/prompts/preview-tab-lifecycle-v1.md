# Preview tab lifecycle v1

Apply to browser-backed research: server tab capacity is shared, while preview_status may list only caller-visible tabs. An absent tab does not prove browser unavailability; attempt preview_open.

Use one own tab per worker. Capture returned tabId, pass it on every call, and navigate that tab for subsequent URLs. Avoid opening a new tab per page. Log navigation separately from read-only snapshots/evaluation.

Close the worker’s own tab with t3_preview_close before returning, including zero-result/error outcomes. Never close human-controlled or another agent’s tabs. Parent may close its own obsolete tabs and smoke-test capacity, then close the test tab to leave a slot for the next worker.

A tab-limit/cache/access failure is a coverage blocker, not evidence absence. Preserve promising leads as quarantined until complete author text is retrieved. After actionable cleanup retry only within the original remaining research allowance. Record exact raw errors and cleanup result; no challenge bypass or repeated doomed opens.
