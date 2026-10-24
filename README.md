# safe-bit

[![Tests](https://github.com/first-uninteresting-username/safe-bit/actions/workflows/run-test.yaml/badge.svg?branch=main)](https://github.com/first-uninteresting-username/safe-bit/actions/workflows/run-test.yaml)
[![Build OCI image](https://github.com/first-uninteresting-username/safe-bit/actions/workflows/build-image.yaml/badge.svg)](https://github.com/first-uninteresting-username/safe-bit/actions/workflows/build-image.yaml)
[![License: AGPL-3.0-only](https://img.shields.io/badge/license-AGPL--3.0--only-blue)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Built with devenv](https://devenv.sh/assets/devenv-badge.svg)](https://devenv.sh)

A completely pointless project that solves [a problem nobody has ever had](/docs/motivation.md).
(TLDR: What if you needed to generate a bit in a way other person can trust you it isn't manipulated, without seeing the bit).

![Screenshot of the frontend](https://user-cdn.hackclub-assets.com/01a16d55-ea89-77b8-87fc-13ead1f9f7c0/Screenshot%20From%202026-10-24%2011-47-48.png)

## How it works

When you submit a secret, the server uses it and current minute, counted from T0 and encrypted using a rotating key, to create a SHA512. That hash is used as a seed for random number generator, and mod 2 of the resulting number is returned to you as the bit.

When you verify, the same thing happpens, and computed values are compared with the values you input in the request.

## Tech stack

Safe-bit is made using python with FastAPI. The frontend is made with plain HTML+CSS+JS.

## Deployment

Copy the [compose file](compose.yaml) to your file system, adjust variables and run it:

```bash
docker compose up -d
# Or if you use podman
podman compose up -d
```

[Quadlet file](quadlet/safe-bit.container) is also available.

To run it, copy it to `~/.config/containers/systemd/` (don't forget about the volume file) and restart systemd:

```bash
systemctl --user daemon-reload
systemctl --user start safe-bit.service
```

If deployed using compose/qudlet files, the database will be in "safe-bit" docker/podman volume.

In order to comply with AGPL 3.0 License, if you modify the program, you must publish the source. If you do so, you should change `SOURCE_CODE_LINK` (it affects the footer on frontend).

Native installations are not supported.

### Envinronment variable reference

| Variable           | Required | Default                         | Meaning                                                                                                   |
| ------------------ | -------- | ------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `SAFE_BIT_HOST`    | No       | `0.0.0.0`                       | Address the server listens on. Outside the container the fallback is `127.0.0.1`                          |
| `SAFE_BIT_PORT`    | No       | `8000`                          | Port the server listens on, between 1 and 65535. Remember to adjust the published port as well            |
| `T0`               | No       | `2026-09-14T00:00:00+00:00`     | Date and time since which the server time is counted. The default value is the day I started developement |
| `KEY_VALIDITY`     | No       | `10080`                         | Key rotation time in minutes                                                                              |
| `DB_PATH`          | No       | `/var/lib/safe-bit/app.sqlite3` | Path to the database file. The whole directory needs to be writable by the service                        |
| `ALLOWED_DRIFT`    | No       | `5`                             | How much in the past, in comparision to the server time the request needs to be                           |
| `OPERATOR_NAME`    | Yes      | ``                              | Operator name, used in the privacy policy                                                                 |
| `CONTACT_EMAIL`    | Yes      | ``                              | Contact email to the operator, used in the privacy policy                                                 |
| `HOSTING_LOG_NOTE` | No       | `""`                            | Hosting log note, used in the privacy policy, to indicate how messages are logged.                        |
| `SOURCE_CODE_LINK` | No       | this project's GitHub repo      | `http(s)` link shown in the page footer. Point it at your fork if you modified the code (AGPL)            |

### Footguns

- Changing `T0` after a key has been generated (corrupted database)
- Running `docker compose down -v` or the podman equivalent (deletes database)
- Using multiple deployments, such as kubernetes (not tested, sqlite works badly with concurrent network writes)
- Letting the server clock skew (breaks the system, running NTP/chrony is highly recommended)
- Exposing endpoints without your own rate limiting (endpoints aren't rate limited)
- Leaving `OPERATOR_NAME`, `CONTACT_EMAIL` and (when applies) `HOSTING_LOG_NOTE` unchanged (those values land in legally binding privacy policy)

## How to use

The whole procedure is explained in [a dedicated doc](/docs/usage.md).

## Developement setup

TLDR: Use devenv; `dev-bash` to launch the dev server

[CONTRIBUTING.md](CONTRIBUTING.md)
