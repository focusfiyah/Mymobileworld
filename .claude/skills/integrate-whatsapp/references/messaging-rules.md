# integrate-whatsapp: Embedding the inbox and template rules

Moved verbatim from upstream SKILL.md (see SOURCE.md). Script paths are relative to the skill folder.

### Embed the inbox

Use Platform API inbox embeds when the user wants to place Kapso's inbox inside their own app.

Create:
- `POST /platform/v1/inbox_embeds`
- Envelope: `inbox_embed`
- Public scopes: `project`, `customer`, `phone_number`
- `scope_id` is blank for `project`, a customer UUID for `customer`, and WhatsApp `phone_number_id` for `phone_number`
- `language` controls the embedded inbox UI language; supported values are `en` and `es`
- Create returns `token` and `embed_url` once. Store `embed_url`; list/get/update omit secrets.

Example:
```json
{
  "inbox_embed": {
    "name": "Support inbox",
    "scope_type": "phone_number",
    "scope_id": "1234567890",
    "allowed_origins": ["https://app.example.com"],
    "default_mode": "system",
    "language": "es"
  }
}
```

Manage:
- `GET /platform/v1/inbox_embeds`
- `GET /platform/v1/inbox_embeds/:id`
- `PATCH /platform/v1/inbox_embeds/:id`
- `DELETE /platform/v1/inbox_embeds/:id` (revokes)

### Template rules

Creation:
- Use `parameter_format: "NAMED"` with `{{param_name}}` (preferred over positional)
- Include examples when using variables in HEADER/BODY
- Use `language` (not `language_code`)
- Don't interleave QUICK_REPLY with URL/PHONE_NUMBER buttons
- URL button variables must be at the end of the URL and use positional `{{1}}`
- For a `REQUEST_CONTACT_INFO` button, omit `text`; WhatsApp supplies the label

Send-time:
- For NAMED templates, include `parameter_name` in header/body params
- URL buttons need a `button` component with `sub_type: "url"` and `index`
- Media headers use either `id` or `link` (never both)
