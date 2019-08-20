# ROTTN

Indie game with only procedurally generated boss levels. Online/LAN-Coop. Boss-AI uses Deep Q Neural Nets in order to adapt to and learn from the player during a fight.

## Development Environment 

This project is using Python 3.6.5 (https://www.python.org/downloads/release/python-365/)

Recommended IDE: VSCode + "official" Python Extension (https://code.visualstudio.com/download)

### Windows

1. Clone Repository (https://git-scm.com/download/win)
1. Run `.\dev_setup.bat` as Administrator
1. IDE-specific setup (VSCode: enable pytest for unit tests in `.\tests\`)

If you're missing dependencies run `.\dev_update.bat` to install them in your venv.

### \*nix/MacOS

No setup scripts yet.

## Documentation

Documentation stuff goes to `.\docs\`.

**Navigation:**
- [ROTTN Game Design Document](./designdocument.md)
- [Player Story Map](https://app.wisemapping.com/c/maps/747726/public)

### Diagrams

Recommended modelling tool: https://www.draw.io/

Save diagrams (.xml and exported .pdf with same name) to `.\docs\diagrams\`.

### API Documentation

We generate markdown files from docstrings using *pydocmd* (https://github.com/NiklasRosenstein/pydoc-markdown).

### Game Design Documentation

`.\docs\gamedesign\` contains a [short design document](./docs/gamedesign/designdocument.md) that illustrates the overall vision and any documents we might come up with to describe game design aspects in the future. A [*Player Story Map*](https://app.wisemapping.com/c/maps/747726/edit) is maintained in [WiseMapping](https://app.wisemapping.com), an open source mind mapping tool, and contains a more detailed view on the features of the game.

## Testing

Start the client with `python -m rottn.client`.
You can run the server seperately with `python -m rottn.server`, but currently it is expected that the client starts the server as a subprocess.

### Unit Tests

py.test (https://docs.pytest.org) unit tests in `.\tests\` folder.

![Screenshot](/screenshot.png)

