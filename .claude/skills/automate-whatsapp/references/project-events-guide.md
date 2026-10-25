# automate-whatsapp: Project Event definitions and workflows built on them

Moved verbatim from upstream SKILL.md (see SOURCE.md). Script paths are relative to the skill folder.

### Manage Project Event definitions

Use definitions for event names, descriptions, and flat scalar property schemas. Emitted events are separate records created by `POST /platform/v1/events`, `emit_event` nodes, Function node `project_events`, or Agent node `emit_event`.

1. List: `node scripts/project-event-definitions.js list`
2. Create/update by name: `node scripts/project-event-definitions.js create --name <event.name> [--description <text>] [--property-schema <json>]`
3. Update by ID: `node scripts/project-event-definitions.js update --definition-id <id> [--name <event.name>] [--description <text>] [--property-schema <json>]`

### Build workflows with Project Events

Use this checklist when a workflow needs to remember or react to durable business facts:

1. Define the event first when the user is introducing a new event name or schema.
2. Use `project_event` triggers when a workflow should react to an emitted event.
3. Use an `emit_event` node for deterministic workflow-step emission.
4. Use Function node `project_events` when emission depends on function code output.
5. Use Agent node `emit_event` only when the agent should decide whether/when to record the fact. Enable the `emit_event` default tool and configure allowed event definitions before relying on it.

Project-event-triggered workflows are observers and cannot emit Project Events. Do not add event emission to a workflow that starts from a Project Event trigger.
