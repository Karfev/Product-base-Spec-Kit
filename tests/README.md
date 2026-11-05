# Tests — Reference Stubs

> These test files are **stubs** that demonstrate the SpecKit traceability pattern.
> They exist so that `trace.md` and `requirements.yml` references resolve to real files.

## Traceability Convention

Each test file/case references a `REQ-ID` from `requirements.yml`:

```
tests/api/api-keys.spec.ts::REQ-AUTH-001   ← links test to requirement
tests/perf/auth-latency.jmx::REQ-AUTH-004  ← links perf test to NFR
```

This convention enables `check-trace.py` to verify that every requirement
has at least one test reference, and every test reference points to a valid REQ-ID.

## In Your Project

Replace these stubs with real tests. Keep the `REQ-ID` references in test names
or tags so the traceability chain remains intact.
