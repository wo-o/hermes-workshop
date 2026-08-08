# FastCampus Hermes Extension Lab

A public, dependency-light training repository that demonstrates three different Hermes extension paths from one upstream Git repository:

1. `skills/lab-release-check` — an installable Hermes skill.
2. Repository root — a native Hermes plugin exposing `course_greeting`.
3. `fastcampus-hermes-lab-mcp` — a stdio MCP server exposing `lab_status`.

The components intentionally return a visible version and color marker so a class can prove that an upstream update reached each installation path.

## Requirements

- Hermes Agent v0.20.0 or later
- Git
- `uv` for the MCP launcher

## Skill

```bash
hermes skills inspect wo-o/fastcampus-hermes-extension-lab/skills/lab-release-check
hermes skills install wo-o/fastcampus-hermes-extension-lab/skills/lab-release-check --yes
hermes skills check lab-release-check
hermes skills update lab-release-check
```

Start a new session or run `/reload-skills`, then invoke `/lab-release-check Techwoo`.

## Native plugin

```bash
hermes plugins install wo-o/fastcampus-hermes-extension-lab --enable
hermes plugins list --user
hermes plugins update fastcampus-extension-lab
```

Restart the Hermes CLI or gateway after install/update. Ask Hermes to call `course_greeting` for `Techwoo`.

## MCP server

Register the public Git repository as a stdio launcher. `--refresh` makes `uvx` re-resolve the branch when the MCP process starts.

```bash
hermes mcp add fastcampus_lab --command uvx --connect-timeout 120 \
  --args --refresh --from git+https://github.com/wo-o/fastcampus-hermes-extension-lab.git \
  fastcampus-hermes-lab-mcp
hermes mcp test fastcampus_lab
```

After an upstream update, run `hermes mcp test fastcampus_lab` again and reload MCP tools in the active session with `/reload-mcp`.

## Local verification

```bash
uv run --with pytest pytest -q
uv build
```

## Cleanup

```bash
hermes skills uninstall lab-release-check
hermes plugins disable fastcampus-extension-lab
hermes plugins remove fastcampus-extension-lab
hermes mcp remove fastcampus_lab
```

## Security boundary

The three mechanisms have different trust models. A skill supplies instructions, a native plugin executes Python in the Hermes process, and an MCP server executes as a separate process connected over MCP. Review public source before enabling any of them.

License: MIT
