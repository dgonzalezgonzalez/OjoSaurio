# Publicación GitHub (público)

## Checklist

1. Inicializa git.
2. Commit inicial.
3. Crea repo público en GitHub.
4. Sube rama principal.
5. Verifica CI verde.

## Comandos sugeridos

```bash
git init
git add .
git commit -m "feat: initial 20-20-20 beeper app"
gh repo create <repo-name> --public --source=. --remote=origin --push
```
