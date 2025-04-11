import scrapers.nba_scraper.constants as const  # Importa as constantes definidas no módulo nba_scraper
from selenium import webdriver  # Importa o WebDriver do Selenium para controle do navegador
from selenium.webdriver.common.by import By  # Importa o localizador de elementos
from selenium.common.exceptions import NoSuchElementException  # Para tratamento de exceções
from selenium.webdriver.chrome.options import Options

class NbaScraper(webdriver.Chrome):
    """
    Classe para raspar informações sobre jogos da NBA usando Selenium.
    Herda da classe webdriver.Chrome para controlar o navegador Chrome.
    """

    def __init__(self):
        """
        Inicializa a classe, configurando o caminho do driver do Chrome e iniciando o navegador.

        Args:
            driver_path (str): Caminho para o diretório onde está o driver do Chrome.
        """
        # Configura as opções do Chrome para ambiente Docker
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Inicializa o WebDriver
        super(NbaScraper, self).__init__(options=chrome_options)
        
        self.implicitly_wait(5)  # Define um tempo de espera implícito de 5 segundos
        self.minimize_window()  # Minimiza a janela do navegador para melhor desempenho

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Garante que o navegador seja fechado corretamente ao sair do contexto.
        """
        print("Closing the NbaScraper...")
        self.quit()

    def land_first_page(self, url=const.BASE_URL):
        """Acessa a página inicial da NBA definida em `const.BASE_URL`."""
        self.get(url)

    def get_schedule_days(self):
        """
        Retorna todos os blocos de dias com jogos na programação.

        Returns:
            list: Lista de elementos representando os dias da programação.
        """
        return self.find_elements(By.XPATH, ".//div[contains(@class, 'ScheduleDay_sd_')]")

    def get_schedule_day_date(self, schedule_day):
        """
        Obtém a data de um dia específico da programação.

        Args:
            schedule_day (WebElement): Elemento do dia da programação.

        Returns:
            str: Data do dia da programação.
        """
        return schedule_day.find_element(By.XPATH, ".//h4[contains(@class, 'ScheduleDay_sdDay')]").get_attribute("textContent")

    def get_schedule_day_games(self, schedule_day):
        """
        Obtém o bloco de jogos de um determinado dia.

        Args:
            schedule_day (WebElement): Elemento do dia da programação.

        Returns:
            WebElement: Bloco contendo os jogos do dia.
        """
        return schedule_day.find_element(By.XPATH, ".//div[contains(@class, 'ScheduleDay_sdGames')]")

    def get_schedule_games(self, schedule_day_games):
        """
        Retorna a lista de jogos dentro de um bloco de jogos.

        Args:
            schedule_day_games (WebElement): Elemento que contém os jogos de um dia.

        Returns:
            list: Lista de elementos representando os jogos.
        """
        return schedule_day_games.find_elements(By.XPATH, "./div[contains(@class, 'ScheduleGame')]")

    def get_schedule_game_time(self, schedule_game):
        """
        Obtém o horário do jogo.

        Args:
            schedule_game (WebElement): Elemento representando um jogo.

        Returns:
            str: Horário do jogo ou status do evento.
        """
        schedule_status_text = schedule_game.find_element(By.XPATH, ".//span[contains(@class, 'ScheduleStatusText')]")
        return schedule_status_text.text

    def get_schedule_game_broadcaster(self, schedule_game):
        """
        Obtém o canal de transmissão do jogo.

        Args:
            schedule_game (WebElement): Elemento representando um jogo.

        Returns:
            str: Nome da emissora ou 'NBA League Pass' caso não esteja especificado.
        """
        try:
            broadcaster_div = schedule_game.find_element(By.XPATH, ".//div[contains(@class, 'Broadcasters')]")
        except NoSuchElementException:  # Captura apenas a exceção esperada
            return None 
        try:
            broadcaster_p = broadcaster_div.find_element(By.XPATH, ".//p[contains(@class, 'Broadcaster')]")
            broadcaster = broadcaster_p.text
            return broadcaster
        except NoSuchElementException:
            return "NBA League Pass"

    def get_schedule_game_teams(self, schedule_game):
        """
        Obtém os nomes das equipes que disputarão o jogo.

        Args:
            schedule_game (WebElement): Elemento representando um jogo.

        Returns:
            list: Lista contendo os nomes das equipes (mandante e visitante).
        """
        teams = schedule_game.find_elements(By.XPATH, ".//div[contains(@class, 'ScheduleGame_sgTeam')]")
        return [team.find_element(By.XPATH, ".//a").text for team in teams]
    
    def get_schedule_game_scores(self, schedule_game):
        """
        Obtém o placar das partidas que já aconteceram.

        Args:
            schedule_game (WebElement): Elemento representando um jogo.

        Returns:
            list: Lista contendo os placares das equipes (mandante e visitante).
        """
        scores = schedule_game.find_elements(By.XPATH, ".//div[contains(@class, 'ScheduleGame_sgScore')]")
        # Se o jogo ainda não aconteceu, scores será uma lista vazia.
        if len(scores) == 0:
            return [None, None]
        
        return [score.find_element(By.XPATH, ".//span").text for score in scores]

    def get_schedule_game_location(self, schedule_game):
        """
        Obtém o local onde o jogo será realizado.

        Args:
            schedule_game (WebElement): Elemento representando um jogo.

        Returns:
            tuple: Nome da arena, cidade e estado onde o jogo será realizado.
        """
        location_inner = schedule_game.find_element(By.XPATH, ".//div[contains(@class, 'ScheduleGame_sgLocationInner')]")
        location_details = location_inner.find_elements(By.XPATH, ".//div")
        
        arena = location_details[0].get_attribute("textContent")
        city_state = location_details[1].get_attribute("textContent")

        # Divide cidade e estado, garantindo a remoção de espaços desnecessários
        city, state = map(str.strip, city_state.split(","))

        return arena, city, state