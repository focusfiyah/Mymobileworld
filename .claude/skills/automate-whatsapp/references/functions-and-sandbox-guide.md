# automate-whatsapp: Creating and deploying functions; agent nodes with remote sandbox repos

Moved verbatim from upstream SKILL.md (see SOURCE.md). Script paths are relative to the skill folder.

### Create and deploy a function

1. Write code with handler signature (see function rules below)
2. Create: `node scripts/create-function.js --name <name> --code-file <path> [--public-endpoint true]`
3. Deploy: `node scripts/deploy-function.js --function-id <id>`
4. Verify: `node scripts/get-function.js --function-id <id>`

Use `--public-endpoint true` when the function should be callable without `X-API-Key` via the Kapso-hosted invoke URL. This is only supported for Cloudflare functions.
New functions default to `invoke_response_mode=passthrough`, which returns the function body directly on successful invoke. Legacy wrapped functions can be migrated later with `update-function.js`.

### Set up agent node with remote sandbox repositories

Use this when the agent needs a remote ephemeral workspace to inspect or modify repository files during a workflow run.

1. Read `references/agent-remote-sandbox.md` for the execution model and field rules
2. Find model: `node scripts/list-provider-models.js`
3. Copy `assets/agent-remote-sandbox-github-repo-example.json` as a starting point, or edit the agent node under `data.config`
4. Set `sandbox_enabled: true`
5. Set `sandbox_network_mode` to `allow_all` or `allow_list`
6. If using `allow_list`, add extra outbound hosts in `sandbox_allowed_outbound_hosts`
7. Add GitHub repositories to `flow_agent_resources` with:
   - `resource_type: "github_repository"`
   - `repo_url`
   - `branch`
   - `pat`
8. Write the system prompt so it explicitly reads from `/workspace/repos/<repo-slug>` before making changes
9. Validate and update the graph

Notes:
- Remote sandbox is beta and free during the beta
- `sandbox_enabled` controls whether the remote workspace and sandbox tools are available
- Repository resources stay configured even if sandbox access is turned off later
- v1 supports GitHub repositories only
- Use a repository root URL, not a GitHub file URL or `tree/...` URL
- Repositories are mounted into `/workspace/repos/<repo-slug>` inside the remote sandbox
- Use `references/agent-remote-sandbox.md` and `references/node-types.md` for the exact shape
