## Twodragon0

Security engineering — cloud security, DevSecOps, and the operational plumbing that
connects security appliances to the tools people actually use.

Most of what I publish here comes out of running those appliances in production and
finding the places where the tooling quietly disagrees with the device.

### Upstream contributions

**Zscaler MCP Server** — [`zscaler/zscaler-mcp-server`](https://github.com/zscaler/zscaler-mcp-server)

- [**#95**](https://github.com/zscaler/zscaler-mcp-server/issues/95) — the entitlement
  filter removed tool families (`ztw_*`, `zid_*`, `zins_*`) that the *same token* could
  reach with HTTP 200. The cause was three product codes missing from `PRD_TO_SERVICE`,
  not a permission boundary — so it surfaced to operators as "I must not have access."
- [**#98**](https://github.com/zscaler/zscaler-mcp-server/issues/98) — a missing tenant
  identifier was reported as `missing OneAPI credentials`, sending operators to re-check
  a client ID and secret that were working fine. The stated blast radius was wrong too.

  Both were reproduced against a live OneAPI tenant and **shipped in v0.15.2
  (2026-08-13)**. The three mappings in the release match the ones reported, and the
  commit comment cites issue #95. To be precise about what happened: the maintainer
  implemented the fix in their own PR — **the patches I opened were not merged.**

**FortiGate MCP Server** — [`alpadalar/fortigate-mcp-server`](https://github.com/alpadalar/fortigate-mcp-server)

- [**PR #8**](https://github.com/alpadalar/fortigate-mcp-server/pull/8) — two defects that
  return **HTTP 200 with wrong data**, which is the kind that gets trusted rather than
  noticed:
  - `get_routing_table` read `dst`, the spelling used by the *config* endpoint
    (`cmdb/router/static`). The *state* endpoint it actually calls (`monitor/router/ipv4`)
    emits `ip_mask` — so every row rendered `Route: N/A`.
  - `get_interface_status` sent a parameter name FortiOS silently ignores, returning the
    full interface set no matter which name you asked for. Fixing the name alone returns
    *zero* results, because that endpoint excludes VLAN and aggregate interfaces by
    default — precisely the ones you'd look up by name.

  Verified on FortiOS v7.6.7. The regression tests assert on the shape of the outgoing
  request rather than the status code, since both defects are well-formed at the HTTP
  layer. **Submitted, not merged — CI has not run yet** (first-time-fork approval gate).
- [**Issue #9**](https://github.com/alpadalar/fortigate-mcp-server/issues/9) — asks
  whether the project's frozen tool surface can admit read-only DHCP and zone tools,
  rather than adding them unilaterally in a PR.

---

<sub>Reach me through the repositories above.</sub>
