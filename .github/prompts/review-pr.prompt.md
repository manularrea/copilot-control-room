---
name: review-pr
description: Revisa un cambio contra reglas de negocio antes de aprobar.
agent: revisor
---
Lee TICKET.md y docs/business-rules.md. Examina app/ledger.py con foco en devoluciones, reintentos y pagos parciales. Formula un contraejemplo por hallazgo. Separa evidencia disponible de tests no ejecutados. Devuelve aprobar/solicitar cambios como recomendación argumentada, nunca como aprobación efectiva del PR.
