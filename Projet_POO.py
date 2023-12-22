import pandas as pd
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()


parametres_backtest = {
    "nom_indice": "Indice Crypto DeFi",
    "periode_backtest": {
        "debut": "2021-01-01",
        "fin": "2022-01-01"
    },
    "tags": ["DeFi", "blockchain"],
    "strategie": {
        "nom": "Stratégie de Momentum",
        "parametres": {
            "periode_momentum": 30,  # jours
            "seuil_achat": 0.05,  # 5% de croissance
            "seuil_vente": -0.03  # 3% de baisse
        }
    },
    "methode_ponderation": "pondération égale",
    "frequence_reéquilibrage": "mensuelle",
    "critere_selection": {
        "capitalisation_minimale": 1000000000,  # 1 milliard USD
        "volume_minimal": 10000000  # 10 millions USD
    }
}

def get_data(parametres_backtest):
    tags = parametres_backtest["tags"]
    print(tags)
    ids_categories = []
    ids_crypto = []
    categories_data = cg.get_coins_categories()
    for categorie in categories_data:
        contenu_categorie = " ".join(str(valeur) for valeur in categorie.values())

        for tag in tags:
           if tag.lower() in contenu_categorie.lower():
                ids_categories.append(categorie['id'])
                break
    print(ids_categories)
    for id_categorie in ids_categories:
        data_per_cate = cg.get_coins_markets(vs_currency='usd', category=str(id_categorie), per_page='250', sparkline='false', locale='en')
        print(data_per_cate)
        ids_per_cate = [crypto['id'] for crypto in data_per_cate]
        print(ids_per_cate)
        ids_crypto.extend(ids_per_cate)
    ids_crypto = list(set(ids_crypto))
    data_frame = pd.DataFrame(ids_crypto, columns=["ids"])
    return(data_frame)



if __name__=='__main__':
    parametres_backtest = {
        "tags": ["DeFi", "blockchain"]
    }
    data_frame = get_data(parametres_backtest)
    print(data_frame)