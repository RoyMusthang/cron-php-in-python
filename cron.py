import os
import subprocess
import time
from datetime import datetime

# Caminho do diretório onde os arquivos PHP estão localizados
diretorio = '/home/josue/sandbox/public_html'

# Definir os horários agendados para execução
cron_times = [
    "08:50", "09:30", "10:40", "11:30", "12:50", "14:30", 
    "15:40", "16:30", "17:40", "18:30", "19:40", "20:50", 
    "21:30", "22:40", "23:50"
]

# Converter os horários para timestamps (segundos desde a época Unix) para maior precisão
cron_timestamps = [datetime.strptime(time_str, "%H:%M").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day).timestamp() for time_str in cron_times]

def check_and_execute():
    # Obter o tempo atual em timestamp
    now = time.time()

    # Verificar se o tempo atual está dentro de 1 minuto antes ou depois do horário agendado
    for cron_time in cron_timestamps:
        # Verificar se estamos dentro de 30 segundos do tempo agendado
        if abs(now - cron_time) <= 30:
            # Encontrar o nome do arquivo baseado no cron_time
            hour_minute = datetime.fromtimestamp(cron_time).strftime("%H%M")
            arquivo_php = f"scraper_{hour_minute}.php"
            arquivo_path = os.path.join(diretorio, arquivo_php)

            if os.path.exists(arquivo_path):
                print(f'Executando {arquivo_path}...')
                try:
                    subprocess.run(['php', arquivo_path], check=True)
                    print(f'{arquivo_php} executado com sucesso.')
                except subprocess.CalledProcessError as e:
                    print(f'Erro ao executar {arquivo_php}: {e}')
            else:
                print(f'{arquivo_php} não encontrado no diretório {diretorio}.')

def main():
    while True:
        check_and_execute()
        # Dormir por 10 segundos antes de verificar novamente (evita uso excessivo de CPU)
        time.sleep(10)

if __name__ == "__main__":
    main()
