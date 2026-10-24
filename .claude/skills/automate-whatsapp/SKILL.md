---
name: automate-whatsapp
description: Builds and debugs Kapso WhatsApp automations: workflows and their graphs, triggers, Project Events, functions, AI agent nodes and executions. Use for a WhatsApp chatbot, auto-reply, keyword reply, lead intake or booking flow, or an AI agent on WhatsApp built in Kapso, or when someone says Kapso workflow. For connecting a number, webhooks and sending messages use integrate-whatsapp; for logs and failed messages use observe-whatsapp.
---

# Automate WhatsApp

## Ralph's setup

Account, API key, CLI install and approval limits: the `integrate-whatsapp` skill, section "Ralph's setup". Read [references/rules.md](references/rules.md) before any graph or function edit.

## When to use

Use this skill to build and run WhatsApp automations: workflow CRUD, graph edits, WhatsApp and Project Event triggers, Project Event emissions, executions, function management, webhook tools, and MCP tools.

## Setup

Preferred path:
- Kapso CLI installed and authenticated (`kapso login`)
- For workflow and function edits, use source-controlled projects with `kapso link`, `kapso pull`, `kapso build`, and `kapso push`
- For workflow code, use `@kapso/workflows` and export a `Workflow` instance from `workflow.js` or `workflow.ts`

Fallback path:
Env vars:
- `KAPSO_API_BASE_URL` (host only, no `/platform/v1`)
- `KAPSO_API_KEY`

## How to

### Edit workflows locally

Use this path first when the user is working in, or can create, a local repo.

```bash
npm install -g @kapso/cli
npm install --save-dev @kapso/workflows
kapso login
kapso link --project <project-id>
kapso pull
```

Edit `workflows/<workflow-slug>/workflow.js` or `workflow.ts` with `@kapso/workflows`:

```ts
import { START, Workflow } from "@kapso/workflows";

const workflow = new Workflow("inbound-support", {
  name: "Inbound Support",
  status: "draft",
});

workflow.addTrigger({
  type: "inbound_message",
  phoneNumberId: "<phone-number-id>",
});

workflow.addNode(START, {
  position: { x: 100, y: 100 },
});

workflow.addNode("reply", {
  type: "send_text",
  message: "Thanks for reaching out.",
});

workflow.addEdge(START, "reply");

export default workflow;
```

Build and push:

```bash
kapso build
kapso push --dry-run
kapso push workflow <workflow-slug>
```

Use `kapso push` to push every local function and workflow. See `references/local-workflow-source.md` for repo layout, source-file behavior, and JSON-only editing.

### Discover phone numbers first

Preferred path:
1. Check project state: `kapso status`
2. List connected numbers: `kapso whatsapp numbers list --output json`
3. Resolve a display number when needed: `kapso whatsapp numbers resolve --phone-number "<display-number>" --output json`

Fallback path:
1. List number configs for triggers: `node scripts/list-whatsapp-phone-numbers.js`

### Edit a workflow graph through API scripts

Prefer local source sync for workflow edits. Use these scripts as a fallback for debugging, direct graph inspection, or API-only environments.

1. Fetch graph: `node scripts/get-graph.js <workflow_id>` (note the `lock_version`)
2. Edit the JSON (see graph rules below)
3. Validate: `node scripts/validate-graph.js --definition-file <path>`
4. Update: `node scripts/update-graph.js <workflow_id> --expected-lock-version <n> --definition-file <path>`
5. Re-fetch to confirm

For small edits, use `edit-graph.js` with `--old-file` and `--new-file` instead.

If you get a lock_version conflict: re-fetch, re-apply changes, retry with new lock_version.

### Manage triggers

1. List: `node scripts/list-triggers.js <workflow_id>`
2. Create: `node scripts/create-trigger.js <workflow_id> --trigger-type <type> --phone-number-id <id>`
3. Toggle: `node scripts/update-trigger.js --trigger-id <id> --active true|false`
4. Delete: `node scripts/delete-trigger.js --trigger-id <id>`

For inbound_message triggers, prefer `kapso whatsapp numbers resolve --phone-number "<display-number>" --output json` to get the exact `phone_number_id`. Fall back to `node scripts/list-whatsapp-phone-numbers.js` when the CLI is unavailable.

For project_event triggers, register or update the Project Event definition first when the user is defining an event type/schema:

```bash
node scripts/project-event-definitions.js create \
  --name conversation.csat_scored \
  --description "Customer satisfaction score for a conversation" \
  --property-schema '{"score":{"type":"number"},"reason":{"type":"string"}}'
```

Then create the trigger:

```bash
node scripts/create-trigger.js <workflow_id> \
  --trigger-type project_event \
  --triggerable-attributes '{"event_name":"conversation.csat_scored","property_key":"score","operator":"gte","property_value":4}'
```

Definitions are metadata only. Do not emit a sample event just to register a name unless the user explicitly accepts that side effect.

### Debug executions

1. Search workflow logs first when you have an execution ID: `kapso logs search --query "<execution-id>" --source flow_event --filter flow_execution_id=<execution-id> --period 7d --limit 20 --output json`
2. List: `node scripts/list-executions.js <workflow_id>`
3. Inspect: `node scripts/get-execution.js <execution-id>`
4. Get value: `node scripts/get-context-value.js <execution-id> --variable-path vars.foo`
5. Events: `node scripts/list-execution-events.js <execution-id>`

## Notes

- Prefer file paths over inline JSON (`--definition-file`, `--code-file`)
- Use `observe-whatsapp` for cross-source Logs search when debugging a workflow alongside API calls, Meta events, or webhook deliveries.
- Variable CRUD (`variables-set.js`, `variables-delete.js`) is blocked - Platform API doesn't support it

## References

Moved out of this file to keep it short:
- [references/functions-and-sandbox-guide.md](references/functions-and-sandbox-guide.md) - Creating and deploying functions; agent nodes with remote sandbox repos
- [references/project-events-guide.md](references/project-events-guide.md) - Project Event definitions and workflows built on them
- [references/rules.md](references/rules.md) - Graph, function and execution-context rules
- [references/scripts-and-assets.md](references/scripts-and-assets.md) - Every bundled script and asset, by task

Read the references for the operation you are changing:
- [references/local-workflow-source.md](references/local-workflow-source.md) - Local workflow source edits and CLI sync
- [references/graph-contract.md](references/graph-contract.md) - Graph edits: schema, computed vs editable fields, and lock_version
- [references/node-types.md](references/node-types.md) - Adding or changing node configuration
- [references/workflow-overview.md](references/workflow-overview.md) - Execution behavior, state changes, and resumption

For function-only work, read the function references below; graph/source references are needed only if the workflow changes too. Other task-specific references:
- [references/execution-context.md](references/execution-context.md) - Context structure and variable substitution
- [references/triggers.md](references/triggers.md) - Trigger types and setup
- [references/agent-remote-sandbox.md](references/agent-remote-sandbox.md) - Remote sandbox behavior, repo resources, mounted paths
- [references/functions-reference.md](references/functions-reference.md) - Function management
- [references/functions-payloads.md](references/functions-payloads.md) - Payload shapes for functions

## Related skills

- `integrate-whatsapp` - Onboarding, webhooks, messaging, templates, flows
- `observe-whatsapp` - Debugging, logs, health checks
