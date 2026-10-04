# Guion de 120 minutos — 100 % demo en vivo

Título: **Copilot Agent Mode: lo que pasa cuando le das el control**.
Subtítulo: Demos en vivo de un agente resolviendo (y rompiendo) código real, y cómo dirigirlo, limitarlo y auditarlo.

## Preparación de la operadora

Ensaya cada escenario con el modelo y la licencia del día. Abre la terminal del controlador en la raíz y VS Code solo en la copia de ensayo. Ten el HTML del último check visible. Cada transición usa `reset --scenario NOMBRE` y un chat nuevo. El reset conserva el trabajo anterior.

No expongas soluciones mientras Copilot investiga. No describas un archivo fuera del workspace como inaccesible a la terminal. Usa datos ficticios y aprobación manual. Si muestras el runner Docker, constrúyelo antes del evento y prueba sus límites.

## Escenas y tiempos

| Minuto | Escena | Acción en vivo | Pregunta a la sala |
|---|---|---|---|
| 00–10 | ¿Y esto para qué me sirve? | Mostrar incidente; pedir explicación, plan y ejecución con la interfaz disponible. Ver modelo y consumo. | ¿Qué permiso hace falta para cada paso? |
| 10–30 | Nadie sabe qué hace el legado | `archaeology`: mapa con arqueólogo/MCP; comparar nota antigua y SQL; migrar fragmento. | ¿Qué fuente creen y qué prueba lo demuestra? |
| 30–50 | Viernes 17:00 | `retry`: reproducir, corregir, comprobar invariantes. Comparar dirección controlled/exploratory si el tiempo permite. | ¿Con qué evidencia declararían resuelto el incidente? |
| 50–75 | El junior pegó la conexión | `injection`: canario ficticio, documento envenenado y SQL concatenado. | ¿La nota del proveedor puede autorizar una acción? |
| 75–85 | Pausa | Si está habilitado, iniciar antes el agente remoto con un ticket claramente delimitado. | — |
| 85–100 | Pedí una cosa, tocó demasiadas | `scope`: aviso simulado; comparar petición abierta y límite explícito. Medir diff real. | ¿Qué cambio extra aceptarían y por qué? |
| 100–115 | ¿Aprobarías este PR? | PR draft preparado o cambio real del agente. Mostrar `review`; opcional `green` como segunda ronda. | Votar antes de revelar los checks independientes. |
| 115–120 | El lunes | Recorrer checklist y acordar un caso propio con evidencia en dos semanas. | ¿Qué control adoptarían primero? |

Son 110 minutos de contenido y 10 de pausa. `green` es un experimento independiente disponible para ensayar, pero se integra como variante en la escena de revisión para respetar las dos horas.

## Escena central: libreto de 20 minutos

1. **0–2:** «La carga termina, el sistema está verde, pero el cierre no cuadra». Mostrar ticket y logs.
2. **2–4:** ejecutar `unit`, `demo`, `check`. Pedir hipótesis sin revelar solución.
3. **4–6:** abrir Copilot; pedir plan y contraejemplo, mirar herramientas disponibles.
4. **6–13:** dejar trabajar; comentar decisiones observables, no adivinar razonamiento interno.
5. **13–17:** revisar diff y ejecutar verificador. Si deduplicó por pedido, contrastar pagos parciales.
6. **17–20:** pedir voto y justificarlo con evidencia. Registrar pendientes.

Objetivo correcto: COP 23000, USD 2500; segunda carga inserta cero eventos. La clave es comercio + evento, no pedido. No conviertas esto en una explicación inicial: es material del facilitador.

## Si algo se sale del guion

- El agente actúa correctamente: mostrar qué evidencia permite confiar en ese cambio. No intentar forzar un error.
- El agente no termina en 7 minutos: interrumpir, guardar diff y explicar lo pendiente.
- Recuperación: `python3 lab.py recover --reference`; decir «aplico un parche preparado para continuar la discusión».
- Quedan cambios fuera de alcance: mostrarlos; recuperar no los elimina. `reset` crea otra copia y archiva el ensayo.
- MCP bloqueado: leer el catálogo JSON y declarar la función no demostrada.
- Agente remoto demora: mostrar estado real y usar el PR draft preparado, identificado como tal.
- Caída de Internet: el laboratorio y verificador siguen funcionando; discutir un parche preparado sin afirmar que hubo una ejecución de Copilot.

## Cómo comparar sin vender una falsa garantía

Mantén commit inicial, escenario, prompt y modelo. Cambia solo el perfil y abre chat nuevo. Registra duración, archivos cambiados, tests conservados, checks, intervenciones y consumo si la interfaz lo reporta. No prometas «40 contra 4 archivos» ni que un perfil represente a todas las startups o bancos.

## Entregables del asistente

[Checklist](../docs/CHECKLIST.md), prompts, agentes, reglas del repo, instrucciones de prueba y registro de evidencia. No requiere labs durante la sesión.
