# Presets

Self-contained governance modules extracted from `constitution.md` for selective loading.

## Convention

- Each preset is a standalone `.md` file with its own header
- Commands load only the presets they need (see mapping below)
- If a preset file is missing, the command SHOULD warn and continue

## Available Presets

| Preset | File | Commands |
|---|---|---|
| Архитектурный комитет | `archkom.md` | consilium, architecture, graduate (Standard+) |
| GSD-интеграция | `gsd.md` | gsd-bridge, gsd-verify, gsd-map, implement (GSD mode) |

## References

- MADR: https://adr.github.io/madr/
- arc42: https://arc42.org/documentation/
- OpenAPI 3.1.1: https://spec.openapis.org/oas/v3.1.1
- AsyncAPI 3.0: https://www.asyncapi.com/docs/reference/specification/v3.0.0
- OpenSLO v1: https://github.com/OpenSLO/OpenSLO
- Keep a Changelog: https://keepachangelog.com/
- SemVer: https://semver.org/
- Redocly CLI: https://redocly.com/docs/cli/
- Spectral: https://stoplight.io/open-source/spectral
- oasdiff: https://github.com/oasdiff/oasdiff
- check-jsonschema: https://github.com/python-jsonschema/check-jsonschema
