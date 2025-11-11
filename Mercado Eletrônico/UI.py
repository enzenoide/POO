from view import View

class UI:
    __usuario = None
    def menu_visitante():
        print("1. Entrar no sistema 2.Abrir conta")
        print("4- Fim")
        return int(input("Oque deseja acessar?"))
    def menu_admin():
        print("1. Produto 2.Categoria 3.Cliente, 4. Fim")
        return int(input("Oque deseja acessar?"))
    def menu_cliente():
        print("1. Listar produtos 2.Inserir produto no carrinho 3. Visualizar carrinho 4. Comprar o carrinho 5. Listar minhas compras 6. Fim ")
        return int(input("Oque deseja acessar?"))
    @classmethod
    def main(cls):
        View.cliente_criar_admin()
        op = 0
        while op != 4 and cls.__usuario == None:
            op = UI.menu_visitante()
            if op == 1:UI.visitante_entrar()
            if op == 2: UI.visitante_criar_conta()
        if cls.__usuario != None and cls.__usuario.get_email() == "admin":
            op = 0
            while op != 4:
                op = UI.menu_admin()
                if op == 1:
                    print("1-Inserir, 2-Listar, 3-Atualizar, 4-Excluir, 5- Reajustar preço")
                    p = int(input("Qual operação deseja realizar?"))
                    if p == 1: UI.Produto_inserir()
                    if p == 2: UI.Produto_listar()
                    if p == 3: UI.Produto_atualizar()
                    if p == 4: UI.Produto_excluir()
                    if p == 5: UI.Produto_reajustar()
                if op == 2:
                    print("1-Inserir, 2-Listar, 3-Atualizar, 4-Excluir")
                    p = int(input("Qual operação deseja realizar?"))
                    if p == 1: UI.Categoria_inserir()
                    if p == 2: UI.Categoria_listar()
                    if p == 3: UI.Categoria_atualizar()
                    if p == 4: UI.Categoria_excluir()
                if op == 3:
                    print("1-Inserir, 2-Listar, 3-Atualizar, 4-Excluir")
                    p = int(input("Qual operação deseja realizar?"))
                    if p == 1: UI.Cliente_inserir()
                    if p == 2: UI.Cliente_listar()
                    if p == 3: UI.Cliente_atualizar()
                    if p == 4: UI.Cliente_excluir()
        if cls.__usuario != None and cls.__usuario.get_email() != "admin":
            op = 0
            while op != 6:
                op = UI.menu_cliente()
                if op == 1: UI.Produto_listar()
                if op == 2: UI.Carrinho_inserir()
                if op == 3: UI.carrinho_listar()
                if op == 4: 
                    confirmacao = input("Deseja finalizar a compra? S/N").upper()
                    if confirmacao == "S":
                        View.carrinho_comprar(cls.__usuario.get_id())
                    else:
                        print("Compra cancelada")
                if op == 5: View.cliente_listar_compras(cls.__usuario.get_id())
            
    @classmethod
    def visitante_entrar(cls):
        email = input("Me informe o e-mail: ")
        senha = input("Me informe a senha: ")
        cls.__usuario = View.cliente_autenticar(email,senha)
        if cls.__usuario == None:
            print("Usuário ou senha inválidos")
    @classmethod
    def visitante_criar_conta(cls):
        email = input("Me informe o e-mail a ser criado: ")
        senha = input("Me informe a senha a ser criada: ")
        nome = input("Insira o seu nome: ")
        fone = input("Insira o seu telefone: ")
        cls.__usuario = View.cliente_criar_conta(nome,email,fone,senha)
    def Cliente_inserir():
        nome = input("Me informe o nome do cliente: ")
        email = input("Me informe o email do cliente: ")
        fone = input("Me infore o telefone do cliente: ")
        senha = input("Me informe a senha do cliente: ")
        View.cliente_inserir(nome,email,fone,senha)
    def Cliente_listar():
        for obj in View.cliente_listar(): print(obj)
    def Cliente_atualizar():
        UI.Cliente_listar
        id = int(input("Informe o id a ser atualizado: "))
        nome = input("Informe o novo nome: ")
        email = input("informe o novo email: ")
        fone = input("Informe o novo telefone: ")
        View.cliente_atualizar(id,nome,email,fone)
    def Cliente_excluir():
        UI.Cliente_listar()
        id = int(input("Informe o ID a ser excluido: "))
        nome = ""
        email = ""
        fone = ""
        View.cliente_excluir(id,nome,email,fone)
    @classmethod
    def cliente_listar_compra(cls):
        View.cliente_listar_compras(UI.__usuario.get_id())

    def Produto_inserir():
        desc = input("Me informe qual é o produto: ")
        preco = float(input("Me informe o preço do produto: "))
        estoque = int(input("Digite a quantidade em estoque: "))
        idcategoria = int(input("Digite o id da categoria do produto: "))
        View.produto_inserir(desc, preco, estoque, idcategoria)
    def Produto_listar(): 
        for obj in View.produto_listar():
            print(obj)
    def Produto_atualizar():
        UI.Produto_listar()
        id = int(input("Me informe o ID do produto a ser atualizado: "))
        desc = input("Me informe a nova descrição: ")
        preco = float(input("Me informe o novo preço: "))
        estoque = int(input("Me informe o novo estoque: "))
        idcat = int(input("Me informe o ID categoria desse produto: "))
        View.produto_atualizar(id, desc, preco, estoque, idcat)

    def Produto_excluir():
        UI.Produto_listar()
        id = int(input("Me informe o ID do produto a ser excluído: "))
        View.produto_excluir(id)

    def Produto_reajustar():
        percentual = float(input("Me informe o percentual que deseja aumentar: "))
        View.produto_reajustar(percentual)
    

    def Categoria_inserir():
        id = 0
        desc = input("Me informe a categoria a ser inserida: ")
        View.categoria_inserir(id,desc)
    def Categoria_listar():
        for obj in View.categoria_listar():
            print(obj)
    def Categoria_atualizar():
        UI.Categoria_listar()
        id = int(input("Me informe o ID a ser atualizado: "))
        desc = input("Me informe  a descrição a ser atualizada: ")
        View.categoria_atualizar(id,desc)
    def Categoria_excluir():
        UI.Categoria_listar()
        id = int(input("Me informe o ID a ser excluido: "))
        View.categoria_excluir(id)
        
    def Carrinho_inserir():
        UI.Produto_listar()
        id = int(input("Me informe o ID do produto que deseja adicionar ao carrinho: "))
        qtd = int(input("Me informe a quantidade desse produto que deseja adicionar ao carrinho: "))
        View.carrinho_inserir(id,qtd)
    def carrinho_listar():
        for obj in View.carrinho_listar_detalhado():
            print(obj)
    def carrinho_preco():
       View.carrinho_preco()
    def carrinho_comprar():
        carrinho = View.carrinho_listar_detalhado()
        if not carrinho:
            print("Carrinho vazio. Não há itens para comprar.")
            return
        print("itens no carrinho: ")
        for item in carrinho:
            print(item)
        
        total = View.carrinho_preco()
        print(f"Total da compra: {total}")

        confirmacao = input("Deseja mesmo finalizar a compra e comprar o carrinho? S/N")

        if confirmacao != "S":
            print("Compra cancelada")
            return 
        
        View.carrinho_comprar(UI.__usuario.get_id())
        print("Compra finalizada!")

UI.main()