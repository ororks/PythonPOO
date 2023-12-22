import asyncio
import aiohttp
import pandas as pd
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

async def fetch_market_data(session, id_categorie):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category={id_categorie}&per_page=250&sparkline=false&locale=en"
    try:
        async with session.get(url) as response:
            data_per_cate = await response.json()
            # Récupération de l'ID et de la capitalisation boursière de chaque crypto
            return [{'id': crypto['id'], 'market_cap': crypto['market_cap']} for crypto in data_per_cate]
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour la catégorie {id_categorie}: {e}")
        return []

async def get_data(parametres_backtest):
    async with aiohttp.ClientSession() as session:
        tags = parametres_backtest["tags"]
        ids_categories = []
        crypto_data = []

        # Récupération des IDs de catégorie
        async with session.get("https://api.coingecko.com/api/v3/coins/categories") as response:
            categories_data = await response.json()

        for categorie in categories_data:
            contenu_categorie = " ".join(str(valeur) for valeur in categorie.values())
            for tag in tags:
                if tag.lower() in contenu_categorie.lower():
                    ids_categories.append(categorie['id'])
                    break
        print(f'la liste ids par catégorie est la suivante {ids_categories}')

        tasks = [fetch_market_data(session, id_categorie) for id_categorie in ids_categories]
        results = await asyncio.gather(*[asyncio.wait_for(task, timeout=15) for task in tasks])

        for data in results:
            crypto_data.extend(data)

        # Création d'un DataFrame avec les IDs et les capitalisations boursières
        data_frame = pd.DataFrame(crypto_data)
        return data_frame

if __name__ == '__main__':
    parametres_backtest = {
        "tags": ["DeFi", "blockchain"]
    }
    data_frame = asyncio.run(get_data(parametres_backtest))
    print(data_frame)

