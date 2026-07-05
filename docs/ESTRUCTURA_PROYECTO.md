# Estructura del proyecto ConcursoDocente

Proyecto real: `C:\ConcursoDocente`.

## Criterio de organizacion

- Las apps Django permanecen en la raiz porque Django las importa directamente desde `INSTALLED_APPS`.
- Los respaldos quedan en `_backups`.
- Los recursos de importacion y bancos procesados quedan en `_resources`.
- Los scripts auxiliares quedan en `scripts`.
- La documentacion operativa queda en `docs`.
- Las carpetas temporales de Codex no son la fuente de trabajo del proyecto.

## Archivos clave

- `manage.py`: entrada principal Django.
- `concurso_web/settings.py`: configuracion general.
- `.env`: credenciales locales, no se versiona.
- `.env.example`: plantilla segura sin secretos reales.
- `start-server.ps1`: arranque local en el puerto 8001.
- `docs/GUIA_FINAL_PRODUCCION.md`: pasos finales para Google, Wompi y correo.

## Arranque local

Desde `C:\ConcursoDocente`:

```powershell
.\start-server.ps1
```

URL local:

```text
http://127.0.0.1:8001/
```

## Estado del banco premium

- Total: 375 preguntas premium.
- Simulacros activos: 18.
- Simulacros por area: 5.
- Productos activos: 12.
