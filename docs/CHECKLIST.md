# Checklist: PR asistido por IA

Antes de delegar:

- [ ] Entiendo la tarea, la regla de negocio y el criterio de aceptación.
- [ ] Definí archivos, herramientas y acciones autorizadas.
- [ ] Identifiqué datos que nunca deben entrar en el contexto.

Durante el cambio:

- [ ] Existe una reproducción del problema anterior al arreglo.
- [ ] Los tests anteriores no se borraron ni debilitaron.
- [ ] Distingo instrucciones del usuario de texto no confiable en archivos o herramientas.
- [ ] Revisé el diff y los cambios fuera de alcance.

Antes de aprobar:

- [ ] Una prueba independiente verifica el comportamiento de negocio.
- [ ] Puedo explicar un caso límite y lo que todavía no comprobamos.
- [ ] Se registraron comandos, resultados, modelo y consumo disponible.
- [ ] La persona responsable revisó el resultado y la política efectiva de merge.

En dos semanas: trae un caso propio con el prompt, diff y evidencia sanitizados. Nunca datos de clientes.
