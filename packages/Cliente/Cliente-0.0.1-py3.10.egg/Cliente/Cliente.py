from datetime import datetime as dt

class Cliente:
    contador_id = 0

    """Classe Cliente
    Description: Classe que representa um cliente do banco
    Atributos:
        1. nome: Nome do cliente
        2. idade: Idade do cliente
        3. data_nascimento: Data de nascimento do cliente (no formato "dd/mm/aaaa")
        4. id: Identificador único do cliente
        5. children: Número de crianças na família
        6. days_employed: Experiência de trabalho em dias
        7. dob_years: Idade do cliente em anos
        8. education: Educação do cliente
        9. education_id: Identificador de educação
        10. family_status: Estado civil do cliente
        11. family_status_id: Identificador de estado civil
        12. gender: Gênero do cliente
        13. income_type: Tipo de emprego
        14. debt: Indica se o cliente tinha alguma dívida no pagamento do empréstimo
        15. total_income: Renda mensal
        16. purpose: O objetivo de obter um empréstimo
        17. contas: Lista de contas associadas ao cliente
    """

    def __init__(self, nome, idade, data_nascimento, children, days_employed, dob_years, education, education_id,
                 family_status, family_status_id, gender, income_type, debt, total_income, purpose):
        self.nome = nome
        self.idade = idade
        self.data_nascimento = dt.strptime(data_nascimento, "%d/%m/%Y").date()
        self.id = Cliente.contador_id
        Cliente.contador_id += 1
        self.children = children
        self.days_employed = days_employed
        self.dob_years = dob_years
        self.education = education
        self.education_id = education_id
        self.family_status = family_status
        self.family_status_id = family_status_id
        self.gender = gender
        self.income_type = income_type
        self.debt = debt
        self.total_income = total_income
        self.purpose = purpose
        self.contas = []

    def adicionar_conta(self, conta):
        """Adiciona uma nova conta à lista de contas do cliente"""
        self.contas.append(conta)

    def listar_contas(self):
        """Retorna a lista de contas do cliente"""
        return self.contas

    def remover_conta(self, conta_id):
        """Remove uma conta da lista de contas do cliente pelo ID da conta"""
        for conta in self.contas:
            if conta.id == conta_id:
                self.contas.remove(conta)
                print(f"Conta {conta_id} removida com sucesso!")
                return

        print(f"Conta {conta_id} não encontrada!")
