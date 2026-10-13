# Passagem de plantão - AgendaFácil, sistema de agendamento de consultas
# Solução de referência para estudo

import json

NOME_SISTEMA = "AgendaFácil - Agendamento de Consultas"
ARQ_OCORRENCIAS = "ocorrencias.json"
ARQ_DIARIO = "diario.txt"
ARQ_PASSAGEM = "passagem.txt"


def avisar_json_invalido():
    print("\nERRO: o arquivo", ARQ_OCORRENCIAS, "está com conteúdo inválido.")
    print("Corrija o arquivo (ele deve conter uma lista JSON, por exemplo [])")
    print("ou restaure uma cópia válida. Cadastro, consulta de ocorrências e")
    print("geração do resumo ficam suspensos até a correção.")
    print("O arquivo não foi alterado.")


def carregar_ocorrencias():
    # None sinaliza JSON inválido: quem chama deve parar sem gravar nada
    try:
        with open(ARQ_OCORRENCIAS, "r", encoding="utf-8") as arquivo:
            ocorrencias = json.load(arquivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        avisar_json_invalido()
        return None

    if type(ocorrencias) != list:
        avisar_json_invalido()
        return None
    return ocorrencias


def salvar_ocorrencias(ocorrencias):
    with open(ARQ_OCORRENCIAS, "w", encoding="utf-8") as arquivo:
        json.dump(ocorrencias, arquivo, ensure_ascii=False, indent=4)


def pedir_texto(mensagem):
    texto = input(mensagem).strip()
    while texto == "":
        print("Campo obrigatório. Digite um valor.")
        texto = input(mensagem).strip()
    return texto


def pedir_opcao(mensagem, opcoes):
    while True:
        valor = input(mensagem).strip().lower().replace("é", "e")
        if valor in opcoes:
            return valor
        print("Valor inválido. Opções aceitas:", ", ".join(opcoes))


def pedir_dados_ocorrencia():
    print("\n--- Nova ocorrência ---")
    servico = pedir_texto("Serviço afetado: ")
    descricao = pedir_texto("Descrição: ")
    prioridade = pedir_opcao("Prioridade (alta/media/baixa): ", ["alta", "media", "baixa"])
    status = pedir_opcao("Status (aberto/resolvido): ", ["aberto", "resolvido"])

    if status == "resolvido":
        proxima_acao = "nenhuma"
    else:
        proxima_acao = pedir_texto("Próxima ação: ")

    return {
        "servico": servico,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": status,
        "proxima_acao": proxima_acao
    }


def registrar_ocorrencia():
    # Carrega antes de incluir: regravar só o registro novo apagaria os anteriores
    ocorrencias = carregar_ocorrencias()
    if ocorrencias is None:
        return

    ocorrencias.append(pedir_dados_ocorrencia())
    salvar_ocorrencias(ocorrencias)
    print("Ocorrência registrada. Total salvo:", len(ocorrencias))


def consultar_ocorrencias():
    ocorrencias = carregar_ocorrencias()
    if ocorrencias is None:
        return
    if len(ocorrencias) == 0:
        print("\nNão há ocorrências registradas.")
        return

    print("\n--- Ocorrências ---")
    for numero, ocorrencia in enumerate(ocorrencias, start=1):
        print(f"\n#{numero}")
        print("Serviço:", ocorrencia["servico"])
        print("Descrição:", ocorrencia["descricao"])
        print("Prioridade:", ocorrencia["prioridade"])
        print("Status:", ocorrencia["status"])
        print("Próxima ação:", ocorrencia["proxima_acao"])


def registrar_anotacao():
    print("\n--- Nova anotação ---")
    servico = pedir_texto("Serviço: ")
    anotacao = pedir_texto("Anotação: ")

    # Modo "a" acrescenta no fim; "w" apagaria o histórico do diário
    with open(ARQ_DIARIO, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{servico} — {anotacao}\n")
    print("Anotação registrada no diário.")


def consultar_diario():
    try:
        with open(ARQ_DIARIO, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        conteudo = ""

    if conteudo.strip() == "":
        print("\nNenhuma anotação registrada.")
    else:
        print("\n--- Diário ---")
        print(conteudo)


def filtrar_abertas(ocorrencias):
    abertas = []
    for ocorrencia in ocorrencias:
        if ocorrencia["status"] == "aberto":
            abertas.append(ocorrencia)
    return abertas


def contar_prioridade(ocorrencias, prioridade):
    total = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["prioridade"] == prioridade:
            total = total + 1
    return total


def montar_texto_passagem(abertas):
    texto = "PASSAGEM DE PLANTÃO\n"
    texto += f"Sistema: {NOME_SISTEMA}\n"
    texto += f"Ocorrências abertas: {len(abertas)}\n"
    texto += f"Abertas com prioridade alta: {contar_prioridade(abertas, 'alta')}\n\n"

    if len(abertas) == 0:
        return texto + "Nenhuma pendência para o próximo plantão\n"

    texto += "Pendências:\n"
    for numero, ocorrencia in enumerate(abertas, start=1):
        texto += f"\n{numero}. Serviço: {ocorrencia['servico']}\n"
        texto += f"   Descrição: {ocorrencia['descricao']}\n"
        texto += f"   Prioridade: {ocorrencia['prioridade']}\n"
        texto += f"   Próxima ação: {ocorrencia['proxima_acao']}\n"
    return texto


def gerar_passagem():
    ocorrencias = carregar_ocorrencias()
    if ocorrencias is None:
        return

    # Modo "w" substitui o resumo anterior, então gerar de novo não duplica
    with open(ARQ_PASSAGEM, "w", encoding="utf-8") as arquivo:
        arquivo.write(montar_texto_passagem(filtrar_abertas(ocorrencias)))

    with open(ARQ_PASSAGEM, "r", encoding="utf-8") as arquivo:
        print("\n" + arquivo.read())


def exibir_menu():
    print("\n===== " + NOME_SISTEMA + " =====")
    print("1 - Registrar ocorrência")
    print("2 - Consultar ocorrências")
    print("3 - Registrar anotação no diário")
    print("4 - Consultar diário")
    print("5 - Gerar passagem de plantão")
    print("6 - Sair")


def main():
    acoes = {
        "1": registrar_ocorrencia,
        "2": consultar_ocorrencias,
        "3": registrar_anotacao,
        "4": consultar_diario,
        "5": gerar_passagem
    }

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "6":
            print("Encerrando. Bom plantão!")
            break
        if opcao in acoes:
            acoes[opcao]()
        else:
            print("Opção inválida. Escolha um número de 1 a 6.")


main()
