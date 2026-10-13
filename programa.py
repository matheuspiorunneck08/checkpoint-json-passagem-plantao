# Checkpoint de arquivos e JSON - Passagem de plantão
# Solução de referência para estudo
# Contexto: AgendaFácil, sistema de agendamento de consultas de uma clínica

import json

NOME_SISTEMA = "AgendaFácil - Agendamento de Consultas"
ARQ_OCORRENCIAS = "ocorrencias.json"
ARQ_DIARIO = "diario.txt"
ARQ_PASSAGEM = "passagem.txt"


# ---------- Leitura e gravação do JSON ----------

def carregar_ocorrencias():
    # Retorna a lista salva, [] se o arquivo não existir
    # ou None se o JSON estiver inválido (bloqueia as opções que dependem dele)
    try:
        with open(ARQ_OCORRENCIAS, "r", encoding="utf-8") as arquivo:
            lista = json.load(arquivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("\nERRO: o arquivo", ARQ_OCORRENCIAS, "está com conteúdo inválido.")
        print("Corrija o arquivo (ele deve conter uma lista JSON, por exemplo [])")
        print("ou restaure uma cópia válida. Cadastro, consulta de ocorrências e")
        print("geração do resumo ficam suspensos até a correção.")
        print("O arquivo não foi alterado.")
        return None

    if type(lista) != list:
        print("\nERRO: o arquivo", ARQ_OCORRENCIAS, "não contém uma lista de ocorrências.")
        print("Corrija o arquivo antes de cadastrar, consultar ou gerar o resumo.")
        return None
    return lista


def salvar_ocorrencias(lista):
    with open(ARQ_OCORRENCIAS, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, ensure_ascii=False, indent=4)


# ---------- Entradas com validação ----------

def pedir_texto(mensagem):
    texto = input(mensagem).strip()
    while texto == "":
        print("Campo obrigatório. Digite um valor.")
        texto = input(mensagem).strip()
    return texto


def pedir_opcao(mensagem, opcoes):
    valor = input(mensagem).strip().lower()
    if valor == "média":
        valor = "media"
    while valor not in opcoes:
        print("Valor inválido. Opções aceitas:", ", ".join(opcoes))
        valor = input(mensagem).strip().lower()
        if valor == "média":
            valor = "media"
    return valor


# ---------- Ocorrências ----------

def registrar_ocorrencia():
    # Carrega antes de incluir para não perder os registros anteriores
    lista = carregar_ocorrencias()
    if lista is None:
        return

    print("\n--- Nova ocorrência ---")
    servico = pedir_texto("Serviço afetado: ")
    descricao = pedir_texto("Descrição: ")
    prioridade = pedir_opcao("Prioridade (alta/media/baixa): ", ["alta", "media", "baixa"])
    status = pedir_opcao("Status (aberto/resolvido): ", ["aberto", "resolvido"])

    if status == "resolvido":
        proxima_acao = "nenhuma"
    else:
        proxima_acao = pedir_texto("Próxima ação: ")

    ocorrencia = {
        "servico": servico,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": status,
        "proxima_acao": proxima_acao
    }

    lista.append(ocorrencia)
    salvar_ocorrencias(lista)
    print("Ocorrência registrada. Total salvo:", len(lista))


def consultar_ocorrencias():
    lista = carregar_ocorrencias()
    if lista is None:
        return

    if len(lista) == 0:
        print("\nNão há ocorrências registradas.")
        return

    print("\n--- Ocorrências ---")
    numero = 1
    for ocorrencia in lista:
        print(f"\n#{numero}")
        print("Serviço:", ocorrencia["servico"])
        print("Descrição:", ocorrencia["descricao"])
        print("Prioridade:", ocorrencia["prioridade"])
        print("Status:", ocorrencia["status"])
        print("Próxima ação:", ocorrencia["proxima_acao"])
        numero = numero + 1


# ---------- Diário ----------

def registrar_anotacao():
    print("\n--- Nova anotação ---")
    servico = pedir_texto("Serviço: ")
    anotacao = pedir_texto("Anotação: ")

    # Modo "a" acrescenta no fim sem apagar o histórico
    with open(ARQ_DIARIO, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{servico} — {anotacao}\n")
    print("Anotação registrada no diário.")


def consultar_diario():
    try:
        with open(ARQ_DIARIO, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        print("\nNenhuma anotação registrada.")
        return

    if conteudo.strip() == "":
        print("\nNenhuma anotação registrada.")
    else:
        print("\n--- Diário ---")
        print(conteudo)


# ---------- Passagem de plantão ----------

def gerar_passagem():
    lista = carregar_ocorrencias()
    if lista is None:
        return

    abertas = []
    abertas_alta = 0
    for ocorrencia in lista:
        if ocorrencia["status"] == "aberto":
            abertas.append(ocorrencia)
            if ocorrencia["prioridade"] == "alta":
                abertas_alta = abertas_alta + 1

    texto = "PASSAGEM DE PLANTÃO\n"
    texto = texto + f"Sistema: {NOME_SISTEMA}\n"
    texto = texto + f"Ocorrências abertas: {len(abertas)}\n"
    texto = texto + f"Abertas com prioridade alta: {abertas_alta}\n\n"

    if len(abertas) == 0:
        texto = texto + "Nenhuma pendência para o próximo plantão\n"
    else:
        texto = texto + "Pendências:\n"
        numero = 1
        for ocorrencia in abertas:
            texto = texto + f"\n{numero}. Serviço: {ocorrencia['servico']}\n"
            texto = texto + f"   Descrição: {ocorrencia['descricao']}\n"
            texto = texto + f"   Prioridade: {ocorrencia['prioridade']}\n"
            texto = texto + f"   Próxima ação: {ocorrencia['proxima_acao']}\n"
            numero = numero + 1

    # Modo "w" substitui o resumo anterior a cada geração
    with open(ARQ_PASSAGEM, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)

    with open(ARQ_PASSAGEM, "r", encoding="utf-8") as arquivo:
        print("\n" + arquivo.read())


# ---------- Menu ----------

def menu():
    while True:
        print("\n===== " + NOME_SISTEMA + " =====")
        print("1 - Registrar ocorrência")
        print("2 - Consultar ocorrências")
        print("3 - Registrar anotação no diário")
        print("4 - Consultar diário")
        print("5 - Gerar passagem de plantão")
        print("6 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            registrar_ocorrencia()
        elif opcao == "2":
            consultar_ocorrencias()
        elif opcao == "3":
            registrar_anotacao()
        elif opcao == "4":
            consultar_diario()
        elif opcao == "5":
            gerar_passagem()
        elif opcao == "6":
            print("Encerrando. Bom plantão!")
            break
        else:
            print("Opção inválida. Escolha um número de 1 a 6.")


menu()
