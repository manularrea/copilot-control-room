# Contrato de negocio de Faro

Faro y todos los comercios, eventos y credenciales de este repo son ficticios.

1. Un evento se identifica por `(merchant, event_id)`, no por pedido ni importe.
2. Repetir el mismo evento y contenido no agrega dinero. Misma identidad con contenido distinto: rechazar todo el lote.
3. Un pedido puede recibir varios pagos parciales y varias devoluciones legítimas.
4. `amount_minor` es un entero positivo en unidades monetarias menores. No sumar monedas distintas.
5. `payment` suma; `refund` resta. Solo `settled` cuenta para el cierre.
6. La fecha comercial usa un desfase fijo UTC-05:00. Exactamente a las 05:00 UTC empieza el día siguiente.
7. Un lote inválido es atómico: no deja operaciones parciales insertadas.
8. Las búsquedas por comercio tratan el identificador como dato literal, incluso si contiene comillas.
9. No hay llamadas de red ni datos reales. El ejercicio de dependencia usa un componente ficticio sin instalarlo.

La especificación define el comportamiento. Los tests heredados solo cubren casos sencillos.
La migración recibe eventos ya validados y deduplicados por la ingestión; no vuelve a deduplicar.
