from typing import Any, Dict, List, Union
import requests
import os
def models() -> List[str]:    
    """
    Lists all the models supported by Konko. 
    """
    baseUrl = os.getenv('KONKO_URL')
    assert baseUrl is not None, "KONKO_URL must be set"

    token = os.getenv('KONKO_TOKEN')
    path = "-/routes"
    url = f"{baseUrl}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    try:
        result = response.json()

    except requests.JSONDecodeError as e:
        raise BackendError(
            f"Error decoding JSON from {url}. Text response: {response.text}",
            response=response,
        ) from e
    
    result = sorted(
        [k.lstrip("/").replace("--", "/") for k in result.keys() if "--" in k]
    )

    return result

def addModels(models: List[str]) -> bool:  
    """
    Host your proprietary fine-tuned models on the Konko AI engine for production-grade applications. 
    The Konko engine will characterize your model for cost, quality and latency and make it available to use in your application. 
    """  
    [print(f'Adding model {m}') for m in models]
    return True

os.environ['KONKO_URL'] = 'http://alb-http-1196840644.us-west-2.elb.amazonaws.com/'
print(models())