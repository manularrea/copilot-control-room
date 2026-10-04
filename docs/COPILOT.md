# Configurar Copilot para el ensayo

Revisado contra documentación oficial el 3 de octubre de 2026. La interfaz y las políticas de la organización pueden cambiar. No se ha ejecutado una sesión con la licencia de iData desde este entorno.

## Antes del evento

Registra versión de VS Code/extensión, cuenta con licencia, modelo disponible y política de herramientas. Comprueba con la administración de iData el presupuesto y si están habilitados MCP, agente en la nube y code review. La licencia no permite inferir esas políticas.

La documentación actual de GitHub usa AI Credits y tokens; algunos planes anuales anteriores conservan premium requests. Consulta el panel de tu cuenta y registra el consumo real, sin estimar una cuota universal.

## Agentes

Abre solo `.workshop/workspace` y revisa las definiciones de `.github/agents/`:

| Agente | Herramientas solicitadas | Función |
|---|---|---|
| arqueologo | read, search, faro-catalog/* | Investigar sin edición ni terminal |
| implementador | read, search, edit, execute | Editar y probar con aprobación de comandos |
| revisor | read, search | Hallazgos con evidencia; no ejecuta pruebas |

Comprueba la lista efectiva de herramientas en tu instalación. Los nombres y disponibilidad dependen del harness; no añadas herramientas de escritura al arqueólogo para resolver un problema de configuración. Usa el modelo seleccionado en la interfaz: no hay modelos ni multiplicadores fijados en los archivos.

## Prompt files y compatibilidad

Los seis `.prompt.md` se invocan con `/nombre` en las interfaces que los cargan. La documentación de VS Code indica que Agent Host no carga prompt files; Local todavía los admite. Si tu interfaz no los muestra, selecciona el agente adecuado y pega el cuerpo del archivo. Ese camino conserva el ejercicio sin depender del comando slash.

## MCP local de solo lectura

1. Abre `.vscode/mcp.json` en la copia de ensayo.
2. Configura el ejecutable Python: `python3` en macOS/Linux; normalmente `python` en Windows.
3. Usa la acción de iniciar servidor disponible en VS Code. Revisa el archivo antes de confiar en él.
4. Comprueba que aparecen `list_objects` y `describe_object` del servidor `faro-catalog`.
5. En `arqueologo`, pide describir `daily_close` y mapear sus dependencias.

El servidor solo lee `catalog/dependencies.json`. No tiene conexión a un banco, red, SQL arbitrario ni acceso a rutas elegidas por el usuario. Las anotaciones de solo lectura describen las herramientas; el código es lo que implementa esa restricción.

Si una política bloquea MCP, usa el JSON como evidencia local y declara que esa ejecución no demostró MCP. No cambies políticas corporativas para hacer funcionar una demo.

## Aprobaciones

Mantén permisos manuales. Revisa herramientas, comandos y destinos. El repo no habilita autoaprobación. Los perfiles `controlled` y `exploratory` son estilos de dirección, no niveles de acceso.

Los content exclusions no están soportados en Edit/Agent Mode según la documentación consultada; no los presentes como protección para .env en este taller. Usa únicamente el canario ficticio incluido.

## Agente en VS Code, agente en la nube y revisión

Son superficies distintas. El laboratorio local funciona aunque el agente en la nube o la revisión de PR no estén habilitados.

Para la escena remota, usa un issue del workshop como contexto y una rama nueva. La asignación a Copilot inicia trabajo y puede consumir cuota. No se hace automáticamente al preparar el repo.

Copilot dispone de aprobaciones de PR en vista previa según políticas. Para representar aprobación humana obligatoria, configura el repositorio para que las aprobaciones de IA no satisfagan ese requisito y usa otro revisor humano cuando aplique. No confundas una recomendación escrita con un control de merge activo.

Fuentes: [REFERENCES.md](REFERENCES.md).
