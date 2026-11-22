Source: https://github.com/social-media-skills/skills (MIT), skills/youtube-shorts
Commit: f28cef2 (2026-10-15), copied 2026-11-22 for Then You Decide (Ralph 2026-11-22, after the first YouTube numbers: "If you need to look at some skills that you need, like a YouTube manager, let's look that up"; he tapped "Install + long-form one").
Copied: SKILL.md, references/ and LICENSE (evals/ left out, as with the sibling skills from this pack).
Scanned 2026-11-22 with SkillSpector 2.12.0 (--no-llm): 7/100 LOW SAFE, scripts=0. Findings: 2x MEDIUM "E1 External Transmission" at references/publishing-*.md line 9-10 = the WoopSocial API address written as text (nothing calls it); false positive.
Local use (differs from the upstream text):
- Publishing: WoopSocial does not apply to us. We post with yt.py / channels/story-niche-2d/channel/publish.py (YouTube), Zernio (TikTok @azariah2244) and Composio (Instagram @realgoodhustles, Facebook RG Hustles). Sibling skills it names (brand-profile, voice-builder, hook-writer, caption-writer, scheduling-and-queue) are routed by our social-growth-stack skill.
- Analytics: yt.py analytics (YouTube Analytics API v2) plus Ralph's YouTube Studio screenshots for what the API does not give (Shorts viewed vs swiped away, impressions, CTR).
- Channel rules for Then You Decide live in Dayone-ai channels/story-niche-2d/channel/MANAGE.md; Ralph's dated decisions there win over this skill.
