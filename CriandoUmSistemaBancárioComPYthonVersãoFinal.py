def exibir_menu():
    print("""
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
""")


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("✅ Depósito realizado com sucesso.")
    else:
        print("❌ Operação falhou! Valor inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, numero_saques, LIMITE_SAQUES, LIMITE_VALOR):
    if numero_saques >= LIMITE_SAQUES:
        print("❌ Limite diário de saques excedido.")
    elif valor > saldo:
        print("❌ Saldo insuficiente.")
    elif valor > LIMITE_VALOR:
        print(f"❌ O valor excede o limite permitido de R$ {LIMITE_VALOR:.2f}.")
    elif valor <= 0:
        print("❌ Valor inválido.")
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print("✅ Saque realizado com sucesso.")
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, extrato):
    print("\n🧾 === EXTRATO ===")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for operacao in extrato:
            print(operacao)
    print(f"\n💰 Saldo atual: R$ {saldo:.2f}")
    print("===================")

def criar_usuario(lista_usuarios):
    nome = input("Informe o nome do usuário: ")
    cpf = input("Informe o CPF do usuário: ")
    if filtrar_usuarios_por_cpf(cpf, lista_usuarios):
        print("Usuário já cadastrado com este CPF.")
        return None
    else:
        usuario = {"nome": nome, "cpf": cpf, "contas": []}
        lista_usuarios.append(usuario)
        print("Usuário criado com sucesso!")
        return usuario

def filtrar_usuarios_por_cpf(cpf, lista_usuarios):
    for usuario in lista_usuarios:
        if usuario.get("cpf") == cpf:
            return usuario
    return None

def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    usuario = filtrar_usuarios_por_cpf(cpf, usuarios)
    if usuario:
        agencia = input("Informe a agência da conta: ")
        numero_conta = input("Informe o número da conta: ")
        conta_nova = {"agencia": agencia, "numero_conta": numero_conta, "saldo": 0.0}
        usuario_vinculado = vincular_usuario(cpf, usuarios, conta_nova)
        if usuario_vinculado:
            contas.append(conta_nova)
            print("Conta criada e vinculada ao usuário com sucesso!")
        else:
            print("Erro ao vincular a conta ao usuário.")
    else:
        print("Usuário não encontrado.")

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Saldo: R$ {conta['saldo']:.2f}")

def vincular_usuario(cpf_busca, lista_usuarios, conta_nova):
    """
    Vincula uma conta a um usuário cujo CPF corresponde ao informado.

    Parâmetros:
    - cpf_busca: str -> CPF que está sendo procurado
    - lista_usuarios: list[dict] -> Lista com os usuários cadastrados
    - conta_nova: dict -> Conta que será vinculada ao usuário

    Retorna:
    - dict -> Usuário atualizado com a nova conta, ou None se não encontrado
    """
    for usuario in lista_usuarios:
        if usuario.get("cpf") == cpf_busca:
            if "contas" not in usuario:
                usuario["contas"] = []
            usuario["contas"].append(conta_nova)
            return usuario
    return None

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    LIMITE_VALOR = 500.00

    saldo = 0
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        print("\n=== MENU ===")
        print("[d] Depositar")
        print("[s] Sacar")
        print("[e] Extrato")
        print("[1] Criar Usuário")
        print("[2] Criar Conta")
        print("[3] Listar Contas")
        print("[q] Sair")

        opcao = input("Escolha uma opção: ").lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: R$ "))
            saldo, extrato, numero_saques = sacar(
                valor=valor,
                saldo=saldo,
                extrato=extrato,
                numero_saques=numero_saques,
                LIMITE_SAQUES=LIMITE_SAQUES,
                LIMITE_VALOR=LIMITE_VALOR
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "1":
            criar_usuario(usuarios)

        elif opcao == "2":
            criar_conta(AGENCIA, len(contas) + 1, usuarios, contas)

        elif opcao == "3":
            listar_contas(contas)

        elif opcao == "q":
            print("👋 Sessão encerrada. Obrigado por usar o Banco DIO Jefferson Edition!")
            break

        else:
            print("⚠️ Opção inválida. Tente novamente.")

main()