from InquirerPy import inquirer

numeros_quartos = []
status_quartos = []
hospedes_quartos = []
dias_estadia = []
opcao_menu = ""

def inicializar_hotel():
    global numeros_quartos, status_quartos, hospedes_quartos, dias_estadia
    numeros_quartos = list(range(101, 151))
    status_quartos = ["Livre"] * 50
    hospedes_quartos = [""] * 50
    dias_estadia = [0] * 50

def encontrar_indice_quarto(num_quarto, numeros_quartos):
    try:
        return numeros_quartos.index(num_quarto)
    except ValueError:
        return -1

def fazer_check_in(num_quarto, nome_hospede, num_dias, numeros_quartos, status_quartos, hospedes_quartos, dias_estadia):
    indice = encontrar_indice_quarto(num_quarto, numeros_quartos)
    
    if indice == -1:
        print("Número de quarto inválido ou não localizado. Verifique e tente novamente.")
        return 
    elif status_quartos[indice] in ["Ocupado", "Limpeza", "Manutenção"]:
        print(f"O quarto selecionado não está disponível (Status: {status_quartos[indice]}).")
        return
    else:
        hospedes_quartos[indice] = nome_hospede
        dias_estadia[indice] = num_dias
        status_quartos[indice] = "Ocupado"
        print("Check-in efetuado com sucesso.")

def fazer_check_out(num_quarto, numeros_quartos, status_quartos, hospedes_quartos, dias_estadia):
    indice = encontrar_indice_quarto(num_quarto, numeros_quartos)
    
    if indice == -1:
        print("Número de quarto inválido ou não localizado. Verifique e tente novamente.")
        return
    elif status_quartos[indice] == "Ocupado":
        hospedes_quartos[indice] = ""
        dias_estadia[indice] = 0
        status_quartos[indice] = "Limpeza"
        print("Check-out efetuado com sucesso.")
    else:
        print("Operação não permitida. O quarto não se encontra ocupado.")
        return

def limpeza_quarto(num_quarto, numeros_quartos, status_quartos):
    indice = encontrar_indice_quarto(num_quarto, numeros_quartos)
    
    if indice == -1:
        print("Número de quarto inválido ou não localizado. Verifique e tente novamente.")
        return
    elif status_quartos[indice] in ["Limpeza", "Manutenção"]:
        status_quartos[indice] = "Livre"
        print("O status do quarto foi atualizado para 'Livre'.")
    else:
        print(f"Operação não permitida. O quarto (Status: {status_quartos[indice]}) não requer limpeza no momento.")
        return

def vizualizar_ocupacao_especifica(num_quarto, hospedes_quartos, numeros_quartos, status_quartos, dias_estadia):
    indice = encontrar_indice_quarto(num_quarto, numeros_quartos)
    
    if indice == -1:
        print("Número de quarto inválido ou não localizado. Verifique e tente novamente.")
        return
    elif status_quartos[indice] == "Ocupado":
        print(f"Quarto {num_quarto} | Status: {status_quartos[indice]} | Hóspede: {hospedes_quartos[indice]} | Estadia: {dias_estadia[indice]} dias")
    else:
        print(f"Quarto {num_quarto} | Status: {status_quartos[indice]}")

def vizualizar_ocupacoes(hospedes_quartos, numeros_quartos, status_quartos, dias_estadia):
    print("\n--- Relatório de Ocupação Geral ---")
    for i in range(50):
        if status_quartos[i] == "Ocupado":
            print(f"Quarto {numeros_quartos[i]} | Status: {status_quartos[i]} | Hóspede: {hospedes_quartos[i]} | Estadia: {dias_estadia[i]} dias")
        else:
            print(f"Quarto {numeros_quartos[i]} | Status: {status_quartos[i]}")
    print("--- Fim do Relatório ---")


def menu():
    global opcao_menu
    
    try:
        opcao_menu = inquirer.select(
            message="\n=== HOTEL MANAGER PRO ===\nSelecione uma operação:",
            choices=[
                "Fazer Check-in",
                "Fazer Check-out",
                "Marcar quarto como limpo",
                "Visualizar Ocupação Geral",
                "Consultar Quarto Específico",
                "Sair"
            ]
        ).execute()
        
        if opcao_menu == "Visualizar Ocupação Geral":
            vizualizar_ocupacoes(hospedes_quartos, numeros_quartos, status_quartos, dias_estadia)
        
        elif opcao_menu == "Consultar Quarto Específico":
            try:
                num_quarto = int(input("Informe o número do quarto: "))
                vizualizar_ocupacao_especifica(num_quarto, hospedes_quartos, numeros_quartos, status_quartos, dias_estadia)
            except ValueError:
                print("Entrada inválida. É necessário inserir um valor numérico.")
        
        elif opcao_menu == "Fazer Check-in":
            try:
                num_quarto = int(input("Informe o número do quarto: "))
                nome_hospede = input("Informe o nome do hóspede: ")
                num_dias = int(input("Informe o número de dias da estadia: "))
                fazer_check_in(num_quarto, nome_hospede, num_dias, numeros_quartos, status_quartos, hospedes_quartos, dias_estadia)
            except ValueError:
                print("Entrada inválida. O número do quarto e os dias de estadia devem ser valores numéricos.")
        
        elif opcao_menu == "Fazer Check-out":
            try:
                num_quarto = int(input("Informe o número do quarto: "))
                fazer_check_out(num_quarto, numeros_quartos, status_quartos, hospedes_quartos, dias_estadia)
            except ValueError:
                print("Entrada inválida. É necessário inserir um valor numérico.")
        
        elif opcao_menu == "Marcar quarto como limpo":
            try:
                num_quarto = int(input("Informe o número do quarto: "))
                limpeza_quarto(num_quarto, numeros_quartos, status_quartos)
            except ValueError:
                print("Entrada inválida. É necessário inserir um valor numérico.")
                
        else:
            print("Encerrando o sistema...")
            
    except KeyboardInterrupt:
        print("\nEncerrando o sistema...")
        opcao_menu = "Sair"
        
    return opcao_menu

inicializar_hotel()
menu()

while opcao_menu != "Sair":
    menu()