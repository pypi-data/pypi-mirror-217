# Pacote Cliente

Classe que representa a entidade Cliente de um sistema bancário. O Cliente contém os atributos:
- Nome: Nome do cliente
- Idade: Idade do cliente em anos
- Data de nascimento: Data em que o cliente nasceu
- id: Identificador único do cliente
- Children: Quantidade de crianças/ filhos que o cliente possui
- Dias trabalhados: Quantidade de dias trabalhados que o cliente possui
- Education: Nível de escolaridade do cliente
- Education id: Identificador único do atributo "Education"
- Status familiar: Classe que representa o status civil do cliente
- Status familiar id: Identificador único do atributo "Status familiar id"
- Gênero (Masculino, Feminino ou XMA)
- Tipo de trabalho: CLT, PJ, etc...
- dívida: Se o cliente apresenta ou não algum tipo de dívida
- Renda mensal total
- purpose: Propósito em que o cliente apresenta o desejo em alcançar uma linha de crédito
- Repositório de contas do cliente

## Uso:

Criação de um objeto:

    cliente = Cliente("João", 30, "01/01/1990", 2, 1000, 30, "Ensino Médio", 1, "Casado", 1, "Masculino","Assalariado", False, 5000, "Comprar uma casa")

Adicionando uma conta:

    conta = Conta(saldo=1000, limite_saques=3)
    cliente.adicionar_conta(conta)

Listar as contas do cliente:

    contas = cliente.listar_contas()
    for conta in contas:
        print(conta.saldo)
        print(conta.limite_saques)

Removendo a conta do cliente:

    # Altere "conta_id" pelo identificador único da conta
    cliente.remover_conta(conta_id)

