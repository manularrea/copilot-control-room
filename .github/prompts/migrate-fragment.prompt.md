---
name: migrate-fragment
description: Corrige una migración con validación de equivalencia.
agent: implementador
---
Porta correctamente el fragmento de legacy/daily_close.sql en app/migration.py. Conserva fecha comercial UTC-05:00, devoluciones, estado y separación de monedas. Agrega tests/test_regression.py que compare la consulta SQL y Python con datos de borde; usa sqlite3 de la biblioteca estándar. Respeta el alcance de TICKET.md.
