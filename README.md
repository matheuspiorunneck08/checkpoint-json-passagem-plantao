# Passagem de plantão — arquivos e JSON

Programa de terminal em Python que registra ocorrências de um sistema e gera
uma passagem de plantão em texto para a próxima equipe.

> Desenvolvido com auxílio de IA.

Contexto fictício: **AgendaFácil**, sistema de agendamento de consultas de uma clínica.

## Como executar

Requer Python 3. Na pasta dos arquivos:

```bash
python programa.py
```

## Funcionalidades

| Opção | O que faz | Arquivo |
|---|---|---|
| 1 | Registra ocorrência (serviço, descrição, prioridade, status, próxima ação) | `ocorrencias.json` |
| 2 | Lista todas as ocorrências | `ocorrencias.json` |
| 3 | Acrescenta uma anotação ao diário (modo `"a"`) | `diario.txt` |
| 4 | Exibe o diário (modo `"r"`) | `diario.txt` |
| 5 | Gera o resumo só com as ocorrências abertas (modo `"w"`) | `passagem.txt` |
| 6 | Sai | — |

Tratamento de erros:

- **JSON ausente:** começa com uma lista vazia.
- **Diário ausente:** informa "Nenhuma anotação registrada".
- **JSON inválido:** bloqueia cadastro, consulta e resumo sem alterar o arquivo; o diário continua funcionando.

## Arquivos

- `programa.py` — versão principal
- `programa_simples.py` — mesma funcionalidade só com recursos básicos (concatenação, `while` com condição)
- `ocorrencias.json`, `diario.txt`, `passagem.txt` — base gerada pelo teste entre integrantes

## Testes executados

**Teste entre integrantes:** duas execuções seguidas em uma pasta vazia.

- **Execução A:** 3 ocorrências (alta aberta, baixa aberta, alta resolvida) e 2 anotações.
- **Execução B:** confere os dados, cadastra uma ocorrência média aberta, faz 1 anotação e gera o resumo.
- **Resultado:** 4 ocorrências no JSON, 3 linhas no diário, 3 pendências no resumo e 1 de prioridade alta. ✅

| Teste adicional | Resultado |
|---|---|
| Arquivos ausentes | Consultas não encerram o programa com erro ✅ |
| Nova geração | Gerar duas vezes não duplica o resumo nem altera diário e JSON ✅ |
| Sem pendências (`[]`) | Contadores zerados e "Nenhuma pendência para o próximo plantão" ✅ |
| JSON inválido (`{erro}`) | Cadastro, consulta e resumo bloqueados; arquivo e resumo anterior preservados ✅ |
