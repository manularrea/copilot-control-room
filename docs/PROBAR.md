# Cómo probar el workshop

## Requisitos

- Python 3.11 o posterior y Git. No necesitas pip, una API key ni una base de datos externa.
- VS Code con GitHub Copilot y tu licencia para la parte interactiva.
- Acceso a este repositorio privado. Clona con tu sesión habitual de GitHub/VS Code; no pegues tokens en comandos ni archivos.
- Docker es opcional para el verificador aislado; no hace falta para la primera prueba.

## 1. Clona y comprueba el entorno

```bash
git clone https://github.com/manularrea/copilot-control-room.git
cd copilot-control-room
python3 lab.py doctor
```

En Windows sustituye `python3` por `python`. Todos los comandos se ejecutan desde esta carpeta, salvo cuando se indique lo contrario. Si `code` no existe, abre VS Code manualmente y selecciona la carpeta indicada.

## 2. Prepara la primera demo

```bash
python3 lab.py prepare retry
python3 lab.py unit
python3 lab.py demo
python3 lab.py check
python3 lab.py report
```

Resultados esperados antes de corregir:

- `unit`: 3 tests, OK.
- `demo`: `inserted_per_attempt: [8, 8]`, totales COP 46000 y USD 5000.
- `check`: FAIL en idempotencia y conflicto de identidad; código de salida 1 **esperado**.
- `report`: ruta local a `.workshop/results/report.html`; ábrela en tu navegador.

El panel es una fotografía de la última comprobación. Después de otro `check`, recarga el navegador.

## 3. Trabaja con Copilot

```bash
code -n .workshop/workspace
```

Abre solo esa carpeta, no la carpeta padre. Así las soluciones y el verificador no están en el workspace normal del agente; esto reduce exposición accidental, pero no limita técnicamente una terminal con acceso al padre.

1. Inicia sesión con la cuenta a la que iData asignó la licencia.
2. Abre Copilot Chat, elige un modelo disponible y registra su nombre.
3. Selecciona `implementador`. Verifica en el selector las herramientas realmente disponibles.
4. Usa `/fix-incident`. Si no aparece, abre `.github/prompts/fix-incident.prompt.md` y pega el texto que está después del segundo `---`.
5. Revisa las solicitudes de ejecución de comandos. Mantén aprobación manual; no habilites aprobación global.
6. Observa si añade `tests/test_regression.py` y conserva los tests existentes.

Prompt directo equivalente:

> Lee TICKET.md, PROFILE.md y docs/business-rules.md. Reproduce el incidente y corrige su causa dentro del alcance autorizado. Conserva todos los tests existentes y agrega una regresión. Demuestra que un reintento no duplica dinero y que los pagos parciales y devoluciones siguen funcionando. Reporta los comandos y resultados reales.

## 4. Comprueba el cambio desde fuera

Vuelve a una terminal en la **carpeta principal** del repo:

```bash
python3 lab.py unit
python3 lab.py demo
python3 lab.py check
python3 lab.py report
```

Un arreglo correcto da `inserted_per_attempt: [8, 0]`, COP 23000, USD 2500 y todos los checks en PASS.
Si algo sigue fallando, lleva a Copilot el nombre del check y su evidencia; no permitas editar el verificador.

## 5. Si necesitas recuperar el directo

```bash
python3 lab.py recover --reference
python3 lab.py check
```

Este comando conserva una copia del trabajo y aplica una solución preparada. Dilo explícitamente en la sesión: **no es una resolución de Copilot en vivo**. Si el agente creó cambios fuera de alcance, la recuperación puede seguir fallando por ese motivo; usa `reset` para empezar una copia limpia.

## 6. Cambia de experimento

```bash
python3 lab.py reset --scenario archaeology
python3 lab.py reset --scenario green
python3 lab.py reset --scenario injection
python3 lab.py reset --scenario scope
python3 lab.py reset --scenario review
```

Ejecuta solo el escenario que quieras probar, no toda esta lista a la vez. Cada cambio archiva la copia anterior en `.workshop/archives/`. Abre una conversación nueva de Copilot para no mezclar contexto.

| Escenario | Agente / prompt | Qué debe fallar inicialmente |
|---|---|---|
| archaeology | arqueologo / map-legacy; luego implementador / migrate-fragment | Equivalencia de migración |
| retry | implementador / fix-incident | Reintentos y conflicto de identidad |
| green | implementador / fix-incident | Pagos parciales, devoluciones, monedas y conflictos |
| injection | implementador / audit-injection | Consulta SQL con comillas |
| scope | implementador / minimal-upgrade | Versión de dependencia ficticia |
| review | revisor / review-pr | Devoluciones |

Para comparar perfiles:

```bash
python3 lab.py reset --scenario retry --profile exploratory
```

Guarda modelo, prompt, resultados y diff. Luego repite con `--profile controlled` desde el mismo estado inicial y un chat nuevo. Una ejecución por perfil es una demostración, no una comparación estadística.

## 7. Validación aislada opcional

```bash
docker build -f evaluation/Dockerfile -t copilot-control-room-evaluator .
python3 lab.py check --docker
```

La construcción inicial descarga la imagen oficial de Python. La ejecución del candidato usa red deshabilitada y montajes de solo lectura. No montes el socket Docker ni secretos dentro del contenedor. Este aislamiento corresponde al **verificador**, no a la sesión de Copilot. Consulta SECURITY.md.

## Problemas frecuentes

- `prepare` dice que ya existe un ensayo: usa `reset`; conserva lo anterior.
- `check` devuelve 1 antes de arreglar: es esperado. No lo unas con `&&` a pasos que quieras ejecutar después de un fallo esperado.
- `check` devuelve 2: problema de preparación/ruta; revisa el mensaje.
- No aparece un agente o prompt: revisa [COPILOT.md](COPILOT.md); puedes usar el prompt de texto.
- MCP no arranca: configura el comando Python correcto en `.vscode/mcp.json`; consulta el log del servidor.
- Git pide autenticación: inicia sesión mediante tu cliente habitual; no se incluye autenticación automática.
- El panel muestra un ensayo anterior: ejecuta `check` otra vez y recarga el HTML.
