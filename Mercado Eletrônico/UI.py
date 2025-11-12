from view import View

class UI:
    __usuario = None

    

    @staticmethod
    def menu_visitante():
        print("\n=== MENU VISITANTE ===")
        print("1 - Entrar no sistema")
        print("2 - Abrir conta")
        print("3 - Fim")
        try:
            return int(input("O que deseja acessar? "))
        except ValueError:
            print("Entrada inválida.")
            return 0

    @staticmethod
    def menu_admin():
        print("\n=== MENU ADMINISTRADOR ===")
        print("1 - Produto")
        print("2 - Categoria")
        print("3 - Cliente")
        print("4 - Fim")
        try:
            return int(input("O que deseja acessar? "))
        except ValueError:
            print("Entrada inválida.")
            return 0

    @staticmethod
    def menu_cliente():
        print("\n=== MENU CLIENTE ===")
        print("1 - Listar produtos")
        print("2 - Inserir produto no carrinho")
        print("3 - Visualizar carrinho")
        print("4 - Comprar o carrinho")
        print("5 - Listar minhas compras")
        print("6 - Fim")
        try:
            return int(input("O que deseja acessar? "))
        except ValueError:
            print("Entrada inválida.")
            return 0

    

    @classmethod
    def main(cls):
        View.cliente_criar_admin()
        op = 0

        
        while op != 3 and cls.__usuario is None:
            op = UI.menu_visitante()
            if op == 1:
                UI.visitante_entrar()
            elif op == 2:
                UI.visitante_criar_conta()

        
        if cls.__usuario and cls.__usuario.get_email() == "admin":
            op = 0
            while op != 4:
                op = UI.menu_admin()
                if op == 1:
                    print("\n1 - Inserir | 2 - Listar | 3 - Atualizar | 4 - Excluir | 5 - Reajustar preço")
                    p = int(input("Qual operação deseja realizar? "))
                    if p == 1: UI.Produto_inserir()
                    elif p == 2: UI.Produto_listar()
                    elif p == 3: UI.Produto_atualizar()
                    elif p == 4: UI.Produto_excluir()
                    elif p == 5: UI.Produto_reajustar()

                elif op == 2:
                    print("\n1 - Inserir | 2 - Listar | 3 - Atualizar | 4 - Excluir")
                    p = int(input("Qual operação deseja realizar? "))
                    if p == 1: UI.Categoria_inserir()
                    elif p == 2: UI.Categoria_listar()
                    elif p == 3: UI.Categoria_atualizar()
                    elif p == 4: UI.Categoria_excluir()

                elif op == 3:
                    print("\n1 - Inserir | 2 - Listar | 3 - Atualizar | 4 - Excluir | 5 - Listar vendas 6 - Lucro")
                    p = int(input("Qual operação deseja realizar? "))
                    if p == 1: UI.Cliente_inserir()
                    elif p == 2: UI.Cliente_listar()
                    elif p == 3: UI.Cliente_atualizar()
                    elif p == 4: UI.Cliente_excluir()
                    elif p == 5: UI.cliente_listar_vendas()
                    elif p == 6: UI.lucro()

        
        elif cls.__usuario and cls.__usuario.get_email() != "admin":
            op = 0
            while op != 6:
                op = UI.menu_cliente()
                if op == 1:
                    UI.Produto_listar()
                elif op == 2:
                    UI.Carrinho_inserir()
                elif op == 3:
                    UI.carrinho_listar()
                elif op == 4:
                    confirmacao = input("Deseja finalizar a compra? (S/N): ").upper()
                    if confirmacao == "S":
                        View.carrinho_comprar(cls.__usuario.get_id())
                        print("Compra finalizada!")
                    else:
                        print("Compra cancelada.")
                elif op == 5:
                    UI.cliente_listar_compra()

    

    @classmethod
    def visitante_entrar(cls):
        email = input("Informe o e-mail: ")
        senha = input("Informe a senha: ")
        cls.__usuario = View.cliente_autenticar(email, senha)
        if cls.__usuario is None:
            print("Usuário ou senha inválidos.")
        else:
            print(f"Bem-vindo(a), {cls.__usuario.get_nome()}!")

    @classmethod
    def visitante_criar_conta(cls):
        nome = input("Informe o seu nome: ")
        email = input("Informe o e-mail: ")
        fone = input("Informe o telefone: ")
        senha = input("Crie uma senha: ")
        cls.__usuario = View.cliente_criar_conta(nome, email, fone, senha)
        print("Conta criada com sucesso!")

    

    @staticmethod
    def Cliente_inserir():
        nome = input("Nome do cliente: ")
        email = input("E-mail do cliente: ")
        fone = input("Telefone: ")
        senha = input("Senha: ")
        View.cliente_inserir(nome, email, fone, senha)

    @staticmethod
    def Cliente_listar():
        for obj in View.cliente_listar():
            print(obj)

    @staticmethod
    def Cliente_atualizar():
        UI.Cliente_listar()
        id = int(input("Informe o ID a ser atualizado: "))
        nome = input("Novo nome: ")
        email = input("Novo e-mail: ")
        fone = input("Novo telefone: ")
        View.cliente_atualizar(id, nome, email, fone)

    @staticmethod
    def Cliente_excluir():
        UI.Cliente_listar()
        id = int(input("Informe o ID a ser excluído: "))
        View.cliente_excluir(id, "", "", "")

    @classmethod
    def cliente_listar_compra(cls):
        View.cliente_listar_compras(cls.__usuario.get_id())

    @classmethod
    def cliente_listar_vendas(cls):
        View.cliente_listar_vendas()  

    @classmethod
    def lucro(cls):
        View.lucro()


    @staticmethod
    def Produto_inserir():
        desc = input("Descrição do produto: ")
        preco = float(input("Preço: "))
        estoque = int(input("Quantidade em estoque: "))
        idcategoria = int(input("ID da categoria: "))
        View.produto_inserir(desc, preco, estoque, idcategoria)

    @staticmethod
    def Produto_listar():
        for obj in View.produto_listar():
            print(obj)

    @staticmethod
    def Produto_atualizar():
        UI.Produto_listar()
        id = int(input("ID do produto a ser atualizado: "))
        desc = input("Nova descrição: ")
        preco = float(input("Novo preço: "))
        estoque = int(input("Novo estoque: "))
        idcat = int(input("ID da categoria: "))
        View.produto_atualizar(id, desc, preco, estoque, idcat)

    @staticmethod
    def Produto_excluir():
        UI.Produto_listar()
        id = int(input("ID do produto a ser excluído: "))
        View.produto_excluir(id)

    @staticmethod
    def Produto_reajustar():
        percentual = float(input("Percentual de reajuste (%): "))
        View.produto_reajustar(percentual)

   

    @staticmethod
    def Categoria_inserir():
        desc = input("Descrição da categoria: ")
        View.categoria_inserir(0, desc)

    @staticmethod
    def Categoria_listar():
        for obj in View.categoria_listar():
            print(obj)

    @staticmethod
    def Categoria_atualizar():
        UI.Categoria_listar()
        id = int(input("ID da categoria a ser atualizada: "))
        desc = input("Nova descrição: ")
        View.categoria_atualizar(id, desc)

    @staticmethod
    def Categoria_excluir():
        UI.Categoria_listar()
        id = int(input("ID da categoria a ser excluída: "))
        View.categoria_excluir(id)

    

    @staticmethod
    def Carrinho_inserir():
        UI.Produto_listar()
        id = int(input("ID do produto que deseja adicionar: "))
        qtd = int(input("Quantidade: "))
        View.carrinho_inserir(id, qtd)

    @staticmethod
    def carrinho_listar():
        for obj in View.carrinho_listar_detalhado():
            print(obj)

    @staticmethod
    def carrinho_preco():
        View.carrinho_preco()

    @classmethod
    def carrinho_comprar(cls):
        carrinho = View.carrinho_listar_detalhado()
        if not carrinho:
            print("Carrinho vazio.")
            return
        print("Itens no carrinho:")
        for item in carrinho:
            print(item)
        total = View.carrinho_preco()
        print(f"Total: R${total:.2f}")
        confirmacao = input("Deseja finalizar a compra? (S/N): ").upper()
        if confirmacao == "S":
            View.carrinho_comprar(cls.__usuario.get_id())
            print("Compra realizada com sucesso!")
        else:
            print("Compra cancelada.")

UI.main()