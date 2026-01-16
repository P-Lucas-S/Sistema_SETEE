from datetime import datetime
import crud
import utils

class SistemaSolicitacoes:
    def __init__(self, conn):
        self.conn = conn
    
    def menu_principal(self):
        while True:
            print("\n" + "="*50)
            print("SISTEMA DE SOLICITAÇÕES")
            print("="*50)
            print("1. PESSOAS")
            print("2. USUÁRIOS")
            print("3. ATENDIMENTOS")
            print("4. SOLICITAÇÕES")
            print("0. SAIR")
            print("="*50)
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self.menu_pessoa()
            elif opcao == "2":
                self.menu_usuario()
            elif opcao == "3":
                self.menu_atendimento()
            elif opcao == "4":
                self.menu_solicitacao()
            elif opcao == "0":
                return
            else:
                print("Opção inválida!")
    
    def menu_pessoa(self):
        while True:
            print("\n" + "="*40)
            print("MENU PESSOAS")
            print("="*40)
            print("1. Listar todas")
            print("2. Buscar por nome")
            print("3. Inserir nova pessoa")
            print("4. Atualizar pessoa")
            print("5. Remover pessoa")
            print("0. Voltar")
            print("="*40)
            
            opcao = input("Opção: ")
            
            if opcao == "1":
                self.listar_pessoas()
            elif opcao == "2":
                self.buscar_pessoa_nome()
            elif opcao == "3":
                self.inserir_pessoa()
            elif opcao == "4":
                self.atualizar_pessoa()
            elif opcao == "5":
                self.remover_pessoa()
            elif opcao == "0":
                return
            else:
                print("Opção inválida!")
    
    def listar_pessoas(self):
        print("\n--- LISTAR PESSOAS ---")
        resultado = crud.select_listar_pessoas(self.conn)
        
        if resultado:
            print(f"\nTotal: {len(resultado)} pessoa(s)\n")
            for linha in resultado:
                email = linha[2] if linha[2] else "(sem email)"
                print(f"ID: {linha[0]:3d} | Nome: {linha[1]:30} | Email: {email}")
        else:
            print("Nenhuma pessoa encontrada.")
    
    def buscar_pessoa_nome(self):
        print("\n--- BUSCAR PESSOA ---")
        nome = input("Nome (ou parte): ")
        
        if not nome:
            print("Nome não pode ser vazio!")
            return
        
        resultado = crud.select_buscar_pessoa_nome(self.conn, nome)
        
        if resultado:
            print(f"\nEncontrado(s) {len(resultado)} registro(s):\n")
            for linha in resultado:
                email = linha[2] if linha[2] else "(sem email)"
                print(f"ID: {linha[0]:3d} | Nome: {linha[1]:30} | Email: {email}")
        else:
            print(f"Nenhuma pessoa encontrada com '{nome}'.")
    
    def inserir_pessoa(self):
        print("\n--- INSERIR PESSOA ---")
        
        while True:
            nome = input("Nome/Razão Social: ").strip()
            if nome:
                break
            print("Nome não pode ser vazio!")
        
        email = input("Email (opcional): ").strip()
        if not email:
            email = None
        
        resultado = crud.insert_pessoa(self.conn, nome, email)
        
        if resultado is not None and resultado > 0:
            print("Pessoa inserida com sucesso!")
    
    def atualizar_pessoa(self):
        print("\n--- ATUALIZAR PESSOA ---")
        self.listar_pessoas()
        
        try:
            id_pessoa = int(input("\nID da pessoa a atualizar: "))
        except ValueError:
            print("ID deve ser um número!")
            return
        
        novo_nome = input("Novo nome (deixe em branco para manter): ").strip()
        novo_email = input("Novo email (deixe em branco para manter): ").strip()
        
        if not novo_nome and not novo_email:
            print("Nenhuma alteração realizada.")
            return
        
        resultado = crud.update_pessoa(self.conn, id_pessoa, novo_nome, novo_email)
        
        if resultado is not None and resultado > 0:
            print("Pessoa atualizada com sucesso!")
    
    def remover_pessoa(self):
        print("\n--- REMOVER PESSOA ---")
        self.listar_pessoas()
        
        try:
            id_pessoa = int(input("\nID da pessoa a remover: "))
        except ValueError:
            print("ID deve ser um número!")
            return
        
        dependencias = crud.verificar_dependencias_pessoa(self.conn, id_pessoa)
        tem_dependencias = any(count > 0 for _, count in dependencias)
        
        if tem_dependencias:
            print(f"\nA pessoa tem dependências:")
            for tabela, count in dependencias:
                if count > 0:
                    print(f"   - {tabela}: {count} registro(s)")
            print("\nNão é possível remover pessoas com atendimentos ou solicitações.")
            return
        
        confirmar = input(f"\nTEM CERTEZA que deseja remover a pessoa com ID {id_pessoa}? (s/n): ")
        
        if confirmar.lower() == 's':
            resultado = crud.delete_pessoa(self.conn, id_pessoa)
            
            if resultado is not None and resultado > 0:
                print("Pessoa removida com sucesso!")
        else:
            print("Operação cancelada.")
    
    def menu_usuario(self):
        while True:
            print("\n" + "="*40)
            print("MENU USUÁRIOS")
            print("="*40)
            print("1. Listar todos")
            print("2. Inserir novo usuário")
            print("3. Atualizar usuário")
            print("4. Remover usuário")
            print("0. Voltar")
            print("="*40)
            
            opcao = input("Opção: ")
            
            if opcao == "1":
                self.listar_usuarios()
            elif opcao == "2":
                self.inserir_usuario()
            elif opcao == "3":
                self.atualizar_usuario()
            elif opcao == "4":
                self.remover_usuario()
            elif opcao == "0":
                return
            else:
                print("Opção inválida!")
    
    def listar_usuarios(self):
        print("\n--- LISTAR USUÁRIOS ---")
        resultado = crud.select_listar_usuarios(self.conn)
        
        if resultado:
            print(f"\nTotal: {len(resultado)} usuário(s)\n")
            for linha in resultado:
                status = "Ativo" if linha[4] else "Inativo"
                print(f"ID: {linha[0]:3d} | Nome: {linha[1]:15} | Login: {linha[2]:10} | Perfil: {linha[3]:15} | {status}")
        else:
            print("Nenhum usuário encontrado.")
    
    def inserir_usuario(self):
        print("\n--- INSERIR USUÁRIO ---")
        
        while True:
            nome = input("Nome: ").strip()
            if nome:
                break
            print("Nome não pode ser vazio!")
        
        while True:
            login = input("Login: ").strip()
            if login:
                break
            print("Login não pode ser vazio!")
        
        senha = input("Senha: ").strip()
        if not senha:
            senha = "123"
        
        perfis = crud.listar_perfis(self.conn)
        if not perfis:
            print("Nenhum perfil disponível!")
            return
        
        print("\nPerfis disponíveis:")
        for perfil in perfis:
            print(f"  {perfil[0]} - {perfil[1]}")
        
        try:
            perfil_id = int(input("\nID do perfil: "))
        except ValueError:
            print("ID deve ser um número!")
            return
        
        resultado = crud.insert_usuario(self.conn, nome, login, senha, perfil_id)
        
        if resultado is not None and resultado > 0:
            print("Usuário inserido com sucesso!")
    
    def atualizar_usuario(self):
        print("\n--- ATUALIZAR USUÁRIO ---")
        self.listar_usuarios()
        
        try:
            id_usuario = int(input("\nID do usuário a atualizar: "))
        except ValueError:
            print("ID deve ser um número!")
            return
        
        novo_nome = input("Novo nome (deixe em branco para manter): ").strip()
        novo_login = input("Novo login (deixe em branco para manter): ").strip()
        novo_status = input("Status (1=Ativo, 0=Inativo, Enter=manter): ").strip()
        
        ativo = None
        if novo_status == '1':
            ativo = True
        elif novo_status == '0':
            ativo = False
        
        if not novo_nome and not novo_login and ativo is None:
            print("Nenhuma alteração realizada.")
            return
        
        resultado = crud.update_usuario(self.conn, id_usuario, novo_nome, novo_login, ativo)
        
        if resultado is not None and resultado > 0:
            print("Usuário atualizado com sucesso!")
    
    def remover_usuario(self):
        print("\n--- REMOVER USUÁRIO ---")
        self.listar_usuarios()
        
        try:
            id_usuario = int(input("\nID do usuário a remover: "))
        except ValueError:
            print("ID deve ser um número!")
            return
        
        dependencias = crud.verificar_dependencias_usuario(self.conn, id_usuario)
        tem_dependencias = any(count > 0 for _, count in dependencias)
        
        if tem_dependencias:
            print(f"\nO usuário tem dependências:")
            for tabela, count in dependencias:
                if count > 0:
                    print(f"   - {tabela}: {count} registro(s)")
            print("\nNão é possível remover usuários com atendimentos ou solicitações.")
            return
        
        confirmar = input(f"\nTEM CERTEZA que deseja remover o usuário com ID {id_usuario}? (s/n): ")
        
        if confirmar.lower() == 's':
            resultado = crud.delete_usuario(self.conn, id_usuario)
            
            if resultado is not None and resultado > 0:
                print("Usuário removido com sucesso!")
        else:
            print("Operação cancelada.")
    
    def menu_atendimento(self):
        while True:
            print("\n" + "="*40)
            print("MENU ATENDIMENTOS")
            print("="*40)
            print("1. Listar todos")
            print("2. Buscar por data")
            print("3. Inserir novo atendimento")
            print("0. Voltar")
            print("="*40)
            
            opcao = input("Opção: ")
            
            if opcao == "1":
                self.listar_atendimentos()
            elif opcao == "2":
                self.buscar_atendimento_data()
            elif opcao == "3":
                self.inserir_atendimento()
            elif opcao == "0":
                return
            else:
                print("Opção inválida!")
    
    def listar_atendimentos(self):
        print("\n--- LISTAR ATENDIMENTOS ---")
        resultado = crud.select_listar_atendimentos(self.conn)
        
        if resultado:
            print(f"\nTotal: {len(resultado)} atendimento(s)\n")
            for linha in resultado:
                obs = f" - {linha[5]}" if linha[5] else ""
                print(f"ID: {linha[0]:3d} | {linha[1]} {linha[2]} | Pessoa: {linha[3]:20} | Atendente: {linha[4]}{obs}")
        else:
            print("Nenhum atendimento encontrado.")
    
    def buscar_atendimento_data(self):
        print("\n--- BUSCAR ATENDIMENTOS POR DATA ---")
        data_str = input("Data (ex: 2024-01-15): ")
        
        data = utils.validar_data(data_str)
        if not data:
            return
        
        resultado = crud.select_buscar_atendimento_data(self.conn, data)
        
        if resultado:
            print(f"\nAtendimentos em {data}: {len(resultado)} registro(s)\n")
            for linha in resultado:
                obs = f" - {linha[5]}" if linha[5] else ""
                print(f"ID: {linha[0]:3d} | {linha[2]} | Pessoa: {linha[3]:20} | Atendente: {linha[4]}{obs}")
        else:
            print(f"Nenhum atendimento encontrado para {data}.")
    
    def inserir_atendimento(self):
        print("\n--- INSERIR ATENDIMENTO ---")
        
        while True:
            data_str = input("Data (YYYY-MM-DD) [hoje]: ").strip()
            if not data_str:
                data_str = datetime.now().strftime('%Y-%m-%d')
            
            data = utils.validar_data(data_str)
            if data:
                break
        
        while True:
            hora_str = input("Hora (HH:MM) [agora]: ").strip()
            if not hora_str:
                hora_str = datetime.now().strftime('%H:%M')
            
            hora = utils.validar_hora(hora_str)
            if hora:
                break
        
        observacao = input("Observação (opcional): ").strip()
        if not observacao:
            observacao = None
        
        pessoas = crud.listar_pessoas_simples(self.conn)
        if not pessoas:
            print("Nenhuma pessoa cadastrada!")
            return
        
        print("\nPessoas disponíveis:")
        for pessoa in pessoas:
            print(f"  {pessoa[0]} - {pessoa[1]}")
        
        try:
            pessoa_id = int(input("\nID da pessoa: "))
        except ValueError:
            print("ID deve ser um número!")
            return
        
        usuarios = crud.listar_usuarios_ativos(self.conn)
        if not usuarios:
            print("Nenhum usuário ativo!")
            return
        
        print("\nUsuários disponíveis:")
        for usuario in usuarios:
            print(f"  {usuario[0]} - {usuario[1]}")
        
        try:
            usuario_id = int(input("\nID do usuário: "))
        except ValueError:
            print("ID deve ser um número!")
            return
        
        resultado = crud.insert_atendimento(self.conn, data, hora, observacao, pessoa_id, usuario_id)
        
        if resultado is not None and resultado > 0:
            print("Atendimento inserido com sucesso!")
    
    def menu_solicitacao(self):
        """Menu de solicitações"""
        print("\n" + "="*40)
        print("MENU SOLICITAÇÕES")
        print("="*40)
        print("1. Listar solicitações")
        print("2. Ver detalhes da solicitação")
        print("3. Atualizar status da solicitação")
        print("0. Voltar")
        print("="*40)
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            self.listar_solicitacoes()
        elif opcao == "2":
            self.ver_detalhes_solicitacao()
        elif opcao == "3":
            self.atualizar_status_solicitacao()
        elif opcao == "0":
            return
        else:
            print("Opção inválida!")
    
    def listar_solicitacoes(self):
        """Lista todas as solicitações"""
        print("\n--- LISTAR SOLICITAÇÕES ---")
        resultado = crud.select_listar_solicitacoes(self.conn)
        
        if resultado:
            print(f"\nTotal: {len(resultado)} solicitação(ões)\n")
            for linha in resultado:
                status = linha[4]
                # Código de cor para status
                if status == "Aprovado":
                    status_str = f"[✓] {status}"
                elif status == "Pendente":
                    status_str = f"[!] {status}"
                elif status == "Em análise":
                    status_str = f"[↻] {status}"
                else:
                    status_str = f"[?] {status}"
                
                print(f"ID: {linha[0]:3d} | {linha[1]} | {linha[2]:20} | {linha[3]:30} | {status_str}")
        else:
            print("Nenhuma solicitação encontrada.")
    
    def ver_detalhes_solicitacao(self):
        """Mostra detalhes de uma solicitação específica"""
        print("\n--- DETALHES DA SOLICITAÇÃO ---")
        
        try:
            id_solicitacao = int(input("ID da solicitação: "))
        except ValueError:
            print("ID deve ser um número!")
            return
        
        resultado = crud.select_detalhes_solicitacao(self.conn, id_solicitacao)
        
        if resultado:
            print(f"\n📋 SOLICITAÇÃO #{resultado[0][0]}")
            print("="*50)
            print(f"📅 Data: {resultado[0][1]}")
            print(f"👤 Pessoa: {resultado[0][2]}")
            print(f"📧 Email: {resultado[0][3]}")
            print(f"📝 Tipo: {resultado[0][4]}")
            print(f"🔍 Status: {resultado[0][5]}")
            print(f"👨‍💼 Responsável: {resultado[0][6]}")
            print(f"📄 Descrição: {resultado[0][7]}")
            if resultado[0][8]:
                print(f"🗒️  Observação: {resultado[0][8]}")
            print("="*50)
        else:
            print(f"Solicitação com ID {id_solicitacao} não encontrada.")
    
    def atualizar_status_solicitacao(self):
        """Atualiza o status de uma solicitação"""
        print("\n--- ATUALIZAR STATUS DA SOLICITAÇÃO ---")
        
        # Listar status disponíveis
        status_lista = crud.listar_status_disponiveis(self.conn)
        if not status_lista:
            print("Nenhum status disponível!")
            return
        
        print("\nStatus disponíveis:")
        for status in status_lista:
            print(f"  {status[0]} - {status[1]}")
        
        try:
            id_solicitacao = int(input("\nID da solicitação: "))
            novo_status_id = int(input("ID do novo status: "))
        except ValueError:
            print("IDs devem ser números!")
            return
        
        resultado = crud.update_status_solicitacao(self.conn, id_solicitacao, novo_status_id)
        
        if resultado is not None and resultado > 0:
            print("Status da solicitação atualizado com sucesso!")
        else:
            print("Erro ao atualizar status.")