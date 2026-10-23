# integrate-whatsapp: WhatsApp Flows: create, publish, data endpoints, rules, troubleshooting

Moved verbatim from upstream SKILL.md (see SOURCE.md). Script paths are relative to the skill folder.

## WhatsApp Flows

Use Flows to build native WhatsApp forms. Read `references/whatsapp-flows-spec.md` before editing Flow JSON.

### Create and publish a flow

1. Create flow: `node scripts/create-flow.js --phone-number-id <id> --name <name>`
2. Update JSON: `node scripts/update-flow-json.js --flow-id <id> --json-file <path>`
3. Publish: `node scripts/publish-flow.js --flow-id <id>`
4. Test: `node scripts/send-test-flow.js --phone-number-id <id> --flow-id <id> --to <phone>`

### Attach a data endpoint (dynamic flows)

1. Set up encryption: `node scripts/setup-encryption.js --flow-id <id>`
2. Create endpoint: `node scripts/set-data-endpoint.js --flow-id <id> --code-file <path>`
3. Deploy: `node scripts/deploy-data-endpoint.js --flow-id <id>`
4. Register: `node scripts/register-data-endpoint.js --flow-id <id>`

### Flow JSON rules

Static flows (no data endpoint):
- Use `version: "7.3"`
- `routing_model` and `data_api_version` are optional
- See `assets/sample-flow.json`

Dynamic flows (with data endpoint):
- Use `version: "7.3"` with `data_api_version: "3.0"`
- `routing_model` is required (defines valid screen transitions)
- See `assets/dynamic-flow.json`

### Data endpoint rules

Handler signature:
```js
async function handler(request, env) {
  const body = await request.json();
  // body.data_exchange.action: INIT | data_exchange | BACK
  // body.data_exchange.screen: current screen id
  // body.data_exchange.data: user inputs
  return Response.json({
    version: "3.0",
    screen: "NEXT_SCREEN_ID",
    data: { }
  });
}
```

- For customer-specific data or mutations, authorize the customer and resource using server-side state. `flow_token` alone is not proof of identity; see [request authentication](whatsapp-flows-spec.md#request-authentication-and-customer-authorization).
- Do not use `export` or `module.exports`
- Completion uses `screen: "SUCCESS"` with `extension_message_response.params`
- Do not include `endpoint_uri` or `data_channel_uri` (Kapso injects these)

### Troubleshooting

- Search Logs before drilling into per-resource endpoints: `kapso logs search --query "<wamid-flow-id-request-id-or-endpoint>" --period 7d --source all --limit 20 --output json`
- Preview shows `"flow_token is missing"`: flow is dynamic without a data endpoint. Attach one and refresh.
- Encryption setup errors: enable encryption in Settings for the phone number/WABA.
- OAuthException 139000 (Integrity): WABA must be verified in Meta security center.
