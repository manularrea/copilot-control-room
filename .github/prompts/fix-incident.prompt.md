---
name: fix-incident
description: Reproduce y corrige el incidente sin debilitar las pruebas.
agent: implementador
---
Lee TICKET.md, PROFILE.md y docs/business-rules.md. Reproduce el incidente, explica su causa y corrige solo los archivos autorizados. Conserva todos los tests existentes y agrega tests/test_regression.py. Demuestra que un reintento no duplica dinero y que pagos parciales y devoluciones se conservan. Termina con comandos ejecutados, resultados y pendientes.
