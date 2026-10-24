# automate-whatsapp: Graph, function and execution-context rules

Moved verbatim from upstream SKILL.md (see SOURCE.md). Script paths are relative to the skill folder.

## Graph rules

- Exactly one start node with `id` = `start`
- Never change existing node IDs
- Use `{node_type}_{timestamp_ms}` for new node IDs
- Non-decide nodes have 0 or 1 outgoing `next` edge
- Decide edge labels must match `conditions[].label`
- Edge keys are `source`/`target`/`label` (not `from`/`to`)

For full schema details, see `references/graph-contract.md`.

## Function rules

```js
async function handler(request, env) {
  // Parse input
  const body = await request.json();
  // Use env.KV and secrets as needed
  return new Response(JSON.stringify({ result: "ok" }));
}
```

- Do NOT use `export`, `export default`, or arrow functions
- Return a `Response` object

## Execution context

Always use this structure:
- `vars` - user-defined variables
- `system` - system variables
- `context` - channel data
- `metadata` - request metadata
