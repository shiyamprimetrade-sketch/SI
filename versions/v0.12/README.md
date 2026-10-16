# SI v0.12 — Independent cross-runtime virtual machine

Experimental SI research module. Adds `js/vm.js`, a Node.js/BigInt/binary64 VM independent of SI's three Python engines, together with `tests/test_cross_runtime_vm.py` differential tests of outputs, stack, step counts and error categories.

Includes `docs/runtime_semantics.md`, `docs/research_v012.md`, `courses/lesson08_cross_runtime_vm.md`, and verified CI evidence once published. Earlier SI versions and the Python `shlex` legacy interpreter are preserved. The new JavaScript VM implements only the optional SI-Portable-1 source profile, not arbitrary Python values or untrusted bytecode deserialization.

## Test
From `versions/v0.12`:
```sh
node --version
python -W error -m unittest discover -s tests -v
python -W error -m si.obligations
python -m si examples.si
```
Workflow `.github/workflows/ci-v012.yml` runs Node 22 and Python 3.11, 3.12 and 3.13. The cross-runtime VM tests require Node.

**Limitations:** finite conformance does not prove full semantic equivalence or global language superiority, security isolation, completed doctoral research, new original language or new terminal.

**Training:** new SI score 0/1000000; points awarded 0; historical score 996667/1000000 retained separately.
