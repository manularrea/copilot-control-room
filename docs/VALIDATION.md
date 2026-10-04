# Validación de la versión inicial

Verificado localmente el 4 de octubre de 2026 con Python 3.12.14 y Git 2.51.1.

| Comprobación | Resultado |
|---|---|
| Suite heredada de la aplicación base | 3 tests, OK |
| Aceptación de negocio de la aplicación base | 12 comprobaciones, PASS |
| Infraestructura del laboratorio | 7 tests, OK; incluyen los seis escenarios y su recuperación |
| Variantes iniciales | Las seis conservan tests heredados verdes y fallan en la regla prevista |
| Soluciones preparadas | Las seis pasan la aceptación y el control de alcance |
| Protección contra sobrescritura accidental | Preparar sobre un ensayo existente se rechaza; reset lo archiva |
| Alteración de tests | Detectada por comparación de hashes y alcance |
| Copia del canario a informe | Detectada en la ruta ensayada |
| MCP por stdio | Handshake, listado, consulta conocida y rechazo de una ruta no válida verificados |
| Consulta SQL y migración de referencia | Coinciden con el cierre esperado |

No se ha ensayado una sesión interactiva de Copilot con la licencia de iData desde este entorno.
Docker no está instalado aquí: el runner opcional está incluido, pero su ejecución requiere validación en el equipo del evento.
Python 3.11 está incluido en la matriz de CI; su resultado remoto debe consultarse en Actions.
Las políticas corporativas, el consumo, la revisión de Copilot y la protección efectiva de main requieren comprobación en la cuenta correspondiente.

Los resultados locales no son una medición de calidad del modelo ni una certificación general de seguridad.
