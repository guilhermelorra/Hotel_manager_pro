try:
    from InquirerPy import inquirer
    USE_INQUIRER = True
except Exception:
    inquirer = None
    USE_INQUIRER = False

import os

opcao_menu = ""

def inicializar_hotel():
    numeros_quartos = list(range(101, 151))
    status_quartos = ["Livre"] * 50
    hospedes_quartos = [""] * 50
    dias_estadia = [0] * 50
    return numeros_quartos, status_quartos, hospedes_quartos, dias_estadia

def encontrar_indice_quarto(num_quarto, numeros_quartos):
    try:
        return numeros_quartos.index(num_quarto)
    except ValueError:
        return -1

def fazer_check_in(num_quarto, nome_hospede, num_dias, numeros_quartos, status_quartos, hospedes_quartos, dias_estadia):
    indice = encontrar_indice_quarto(num_quarto, numeros_quartos)
    if indice == -1:
        print("Número de quarto inválido ou não localizado. Verifique e tente novamente.")
        return False
    if status_quartos[indice] in ["Ocupado", "Limpeza", "Manutenção"]:
        print(f"O quarto selecionado não está disponível (Status: {status_quartos[indice]}).")
        return False
    hospedes_quartos[indice] = nome_hospede
    dias_estadia[indice] = num_dias
    status_quartos[indice] = "Ocupado"
    print("Check-in efetuado com sucesso.")
    return True

def fazer_check_out(num_quarto, numeros_quartos, status_quartos, hospedes_quartos, dias_estadia):
    indice = encontrar_indice_quarto(num_quarto, numeros_quartos)
    if indice == -1:
        print("Número de quarto inválido ou não localizado. Verifique e tente novamente.")
        return None
    if status_quartos[indice] != "Ocupado":
        print("Operação não permitida. O quarto não se encontra ocupado.")
        return None
    nome_hospede = hospedes_quartos[indice]
    hospedes_quartos[indice] = ""
    dias_estadia[indice] = 0
    status_quartos[indice] = "Limpeza"
    print("Check-out efetuado com sucesso.")
    return nome_hospede

def marcar_quarto_limpo(num_quarto, numeros_quartos, status_quartos):
    indice = encontrar_indice_quarto(num_quarto, numeros_quartos)
    if indice == -1:
        print("Número de quarto inválido ou não localizado. Verifique e tente novamente.")
        return False
    if status_quartos[indice] in ["Limpeza", "Manutenção"]:
        status_quartos[indice] = "Livre"
        print("O status do quarto foi atualizado para 'Livre'.")
        return True
    print(f"Operação não permitida. O quarto (Status: {status_quartos[indice]}) não requer limpeza no momento.")
    return False

def colocar_em_manutencao(num_quarto, numeros_quartos, status_quartos):
    indice = encontrar_indice_quarto(num_quarto, numeros_quartos)
    if indice == -1:
        print("Número de quarto inválido ou não localizado. Verifique e tente novamente.")
        return False
    if status_quartos[indice] == "Ocupado":
        print("Não é possível colocar um quarto ocupado em manutenção. Faça check-out primeiro.")
        return False
    status_quartos[indice] = "Manutenção"
    print(f"Quarto {num_quarto} marcado como 'Manutenção'.")
    return True

def encontrar_quartos_por_status(status, numeros_quartos, status_quartos):
    resultados = []
    for i, s in enumerate(status_quartos):
        if s == status:
            resultados.append(numeros_quartos[i])
    return resultados

def visualizar_ocupacao(hospedes_quartos, numeros_quartos, status_quartos, dias_estadia):
    print("\n--- Relatório de Ocupação Geral ---")
    for i in range(len(numeros_quartos)):
        if status_quartos[i] == "Ocupado":
            print(f"Quarto {numeros_quartos[i]} | Status: {status_quartos[i]} | Hóspede: {hospedes_quartos[i]} | Estadia: {dias_estadia[i]} dias")
        else:
            print(f"Quarto {numeros_quartos[i]} | Status: {status_quartos[i]}")
    print("--- Fim do Relatório ---")

def funcao_veficadora(mensagem, tipo, mensagem_error):
    while True:
        resposta = input(mensagem)
        try:
            resposta_formatada = tipo(resposta)
            return resposta_formatada
        except ValueError:
            print(mensagem_error)

def menu(numeros_quartos, status_quartos, hospedes_quartos, dias_estadia):
    global opcao_menu
    try:
        choices = [
            "Fazer Check-in",
            "Fazer Check-out",
            "Marcar quarto como limpo",
            "Colocar quarto em manutenção",
            "Relatórios por status",
            "Visualizar Ocupação Geral",
            "Consultar Quarto Específico",
            "Sair"
        ]

        if USE_INQUIRER:
            opcao_menu = inquirer.select(
                message="\n=== HOTEL MANAGER PRO ===\nSelecione uma operação:",
                choices=choices
            ).execute()
        else:
            print("\n=== HOTEL MANAGER PRO ===\nSelecione uma operação:")
            for i, c in enumerate(choices, 1):
                print(f"{i}. {c}")
            sel = funcao_veficadora("Escolha uma opção (número): ", int, "Digite um número válido.")
            if 1 <= sel <= len(choices):
                opcao_menu = choices[sel - 1]
            else:
                print("Opção inválida.")
                return opcao_menu

        if opcao_menu == "Visualizar Ocupação Geral":
            visualizar_ocupacao(hospedes_quartos, numeros_quartos, status_quartos, dias_estadia)

        elif opcao_menu == "Consultar Quarto Específico":
            try:
                num_quarto = int(input("Informe o número do quarto: "))
                indice = encontrar_indice_quarto(num_quarto, numeros_quartos)
                if indice == -1:
                    print("Número de quarto inválido.")
                elif status_quartos[indice] == "Ocupado":
                    print(f"Quarto {num_quarto} | Status: {status_quartos[indice]} | Hóspede: {hospedes_quartos[indice]} | Estadia: {dias_estadia[indice]} dias")
                else:
                    print(f"Quarto {num_quarto} | Status: {status_quartos[indice]}")
            except ValueError:
                print("Entrada inválida. É necessário inserir um valor numérico.")

        elif opcao_menu == "Fazer Check-in":
            try:
                num_quarto = int(input("Informe o número do quarto: "))
                nome_hospede = input("Informe o nome do hóspede: ")
                num_dias = int(input("Informe o número de dias da estadia: "))
                fazer_check_in(num_quarto, nome_hospede, num_dias, numeros_quartos, status_quartos, hospedes_quartos, dias_estadia)
            except ValueError:
                print("Entrada inválida. O número do quarto e dos dias de estadia devem ser valores numéricos.")

        elif opcao_menu == "Fazer Check-out":
            try:
                num_quarto = int(input("Informe o número do quarto: "))
                fazer_check_out(num_quarto, numeros_quartos, status_quartos, hospedes_quartos, dias_estadia)
            except ValueError:
                print("Entrada inválida. É necessário inserir um valor numérico")

        elif opcao_menu == "Marcar quarto como limpo":
            try:
                num_quarto = int(input("Informe o número do quarto: "))
                marcar_quarto_limpo(num_quarto, numeros_quartos, status_quartos)
            except ValueError:
                print("Entrada inválida. É necessário inserir um valor numérico.")

        elif opcao_menu == "Colocar quarto em manutenção":
            try:
                num_quarto = int(input("Informe o número do quarto: "))
                colocar_em_manutencao(num_quarto, numeros_quartos, status_quartos)
            except ValueError:
                print("Entrada inválida. É necessário inserir um valor numérico.")

        elif opcao_menu == "Relatórios por status":
            choices_status = ["Livre", "Ocupado", "Limpeza", "Manutenção"]
            if USE_INQUIRER:
                status_escolhido = inquirer.select(message="Escolha o status:", choices=choices_status).execute()
            else:
                print("Escolha o status:")
                for i, s in enumerate(choices_status, 1):
                    print(f"{i}. {s}")
                sel = funcao_veficadora("Escolha um número: ", int, "Digite um número válido.")
                if 1 <= sel <= len(choices_status):
                    status_escolhido = choices_status[sel - 1]
                else:
                    print("Opção inválida.")
                    return opcao_menu
            resultados = encontrar_quartos_por_status(status_escolhido, numeros_quartos, status_quartos)
            if resultados:
                print(f"Quartos com status '{status_escolhido}': {resultados}\n")
            else:
                print(f"Não há quartos com status '{status_escolhido}'.")

        else:
            print("Encerrando o sistema...")

    except KeyboardInterrupt:
        print("\nEncerrando o sistema...")
        opcao_menu = "Sair"

    return opcao_menu

if __name__ == "__main__":
    numeros_quartos, status_quartos, hospedes_quartos, dias_estadia = inicializar_hotel()
    menu(numeros_quartos, status_quartos, hospedes_quartos, dias_estadia)

    while opcao_menu != "Sair":
        menu(numeros_quartos, status_quartos, hospedes_quartos, dias_estadia)

    os.system("pause")