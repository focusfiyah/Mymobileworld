# integrate-whatsapp: Every bundled script and asset, by task

Moved verbatim from upstream SKILL.md (see SOURCE.md). Script paths are relative to the skill folder.

## Scripts

### Webhooks

| Script | Purpose |
|--------|---------|
| `list.js` | List webhooks |
| `get.js` | Get webhook details |
| `create.js` | Create a webhook |
| `update.js` | Update a webhook |
| `delete.js` | Delete a webhook |
| `test.js` | Send a test event |

### Messaging and templates

| Script | Purpose | Required ID |
|--------|---------|-------------|
| `list-platform-phone-numbers.mjs` | Discover business_account_id + phone_number_id | — |
| `list-connected-numbers.mjs` | List WABA phone numbers | business_account_id |
| `list-templates.mjs` | List templates (with filters) | business_account_id |
| `template-status.mjs` | Check single template status | business_account_id |
| `create-template.mjs` | Create a template | business_account_id |
| `update-template.mjs` | Update existing template | business_account_id |
| `send-template.mjs` | Send template message | phone_number_id |
| `send-interactive.mjs` | Send interactive message | phone_number_id |
| `upload-media.mjs` | Upload media for send-time headers | phone_number_id |

### Flows

| Script | Purpose |
|--------|---------|
| `list-flows.js` | List all flows |
| `create-flow.js` | Create a new flow |
| `get-flow.js` | Get flow details |
| `read-flow-json.js` | Read flow JSON |
| `update-flow-json.js` | Update flow JSON (creates new version) |
| `publish-flow.js` | Publish a flow |
| `get-data-endpoint.js` | Get data endpoint config |
| `set-data-endpoint.js` | Create/update data endpoint code |
| `deploy-data-endpoint.js` | Deploy data endpoint |
| `register-data-endpoint.js` | Register data endpoint with Meta |
| `get-encryption-status.js` | Check encryption status |
| `setup-encryption.js` | Set up flow encryption |
| `send-test-flow.js` | Send a test flow message |
| `delete-flow.js` | Delete a flow |
| `list-flow-responses.js` | List stored flow responses |
| `list-function-logs.js` | List function logs |
| `list-function-invocations.js` | List function invocations |

### OpenAPI

| Script | Purpose |
|--------|---------|
| `openapi-explore.mjs` | Explore OpenAPI (search/op/schema/where) |

Examples:
```bash
node scripts/openapi-explore.mjs --spec whatsapp search "template"
node scripts/openapi-explore.mjs --spec whatsapp op sendMessage
node scripts/openapi-explore.mjs --spec whatsapp schema TemplateMessage
node scripts/openapi-explore.mjs --spec platform ops --tag "WhatsApp Flows"
node scripts/openapi-explore.mjs --spec platform op setupWhatsappFlowEncryption
node scripts/openapi-explore.mjs --spec platform search "setup link"
```

## Assets

| File | Description |
|------|-------------|
| `template-utility-order-status-update.json` | UTILITY template with named params + URL button |
| `send-template-order-status-update.json` | Send-time payload for order_status_update |
| `template-utility-named.json` | UTILITY template showing button ordering rules |
| `template-marketing-media-header.json` | MARKETING template with IMAGE header |
| `template-authentication-otp.json` | AUTHENTICATION OTP template (COPY_CODE) |
| `send-interactive-buttons.json` | Interactive button message |
| `send-interactive-list.json` | Interactive list message |
| `send-interactive-cta-url.json` | Interactive CTA URL message |
| `send-interactive-location-request.json` | Location request message |
| `send-interactive-catalog-message.json` | Catalog message |
| `sample-flow.json` | Static flow example (no endpoint) |
| `dynamic-flow.json` | Dynamic flow example (with endpoint) |
| `webhooks-example.json` | Webhook create/update payload example |
