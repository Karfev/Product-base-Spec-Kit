# Tests — Reference Stubs

> These test files are **stubs** that demonstrate the SpecKit traceability pattern.
> They exist so that `trace.md` and `requirements.yml` references resolve to real files.

## Traceability Convention

Each test file/case references a `REQ-ID` from `requirements.yml`:

```
tests/api/api-keys.spec.ts::REQ-AUTH-001   ← links test to requirement
tests/perf/auth-latency.jmx::REQ-AUTH-004  ← links perf test to NFR
```

`check-trace.py` verifies that the file exists, the `REQ-ID` matches the requirement
and appears in the file. Broken links are errors once a requirement is `implemented`
or `verified`, and warnings before that.

A test that lives in another repository is written as
`ext:<repo>/<path>::REQ-AUTH-001`. Only its format and `REQ-ID` are checked.

`check-trace.py` checks links only: it does not prove that a test passes.

## In Your Project

Replace these stubs with real tests. Keep the `REQ-ID` references in test names
or tags so the traceability chain remains intact.
