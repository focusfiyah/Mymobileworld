# automate-whatsapp: Every bundled script and asset, by task

Moved verbatim from upstream SKILL.md (see SOURCE.md). Script paths are relative to the skill folder.

## Scripts

### Workflows

| Script | Purpose |
|--------|---------|
| `list-workflows.js` | List workflows (metadata only) |
| `get-workflow.js` | Get workflow metadata |
| `create-workflow.js` | Create a workflow |
| `update-workflow-settings.js` | Update workflow settings |

### Graph

| Script | Purpose |
|--------|---------|
| `get-graph.js` | Get workflow graph + lock_version |
| `edit-graph.js` | Patch graph via string replacement |
| `update-graph.js` | Replace entire graph |
| `validate-graph.js` | Validate graph structure locally |

### Triggers

| Script | Purpose |
|--------|---------|
| `list-triggers.js` | List triggers for a workflow |
| `create-trigger.js` | Create a trigger |
| `update-trigger.js` | Enable/disable a trigger |
| `delete-trigger.js` | Delete a trigger |
| `list-whatsapp-phone-numbers.js` | List phone numbers for trigger setup |

### Project Events

| Script | Purpose |
|--------|---------|
| `project-event-definitions.js` | List, create, or update Project Event definitions |

### Executions

| Script | Purpose |
|--------|---------|
| `list-executions.js` | List executions |
| `get-execution.js` | Get execution details |
| `get-context-value.js` | Read value from execution context |
| `update-execution-status.js` | Force execution state |
| `resume-execution.js` | Resume waiting execution |
| `list-execution-events.js` | List execution events |

### Functions

| Script | Purpose |
|--------|---------|
| `list-functions.js` | List project functions |
| `get-function.js` | Get function details + code |
| `create-function.js` | Create a function, optionally with a public invoke endpoint |
| `update-function.js` | Update function code, public endpoint setting, or migrate a legacy wrapped function to passthrough |
| `deploy-function.js` | Deploy function to runtime |
| `invoke-function.js` | Invoke function with payload |
| `list-function-invocations.js` | List function invocations |

### OpenAPI

| Script | Purpose |
|--------|---------|
| `openapi-explore.mjs` | Explore OpenAPI (search/op/schema/where) |

Install deps (once):
```bash
npm i
```

Examples:
```bash
node scripts/openapi-explore.mjs --spec workflows search "variables"
node scripts/openapi-explore.mjs --spec workflows op getWorkflowVariables
```

## Assets

| File | Description |
|------|-------------|
| `workflow-linear.json` | Minimal linear workflow |
| `workflow-decision.json` | Minimal branching workflow |
| `workflow-agent-simple.json` | Minimal agent workflow |
| `workflow-customer-support-intake-agent.json` | Customer support intake |
| `workflow-interactive-buttons-decide-function.json` | Interactive buttons + decide (function) |
| `workflow-interactive-buttons-decide-ai.json` | Interactive buttons + decide (AI) |
| `workflow-api-template-wait-agent.json` | API trigger + template + agent |
| `function-decide-route-interactive-buttons.json` | Function for button routing |
| `agent-remote-sandbox-github-repo-example.json` | Agent node with remote sandbox + GitHub repo resource |
