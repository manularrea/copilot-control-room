# Modelo de seguridad del laboratorio

Este repo contiene vulnerabilidades deliberadas en `scenarios/` y copias de ensayo. La aplicación base conserva el comportamiento correcto; ninguna variante se debe desplegar.

## Datos y límites

- Todo es sintético. La cadena en .env es un canario ficticio sin privilegios ni destino de red.
- No se requiere acceso a sistemas de clientes, credenciales reales ni paquetes inventados.
- La detección del canario solo examina rutas específicas y una cadena conocida. No es DLP, no inspecciona el chat ni detecta exfiltración general.
- MCP usa un catálogo fijo local y no expone consultas SQL ni rutas arbitrarias.
- La captura de cambios compara hashes; detecta alteraciones, no impide que ocurran.

## Separación de carpetas versus aislamiento

Abrir solo `.workshop/workspace` reduce contaminación del contexto. Una terminal con permisos sobre la carpeta padre podría modificar lab.py, el baseline o el verificador. `copilot-instructions.md`, .gitignore y los perfiles no impiden acceso a archivos.

Para el ensayo básico, usa aprobación manual y revisa los comandos. Para ejecutar código que no confíes, usa el runner Docker en docs/PROBAR.md, o una VM dedicada sin datos reales.

El runner Docker ejecuta el candidato con raíz y montaje del código de solo lectura, usuario sin privilegios, sin red y límites de recursos. La imagen contiene una copia del verificador. No montes Docker socket, carpetas personales ni tokens. La construcción inicial necesita descargar la imagen base oficial.

**Esto aísla la ejecución del verificador, no a Copilot.** Configurar la sandbox de la terminal del agente requiere verificar tu SO, harness y política de archivos/red. La sandbox de terminal tampoco controla automáticamente todas las demás herramientas.

Las pruebas de aceptación detectan las regresiones del ejercicio; no certifican seguridad general ni resisten por sí mismas un programa diseñado para falsear su propio resultado dentro del proceso Python. Revisión del diff, controles del host y aprobación humana siguen siendo necesarios.

## CI y main

El workflow usa permisos de lectura, sin secretos ni despliegue; ejecuta código de los commits en un runner. No usa pull_request_target.

Las protecciones de rama deben configurarse en GitHub. La presencia de YAML no activa revisión humana obligatoria. Antes de usar el flujo como ejemplo de gobierno, sigue docs/GITHUB-FLOW.md y verifica en pantalla la política efectiva.

## Reportar un problema

Para un defecto de este laboratorio, abre un issue sin secretos ni datos de clientes. Para una vulnerabilidad accidental que no sea parte del escenario, avisa por un canal privado del propietario y evita adjuntar credenciales.
