from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar o driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ==== 1) Estados e municípios  ====
estados_municipios = {
    "//*[@id='segunda-coluna']/ul/li[18]/div": [  # Pernambuco
        "Recife", "Jaboatão dos Guararapes", "Olinda", "Paulista",
        "Cabo de Santo Agostinho", "Camaragibe", "São Lourenço da Mata",
        "Abreu e Lima", "Igarassu", "Goiana", "Ipojuca", "Moreno",
        "Itapissuma", "Ilha de Itamaracá", "Araçoiaba"
    ],
    "//*[@id='segunda-coluna']/ul/li[7]/div": [  # Ceará
        "Fortaleza", "Caucaia", "Maracanaú", "Maranguape", "Aquiraz",
        "Cascavel", "Pacajus", "Horizonte", "Pacatuba", "São Gonçalo do Amarante",
        "Eusébio", "Trairi", "Itaitinga", "Paracuru", "Paraipaba",
        "Pindoretama", "Guaiúba", "Chorozinho", "São Luís do Curu"
    ]
}

# ==== 2) Configuração do ChromeDriver  ====
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Users\João Faelis\Desktop\IBGE_MORTALIDADE",
    "download.prompt_for_download": False,
    "directory_upgrade": True
})

driver = webdriver.Chrome(
    service=Service(r"C:\Users\João Faelis\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"),
    options=chrome_options
)

driver.set_page_load_timeout(300)  # Timeout de carregamento de página
driver.maximize_window()

# ==== 3) Função para tentar acessar a URL com várias tentativas ====
def safe_get(driver, url, retries=3, wait=10):
    """
    Tenta acessar a URL repetidamente, em caso de timeout ou erro temporário.
    :param driver: Instância do driver Selenium
    :param url: URL a ser acessada
    :param retries: Quantidade de tentativas
    :param wait: Tempo de espera (segundos) entre as tentativas
    """
    for attempt in range(retries):
        try:
            driver.get(url)
            return
        except Exception as e:
            print(f"Tentativa {attempt+1} falhou para {url} -> {e}")
            time.sleep(wait)
    raise Exception(f"Não foi possível carregar a página após {retries} tentativas: {url}")

# ==== 4) URL do site do IBGE  ====
url = "https://cidades.ibge.gov.br/brasil/pesquisa/17/15752"

# ==== 5) Funções auxiliares ====
def wait_for_element(by, value, timeout=5):
    """Espera até que o elemento esteja presente no DOM."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def wait_for_element_visible(by, value, timeout=5):
    """Espera até que o elemento esteja visível na tela."""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))

def click_element(by, value, timeout=5):
    """Clique seguro em um elemento (tenta JavaScript se falhar)."""
    element = wait_for_element_visible(by, value, timeout=timeout)
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)

# ==== 6) XPaths usados repetidamente  ====
pesquisas_xpath = "//a[text()='Pesquisas']"
mortalidade_xpath = "//*[@id='container']/div[2]/submenu/div/ul/li[15]/div/p"
serie_historica_xpath = "//*[@id='container']/div[4]/pesquisa/div/pesquisa-header/div/div[2]/div[2]"
grupo_idade_menu_xpath = "//*[@id='container']/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[3]/td/div[1]"
botao_download_xpath = "//*[@id='pesquisa-dados']/pesquisa-graficos/div/grafico/div/div/div/a/i"

# Lista dos grupos de idade (XPaths)
grupos_idade = [
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[7]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[8]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[9]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[10]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[11]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[12]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[13]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[14]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[15]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[16]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[17]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[18]/td/div[3]',
    '//*[@id="container"]/div[4]/pesquisa/div/div/pesquisa-indicadores/table/tr[19]/td/div[3]',
]

# ==== 7) Fluxo principal  ====
# Agora, em vez de dar 'back' para cada município, recarregamos a URL inicial.
# Assim, cada município recomeça da página de seleção do IBGE.

for estado_xpath, municipios in estados_municipios.items():
    for municipio in municipios:
        try:
            # Recarrega a página inicial do IBGE para começar "do zero"
            safe_get(driver, url, retries=3, wait=5)
            time.sleep(2)

            # Clique em 'Selecionar local'
            click_element(By.XPATH, "//button[text()='Selecionar local']")
            time.sleep(2)

            # Clique em 'Municípios'
            click_element(By.XPATH, "//li[@id='menu__municipio']")
            time.sleep(2)

            # Clique no estado
            click_element(By.XPATH, estado_xpath)
            time.sleep(2)

            # Seleciona o município
            municipio_xpath = f"//a[contains(text(), '{municipio}')]"
            click_element(By.XPATH, municipio_xpath)
            time.sleep(2)

            # Clique em 'Pesquisas'
            click_element(By.XPATH, pesquisas_xpath)
            time.sleep(2)

            # Clique em 'Mortalidade'
            click_element(By.XPATH, mortalidade_xpath)
            time.sleep(2)

            # Clique na 'Série Histórica'
            click_element(By.XPATH, serie_historica_xpath)
            time.sleep(2)

            # Clica no menu 'Grupo de Idade'
            click_element(By.XPATH, grupo_idade_menu_xpath)
            time.sleep(2)

            # Percorrer cada grupo de idade
            for grupo_xpath in grupos_idade:
                try:
                    # Verifica se o elemento existe
                    grupo_elements = driver.find_elements(By.XPATH, grupo_xpath)
                    if not grupo_elements:
                        print(f"[INFO] Grupo de idade não encontrado (XPATH: {grupo_xpath}) para {municipio}. Pulando...")
                        continue

                    # Clica no grupo
                    grupo_elements[0].click()
                    time.sleep(2)

                    # Faz o download do gráfico
                    download_button = wait_for_element_visible(By.XPATH, botao_download_xpath, timeout=10)
                    download_button.click()
                    time.sleep(3)  # espera download terminar

                    # Volta ao menu de grupos de idade para selecionar o próximo
                    click_element(By.XPATH, grupo_idade_menu_xpath)
                    time.sleep(2)

                except Exception as e:
                    print(f"[ERRO GRUPO_IDADE] Município={municipio}, XPath={grupo_xpath}, ERRO={e}")
                    continue

            print(f"[OK] Finalizado município: {municipio}")

        except Exception as e:
            print(f"[ERRO MUNICIPIO] {municipio} -> {e}")
            continue

# ==== 8) Encerrar o navegador ====
driver.quit()
