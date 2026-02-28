# Event Catalog: {domain}

**Профиль:** Standard+
**Последнее обновление:** {YYYY-MM-DD}

## События

| Event name | Version | Producer | Consumers | Schema |
|---|---|---|---|---|
| `{domain}.{entity}.{action}` | `1.0.0` | `{service}` | `{service-list}` | `contracts/schemas/{event}.schema.json` |

## {domain}.{entity}.{action} v1.0.0

**Триггер:** {когда публикуется}

**Payload:**

```json
{
  "eventId": "{uuid}",
  "occurredAt": "{ISO8601}",
  "data": {
    "{field}": "{value}"
  }
}
```

**Семантика:** {что означает, что делать consumer-ам}
