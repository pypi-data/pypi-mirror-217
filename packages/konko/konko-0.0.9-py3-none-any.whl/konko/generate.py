import os
import requests
import json 
from konko.utils.constants import TIMEOUT
from konko.utils.logs import BackendError
from typing import Any, Dict, List, Union, Iterator


def generate(prompt: List[str] = None, 
             models: List[str] = ['gpt-4', 'mpt-7b-instruct', 'llama-30b'],
             prompt_file: str = None,
             prompt_file_separator: str = "----",
             stream: bool = False, 
             optimize: Dict = {"cost" : 10} ) -> Union[List[Dict[str, Union[str, float, int]]],Iterator[Dict[str, Union[str, float, int]]]]:
    """
    This method generates a response for a user-specified prompt(s), set of models and an optimization constraint (cost,quality,latency) 
    Args:
        prompt: The input prompt(s) to generate a response for 
        models: The model(s) to evaluate from         
        prompt_file: Path to a file containing many prompts 
        prompt_file_separator: Seprator string 
        stream: If set to True this returns a handle to the stream object 
        optimize: The cost,quality, and latency constraints
    Examples: 
        >>> import konko
        >>> prompt = ['Summarize the Foundation by Isaac Asimov']
        >>> models = ['gpt-4', 'mpt-7b-instruct', 'llama-30b']
        >>> optimize = {'cost': 10, 'quality': 6}
        >>> konko.generate(prompt = prompt, models = models, optimize = optimize)
    """
    baseUrl = os.getenv('KONKO_URL')
    assert baseUrl is not None, "KONKO_URL must be set"
    token = os.getenv('KONKO_TOKEN')

    # TODO : Update to ->
    # from konko import evaluate 
    # model = evaluate(prompt, models, optimize)
    model = models[0].replace("/", "--")
    headers = {"Authorization": f"Bearer {token}"}
    response = []

    if prompt_file:
        with open(prompt_file, "r") as f:
            prompt = f.read().split(prompt_file_separator)
    params = [{"prompt": p, "use_prompt_format": use_format} 
            for p, use_format in zip(prompt, [True] * len(prompt))]   
    
    if stream:    
        path = '/stream' 
        url = f"{baseUrl}{model}{path}"   
        return generateStream(prompt = prompt,url = url, headers=headers)       
    else:
        path = '/batch'
        url = f"{baseUrl}{model}{path}"   
        return generateBatch(prompt = prompt,url = url, headers=headers)   
            

def generateBatch(prompt:List[str] = None,
                  url: str = None,
                  headers: Dict = None) -> List[Dict[str, Union[str, float, int]]]:
    
    #params = [{"prompt": p} for p in prompt]         
    params = [{"prompt": p, "use_prompt_format": use_format} 
              for p, use_format in zip(prompt, [True] * len(prompt))]   
     
    response = requests.post(url, 
                             headers=headers, 
                             json=params,
                             timeout=TIMEOUT)
    try:
        return response.json()
    except requests.JSONDecodeError as e:
        raise BackendError(
                f"Error decoding JSON from {url}. Text response: {response.text}",
                response=response,
            ) from e 

def generateStream(prompt:List[str] = None,
                   url: str = None,
                   headers: Dict = None) -> Iterator[Dict[str, Union[str, float, int]]]:    
    #params = [{"prompt": p} for p in prompt]         
    params = [{"prompt": p, "use_prompt_format": use_format} 
              for p, use_format in zip(prompt, [True] * len(prompt))]   
     
    response = requests.post(url, 
                             headers=headers, 
                             json=params,
                             timeout=TIMEOUT,
                             stream=True) 
    chunk = ""
    try:
        for chunk in response.iter_lines(chunk_size=None, decode_unicode=True):            
            chunk = chunk.strip()
            print("here",chunk)
            if not chunk:
                continue
            data = json.loads(chunk)
            if "error" in data:
                raise BackendError(data["error"], response=response)
            yield data
    except ConnectionError as e:
            raise BackendError(str(e) + "\n" + chunk, response=response) from e    

