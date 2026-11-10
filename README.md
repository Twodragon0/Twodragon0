## Twodragon0

Security engineering — cloud security, DevSecOps, and the operational plumbing that
connects security appliances to the tools people actually use.

Most of what I publish here comes out of running those appliances in production and
finding the places where the tooling quietly disagrees with the device.

### Writing

| | | |
|---|---|---|
| **[tech.2twodragon.com](https://tech.2twodragon.com)** | Tech blog — security, cloud, DevSecOps | built from [`tech-blog`](https://github.com/Twodragon0/tech-blog) |
| **[twodragon.tistory.com](https://twodragon.tistory.com)** | Longer write-ups and course notes | |
| **[2twodragon.com](https://2twodragon.com)** | Personal site | |

The list below is refreshed daily from those feeds by
[`scripts/update_blog_posts.py`](scripts/update_blog_posts.py). Each blog gets its own
section on purpose — they publish at very different rates, and a single merged "latest N"
list silently drops the slower one.

<!-- BLOG-POSTS:START -->

**[Tech Blog](https://tech.2twodragon.com)**

- [2026년 11월 10일 주간 보안 다이제스트: 클라우드·악성코드·AI 에이전트 (29건)](https://tech.2twodragon.com/posts/2026/11/10/Tech_Security_Weekly_Digest_AWS_Data_Rust_Malware/)
- [2026년 11월 09일 주간 보안 다이제스트: 클라우드·BYOVD EDR·블록체인 (15건)](https://tech.2twodragon.com/posts/2026/11/09/Tech_Security_Weekly_Digest_Cloud_Data_Security_Agent/)
- [2026년 11월 08일 주간 보안 다이제스트: 제로데이·패치·쿠버네티스 (15건)](https://tech.2twodragon.com/posts/2026/11/08/Tech_Security_Weekly_Digest_AI_Rust_Vulnerability_Patch/)
- [2026년 11월 07일 주간 보안 다이제스트: AI 에이전트·패치·쿠버네티스 (30건)](https://tech.2twodragon.com/posts/2026/11/07/Tech_Security_Weekly_Digest_Kubernetes_Security_AI_AWS/)
- [2026년 11월 06일 주간 보안 다이제스트: 패치·AI 에이전트·클라우드 (30건)](https://tech.2twodragon.com/posts/2026/11/05/Tech_Security_Weekly_Digest_Threat_DeFi_AI_Cloud/)

**[Tistory](https://twodragon.tistory.com)**

- [클라우드 시큐리티 9기 3주차: AWS 보안 점검과 FinOps를 한 장의 운영표로 연결하기](https://twodragon.tistory.com/714)
- [클라우드 시큐리티 9기 2주차: AWS 네트워크·보안 아키텍처와 FinOps, 데이터센터·CPU·GPU까지](https://twodragon.tistory.com/713)
- [클라우드 시큐리티 9기 1주차 : 온프레미스 vs 클라우드 네트워크 아키텍처 비교부터 제로 트러스트 &amp; DevSecOps 핵심 정리](https://twodragon.tistory.com/712)
- [클라우드 시큐리티 9기 OT: AI 시대의 DevSecOps, GPU 인프라, 그리고 대체 불가능한 보안 거버넌스](https://twodragon.tistory.com/711)
- [클라우드 보안 과정 8기 9주차: DevSecOps 통합 및 AI 기반 보안 자동화](https://twodragon.tistory.com/710)

<sub>Updated 2026-11-10 07:27 UTC — see <code>scripts/update_blog_posts.py</code></sub>

<!-- BLOG-POSTS:END -->

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
