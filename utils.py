from datetime import datetime

def validar_data(data_str):
    try:
        data_str = data_str.strip()
        formatos = ['%Y-%m-%d', '%Y%m%d', '%d/%m/%Y', '%d/%m/%y']
        for formato in formatos:
            try:
                data_obj = datetime.strptime(data_str, formato)
                return data_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        raise ValueError(f"Formato de data inválido: {data_str}")
    except Exception as e:
        print(f"Erro: {e}")
        print("Use o formato: YYYY-MM-DD (ex: 2024-01-15)")
        return None

def validar_hora(hora_str):
    try:
        hora_str = hora_str.strip()
        formatos = ['%H:%M', '%H:%M:%S', '%H%M']
        for formato in formatos:
            try:
                hora_obj = datetime.strptime(hora_str, formato)
                return hora_obj.strftime('%H:%M:%S')
            except ValueError:
                continue
        raise ValueError(f"Formato de hora inválido: {hora_str}")
    except Exception as e:
        print(f"Erro: {e}")
        print("Use o formato: HH:MM (ex: 14:30)")
        return None