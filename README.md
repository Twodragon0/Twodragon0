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

- [2026년 09월 13일 주간 보안 다이제스트: 제로데이·클라우드·AI 에이전트 (18건)](https://tech.2twodragon.com/posts/2026/09/13/Tech_Security_Weekly_Digest_AWS_AI_Agent_Data/)
- [2026년 09월 12일 주간 보안 다이제스트: AI 에이전트·BYOVD EDR·악성코드 (27건)](https://tech.2twodragon.com/posts/2026/09/12/Tech_Security_Weekly_Digest_Data_AI_AWS_Malware/)
- [2026년 09월 11일 주간 보안 다이제스트: 클라우드·랜섬웨어·악성코드 (30건)](https://tech.2twodragon.com/posts/2026/09/11/Tech_Security_Weekly_Digest_AWS_Threat_Go_Malware/)
- [2026년 09월 10일 주간 보안 다이제스트: 쿠버네티스·클라우드·AI 에이전트 (30건)](https://tech.2twodragon.com/posts/2026/09/10/Tech_Security_Weekly_Digest_Cloud_Threat_AI_Security/)
- [2026년 09월 09일 주간 보안 다이제스트: 쿠버네티스·AI 에이전트·보안 위협 (30건)](https://tech.2twodragon.com/posts/2026/09/09/Tech_Security_Weekly_Digest_API_Bitcoin_AI_GPT/)

**[Tistory](https://twodragon.tistory.com)**

- [클라우드 보안 과정 8기 9주차: DevSecOps 통합 및 AI 기반 보안 자동화](https://twodragon.tistory.com/710)
- [클라우드 보안 과정 8기 8주차: CI/CD와 Kubernetes 보안 실전 가이드 - DevSecOps 파이프라인부터 클러스터 보안까지](https://twodragon.tistory.com/709)
- [클라우드 보안 과정 8기 7주차: Docker &amp; Kubernetes 보안 실전 가이드 - 컨테이너 보안부터 클러스터 보안까지](https://twodragon.tistory.com/708)
- [클라우드 보안 과정 8기 6주차: AWS WAF/CloudFront 보안 아키텍처 및 GitHub DevSecOps 실전](https://twodragon.tistory.com/707)
- [클라우드 시큐리티 과정 8기 5주차: AWS Control Tower/SCP 기반 거버넌스 및 Datadog SIEM, Cloudflare 보안](https://twodragon.tistory.com/706)

<sub>Updated 2026-09-13 05:44 UTC — see <code>scripts/update_blog_posts.py</code></sub>

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
