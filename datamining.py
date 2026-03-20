# Mineracao de dados
# Importando bibliotecas
import requests
import json
import pandas as pd
import time

# Abrindo o arquivo json e salvando numa variavel
with open("export.json", "r", encoding="utf-8") as file:
    data = json.load(file)

places = [] # Criando uma lista vazia

for el in data["elements"]:
    tags = el.get("tags", {})

    places.append({
        "lat": el.get("lat"),
        "lon": el.get("lon"),
        "taxa" : tags.get("fee"),
        "tipo": tags.get("amenity"),
        "capacidade": tags.get("capacity"),
    })


places = pd.DataFrame(places)

# -----------------------------------------------------------------------------------------

# Procurando pelo endereco
# Extraindo os enderecos pela lat e lon

enderecos = []
erros = 0

headers = {
    "User-Agent": "datamining/1.0 (contato: misaelalmeidamisael@gmail.com)"
}

for el in data["elements"]:
    lat = el.get("lat")
    lon = el.get("lon")

    if lat is None or lon is None:
        erros += 1
        continue

    # Usando Nomination para procura (e interessante abrir o arquivo JSON gerado para melhorar a busca)
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erro HTTP: {response.status_code}")
        time.sleep(2)
        continue

    try:
        response_data = response.json()
    except:
        print("Erro JSON")
        continue

    address = response_data.get("address", {})

    # Juntando tudo em um so dataframe
    enderecos.append({
        "nome": tags.get("name"),
        "lat": el.get("lat"),
        "lon": el.get("lon"),
        "tipo": tags.get("amenity"),
        "capidade": tags.get("capacity"),
        "rua": address.get("road"),
        "cep": address.get("postcode"),
        "road": address.get("road"),
        "suburb": address.get("suburb"),
        "city": address.get("city"),
        "state": address.get("state"),
        "postcode": address.get("postcode")
    })
    print(enderecos)

    time.sleep(1.0)

enderecos = pd.DataFrame(enderecos)
print(enderecos)
print(places)
enderecos.to_csv("enderecos.csv", index=False)







