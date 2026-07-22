# Release Checklist

Use this checklist before tagging a new release.

## Scientific Integrity

- [ ] New or updated claims are recorded in EVIDENCE_TABLE.md.
- [ ] Every external claim cites a DOI or peer-reviewed source.
- [ ] Claims are labeled as proven-theorem, computational-evidence,
      toy-model-observation, or open.
- [ ] README scope statement still clearly separates Collatz from toy maps.

## Reproducibility

- [ ] Environment and command log are updated in REPRODUCIBILITY.md.
- [ ] Key scripts have deterministic parameters documented.
- [ ] Core command outputs are copied into release notes or artifacts.

## Code Quality

- [ ] Run: python -m unittest discover -v .
- [ ] No test failures.
- [ ] CLI examples in README still execute.
- [ ] New scripts include docstrings and argument help.

## Governance and Metadata

- [ ] CITATION.cff version/date fields are updated.
- [ ] CHANGELOG or release notes summarize scientific changes.
- [ ] Tag name matches semantic versioning policy.

## Final Gate

- [ ] Re-run the full test suite on the release commit.
- [ ] Confirm CI workflow passes on the tagged commit.
