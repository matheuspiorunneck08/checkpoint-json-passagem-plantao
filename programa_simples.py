# Passagem de plantão - versão simplificada para estudo
# Sistema: AgendaFácil (agendamento de consultas)

import json

sistema = "AgendaFácil"


def ler_ocorrencias():
    try:
        with open("ocorrencias.json", "r", encoding="utf-8") as arq:
            lista = json.load(arq)
        return lista
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("O arquivo ocorrencias.json está com erro.")
        print("Corrija o arquivo para voltar a usar as opções 1, 2 e 5.")
        return None


def salvar_ocorrencias(lista):
    with open("ocorrencias.json", "w", encoding="utf-8") as arq:
        json.dump(lista, arq, ensure_ascii=False, indent=4)


def cadastrar():
    lista = ler_ocorrencias()
    if lista == None:
        return

    servico = input("Serviço: ")
    descricao = input("Descrição: ")

    prioridade = input("Prioridade (alta, media, baixa): ")
    while prioridade != "alta" and prioridade != "media" and prioridade != "baixa":
        print("Prioridade inválida!")
        prioridade = input("Prioridade (alta, media, baixa): ")

    status = input("Status (aberto, resolvido): ")
    while status != "aberto" and status != "resolvido":
        print("Status inválido!")
        status = input("Status (aberto, resolvido): ")

    if status == "resolvido":
        proxima_acao = "nenhuma"
    else:
        proxima_acao = input("Próxima ação: ")

    ocorrencia = {
        "servico": servico,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": status,
        "proxima_acao": proxima_acao
    }
    lista.append(ocorrencia)
    salvar_ocorrencias(lista)
    print("Ocorrência salva!")


def consultar():
    lista = ler_ocorrencias()
    if lista == None:
        return
    if len(lista) == 0:
        print("Não há ocorrências.")
        return
    for oc in lista:
        print("-----")
        print("Serviço:", oc["servico"])
        print("Descrição:", oc["descricao"])
        print("Prioridade:", oc["prioridade"])
        print("Status:", oc["status"])
        print("Próxima ação:", oc["proxima_acao"])


def anotar_diario():
    servico = input("Serviço: ")
    anotacao = input("Anotação: ")
    with open("diario.txt", "a", encoding="utf-8") as arq:
        arq.write(servico + " — " + anotacao + "\n")
    print("Anotação salva!")


def ver_diario():
    try:
        with open("diario.txt", "r", encoding="utf-8") as arq:
            print(arq.read())
    except FileNotFoundError:
        print("Nenhuma anotação registrada")


def gerar_passagem():
    lista = ler_ocorrencias()
    if lista == None:
        return

    abertas = 0
    altas = 0
    for oc in lista:
        if oc["status"] == "aberto":
            abertas = abertas + 1
            if oc["prioridade"] == "alta":
                altas = altas + 1

    with open("passagem.txt", "w", encoding="utf-8") as arq:
        arq.write("Passagem de plantão - " + sistema + "\n")
        arq.write("Ocorrências abertas: " + str(abertas) + "\n")
        arq.write("Abertas com prioridade alta: " + str(altas) + "\n\n")
        if abertas == 0:
            arq.write("Nenhuma pendência para o próximo plantão\n")
        for oc in lista:
            if oc["status"] == "aberto":
                arq.write("Serviço: " + oc["servico"] + "\n")
                arq.write("Descrição: " + oc["descricao"] + "\n")
                arq.write("Prioridade: " + oc["prioridade"] + "\n")
                arq.write("Próxima ação: " + oc["proxima_acao"] + "\n\n")

    with open("passagem.txt", "r", encoding="utf-8") as arq:
        print(arq.read())


opcao = ""
while opcao != "6":
    print("\n1 - Registrar ocorrência")
    print("2 - Consultar ocorrências")
    print("3 - Registrar anotação no diário")
    print("4 - Consultar diário")
    print("5 - Gerar passagem de plantão")
    print("6 - Sair")
    opcao = input("Opção: ")

    if opcao == "1":
        cadastrar()
    elif opcao == "2":
        consultar()
    elif opcao == "3":
        anotar_diario()
    elif opcao == "4":
        ver_diario()
    elif opcao == "5":
        gerar_passagem()
    elif opcao == "6":
        print("Saindo...")
    else:
        print("Opção inválida!")
