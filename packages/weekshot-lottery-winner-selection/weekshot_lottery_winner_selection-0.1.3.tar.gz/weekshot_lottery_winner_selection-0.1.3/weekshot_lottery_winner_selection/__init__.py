import httpx

async def generate_random_numbers(
    api_key: str,
    max_number: int,
    count: int,
    unique: bool = True,
) -> list[int]:
    """
    Generate random numbers from 1 to `max_number`

    :param `api_key`: Random.org API key
    :param `max_number`: Max number of random numbers
    :param `count`: Count of random numbers
    :param `unique`: Unique random numbers, default is True
    :return: List of random numbers
    """
        
    url = f"https://api.random.org/json-rpc/2/invoke"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": api_key,
            "n": count,
            "min": 1,
            "max": max_number,
            "replacement": not unique
        },
        "id": 1
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        random_numbers = data["result"]["random"]["data"]
        return random_numbers
    else:
        raise Exception("Failed to generate random numbers")
