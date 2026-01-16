import database
import menus

def main():
    
    conn = database.conectar()
    if not conn:
        print("\nNão foi possível conectar ao banco de dados.")
        return
    
    try:
        sistema = menus.SistemaSolicitacoes(conn)
        sistema.menu_principal()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
    except Exception as e:
        print(f"\nErro fatal: {e}")
    finally:
        database.fechar_conexao(conn)

if __name__ == "__main__":
    main()