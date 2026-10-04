# El reintento que cobra dos veces

**Incidente ficticio para el workshop.** No describe a un cliente real.

La carga nocturna se reintentó tras un timeout. Los logs dicen completed, pero el cierre tiene importes duplicados. Reproduce el incidente y corrige su causa sin descartar eventos legítimos.

## Alcance autorizado

- `app/ledger.py`
- `tests/test_regression.py`
- `docs/incident.md`

Máximo cuatro archivos. Conserva los tests existentes, workflows y contratos.
Cualquier otro cambio debe proponerse como pendiente, no ejecutarse.

## Criterio de aceptación

Cumplir docs/business-rules.md y aportar una prueba de regresión que distinga el bug del arreglo.
La operadora ejecutará la validación independiente desde la carpeta principal del laboratorio.
No accedas a soluciones de referencia ni cambies el verificador.

## Evidencia inicial

```bash
python3 -m unittest discover -s tests -v
python3 -m app.cli
```

En el chat explica hipótesis, evidencia, archivos modificados y riesgos pendientes.
