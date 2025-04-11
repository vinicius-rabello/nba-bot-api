from datetime import datetime
import hashlib

def get_day_of_week_from_date_string(date_str):
    """
    Pega o dia da semana de uma string "YYYY-mm-dd" (Por ex: 2025-03-28).

    Parâmetros:
        date_str (str): String no formato "YYYY-mm-dd" (Por ex: 2025-03-28).

    Retorno:
        str: Nome do dia da semana em inglês (ex: "Monday", "Thursday").
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    day_of_week = date_obj.strftime('%A')  # Dia da semana em inglês
    return day_of_week

def get_month_from_date_string(date_str):
    """
    Pega o número do mês de uma string "YYYY-mm-dd" (Por ex: 2025-03-28).

    Parâmetros:
        date_str (str): String no formato "YYYY-mm-dd" (Por ex: 2025-03-28).

    Retorno:
        int: Número do mês correspondente (1 a 12) ou None se não for encontrado.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    month = date_obj.month
    return month

def month_name_to_num(month_name):
    """
    Converte o nome do mês para seu número correspondente.

    Parâmetros:
        month_name (str): Nome do mês em inglês (exemplo: "January", "February").

    Retorno:
        int: Número do mês correspondente (1 a 12) ou None se não for encontrado.
    """
    MONTH_TO_NUM = {
        "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
        "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
    }

    # Converte para minúsculas para evitar erros de formatação
    return MONTH_TO_NUM.get(month_name.lower())

def month_num_to_name(month_num):
    """
    Converte o número do mês para seu nome correspondente.

    Parâmetros:
        month_num (int): Número do mês (1 a 12).

    Retorno:
        str: Nome do mês correspondente (exemplo: "January", "February") ou None se não for encontrado.
    """
    NUM_TO_MONTH = {
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
    }

    return NUM_TO_MONTH.get(month_num)

def format_date(input_date, timezone=None):
    """
    Formata a data extraída da página para o formato YYYY-MM-DD.

    Parâmetros:
        input_date (str): Data no formato "Day, Month DD" (exemplo: "Friday, March 15").
        timezone (datetime.tzinfo, opcional): Fuso horário para considerar o ano corretamente.

    Retorno:
        str: Data formatada no formato "YYYY-MM-DD".
    """
    # Obtém o ano atual considerando o fuso horário (se fornecido)
    today = datetime.now(tz=timezone)
    year = today.year

    try:
        # Extrai o mês e o dia da string de entrada
        day_of_week = input_date.split(', ')[0].strip()
        date_string = input_date.split(', ')[1].strip()
        month_name, day = date_string.split(' ')
        day = int(day.strip())

        # Converte o nome do mês para número
        month = month_name_to_num(month_name)
        if month is None:
            raise ValueError(f"Nome do mês inválido: {month_name}")

        # Verifica se o dia da semana da data gerada bate com o dia da semana da entrada
        # Isso é necessário porque a string de entrada não contém o ano, e o ano atual pode não ser o correto
        # Exemplo: Se hoje é 2025, mas a data "Friday, March 15" realmente pertence a 2024,
        # o dia da semana não vai coincidir, e precisamos subtrair 1 do ano.
        date = f"{year:04d}-{month:02d}-{day:02d}"
        if get_day_of_week_from_date_string(date) != day_of_week:
            date = f"{year-1:04d}-{month:02d}-{day:02d}"

        return date

    except (IndexError, ValueError) as e:
        raise ValueError(f"Erro ao processar data '{input_date}': {e}")

def generate_game_id(date, home_team, away_team):
    """
    Gera um ID único para cada jogo baseado na data e nos times.

    Parâmetros:
        date (str): Data do jogo no formato 'YYYY-MM-DD'.
        home_team (str): Nome do time da casa.
        away_team (str): Nome do time visitante.

    Retorno:
        str: ID único gerado como hash SHA-1.
    """
    raw_id = f"{date}_{home_team}_{away_team}".lower().replace(" ", "_")
    return hashlib.sha1(raw_id.encode()).hexdigest()[:10]  # Hash curto para evitar IDs longos