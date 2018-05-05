# bossfight

Indie game with only procedurally generated boss levels. Online/LAN-Coop. Aim: Boss-AI uses procedurally generated Neural Nets with Reinforcement Learning capacity.

## Development Environment Setup

Recommended IDE: VSCode + Python Extension (by MS)

### Windows

1. Clone Repository
1. Run `.\dev_setup.bat` as Administrator
1. Open project folder in preferred IDE, maybe install pylint, enable pytest (unit tests are in the `.\tests\` subfolder).
1. To start the server run `python -m bossfight.server`, the start a client in a new terminal with `python -m bossfight.client`.

### \*nix/MacOS

No setup scripts yet.
