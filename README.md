# Certificate Service

Servicio para generación automática de certificados

## Estructura

```
app/
  api/            # rutas FastAPI
  core/           # config, logger
  schemas/        # modelos Pydantic
  services/       # lógica de negocio
  repositories/   # acceso a datos o storage externo
  utils/          # helpers
```

## Comandos

```bash
poetry install
cp .env.example .env
make run
```
