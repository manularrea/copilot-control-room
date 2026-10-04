# Issues, PR y decisiones de publicación

Los issues del workshop son tickets sintéticos. No representan incidencias de una empresa ni contribuciones de terceros.

El PR de demostración `demo/review-candidate` propone deliberadamente omitir devoluciones. Debe permanecer **draft y sin fusionar**. Su CI debe fallar en la validación del negocio aunque pase la suite heredada. Es un caso de auditoría preparado, no una salida atribuida a Copilot.

## Ensayar con el agente en la nube

1. Comprueba disponibilidad y presupuesto en tu cuenta/organización.
2. Elige el ticket de `retry` como contexto y especifica una rama nueva.
3. Indica que el bug vive en la variante del escenario. Pide un test de regresión y una propuesta de corrección; no pidas arreglar main, que ya contiene la referencia correcta.
4. Inicia el trabajo antes de la pausa. Muestra estado y logs reales cuando retomes.
5. Revisa el diff y ejecuta los controles. La aceptación actual de la infraestructura espera que los fixtures sigan rotos; si el PR modifica un fixture para corregirlo, habrá que revisar conscientemente la expectativa del test de infraestructura o mantener la corrección en una rama de solución. No borrar checks para lograr verde.
6. Si el agente remoto no está disponible, utiliza el agente local y presenta su diff. No atribuyas el PR preparado al agente.

Para una demo remota más directa, exporta la copia de ensayo a una rama/repo dedicado y añade un pipeline con el verificador tomado de un commit de confianza. No copies secretos ni soluciones. Este repo no crea automáticamente otra cuenta ni inicia consumo de agentes.

## Configurar main antes de simular gobierno empresarial

En Settings → Rules → Rulesets, según las funciones disponibles para tu plan:

- Aplicar la regla a main.
- Exigir PR y aprobación de otro humano si habrá cofacilitador.
- Exigir los checks `test (3.11)` y `test (3.12)` de Workshop quality, tras observar sus nombres reales en el primer run.
- Exigir resolución de conversaciones y bloquear force push/eliminación.
- Configurar aprobaciones de Copilot para que no satisfagan el requisito humano.
- Revisar quién puede omitir las reglas; demostrarlo en pantalla.

Con una sola persona no podrás aprobar tu propio PR para cumplir una regla que exija otra revisión humana. Para el workshop, basta llegar a «listo para revisión»; no necesitas fusionarlo. La disponibilidad de protecciones en repos privados depende del plan.

Este documento es una guía de configuración, no una afirmación de que esas reglas estén activas.
