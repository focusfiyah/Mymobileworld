# integrate-whatsapp: Connect WhatsApp: setup links, onboarding, detecting the connection

Moved verbatim from upstream SKILL.md (see SOURCE.md). Script paths are relative to the skill folder.

## Connect WhatsApp (setup links)

Preferred onboarding path (CLI):

1. Start onboarding: `kapso setup`
2. If setup is blocked, resolve context with:
   - `kapso projects list`
   - `kapso projects use <project-id>`
   - `kapso customers list`
   - `kapso customers new --name "<customer-name>" --external-id <external-id>`
   - `kapso setup --customer <customer-id>`
3. Complete the hosted onboarding URL
4. Confirm connected numbers: `kapso whatsapp numbers list --output json`
5. Resolve the exact number you want to operate: `kapso whatsapp numbers resolve --phone-number "<display-number>" --output json`

Fallback onboarding flow (direct API):

1. Create customer: `POST /platform/v1/customers`
2. Generate setup link: `POST /platform/v1/customers/:id/setup_links`
3. Customer completes embedded signup
4. Use `phone_number_id` to send messages and configure webhooks

Detect connection:
- Project webhook `whatsapp.phone_number.created` (recommended)
- Success redirect URL query params (use for frontend UX)

Verify webhook signatures before processing events. Redirect query parameters are untrusted UI hints; confirm the connection through the project-scoped API and bind it to the authenticated customer before updating records. See [connection detection](detecting-whatsapp-connection.md).

Recommended Kapso setup-link defaults:
```json
{
  "setup_link": {
    "allowed_connection_types": ["dedicated"],
    "provision_phone_number": true,
    "phone_number_country_isos": ["US"]
  }
}
```

Notes:
- `kapso setup` and `kapso whatsapp numbers new` use dedicated plus provisioning by default.
- Keep `phone_number_country_isos`, `phone_number_area_code`, `language`, and redirect URLs as optional overrides.

- Platform API base: `/platform/v1`
- Meta proxy base: `/meta/whatsapp/v24.0` (messaging, templates, media)
- Use `phone_number_id` as the primary WhatsApp identifier
