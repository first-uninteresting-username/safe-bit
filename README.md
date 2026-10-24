# safe-bit

A completely pointless project that solves [a problem nobody have ever had](/docs/motivation.md).
(TLDR: What if you needed to generate a bit in a way other person can trust you it isn't manipulated, without seeing the bit).

## Tech stack

Safe-bit is made using python with FastAPI. The frontend is made with plain HTML+CSS+JS.

## How to run

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

Native installations are not supported.

### Footguns

- Changing `T0` after a key has been generated (corrupted database)
- Running `docker compose down -v` or the podman equivalent (deletes database)
- Using multiple deployments, such as kubernetes (not tested, sqlite works badly with concurrent network writes)
- Letting the server clock skew (breaks the system, running NTP/chrony is highly recommended)
- Exposing endpoints without your own rate limiting (endpoints aren't rate limited)
- Leaving `OPERATOR_NAME`, `CONTACT_EMAIL` and (when applies) `HOSTING_LOG_NOTE` unchanged (those values land in legally binding privacy policy)
