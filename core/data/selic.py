import requests

SELIC_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"

def get_selic_rate() -> float:
  """
  Busca o valor da Selic mais atualizada através de uma api pública do Banco Central.
  """
  response = requests.get(SELIC_URL, timeout=5)
  response.raise_for_status()
  data = response.json()
  return float(data[0]["valor"]) / 100