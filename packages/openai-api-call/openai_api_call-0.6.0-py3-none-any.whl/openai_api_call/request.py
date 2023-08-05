# rewrite the request function

from typing import List, Dict, Union
import requests, json
import datetime, os, warnings
from urllib.parse import urlparse, urlunparse

url = None # Deprecated

# Read base_url from the environment
if os.environ.get('OPENAI_BASE_URL') is not None:
    base_url = os.environ.get("OPENAI_BASE_URL")
elif os.environ.get('OPENAI_API_BASE_URL') is not None:
    # adapt to the environment variable of chatgpt-web
    base_url = os.environ.get("OPENAI_API_BASE_URL")
else:
    base_url = "https://api.openai.com"

def is_valid_url(url: str) -> bool:
    """Check if the given URL is valid.

    Args:
        url (str): The URL to be checked.

    Returns:
        bool: True if the URL is valid; otherwise False.
    """
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

def normalize_url(url: str) -> str:
    """Normalize the given URL to a canonical form.

    Args:
        url (str): The URL to be normalized.

    Returns:
        str: The normalized URL.

    Examples:
        >>> normalize_url("http://api.example.com")
        'http://api.example.com'

        >>> normalize_url("api.example.com")
        'https://api.example.com'
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        # If no scheme is specified, default to https protocol.
        parsed_url = parsed_url._replace(scheme="https")
    return urlunparse(parsed_url).replace("///", "//")

def chat_completion( api_key:str
                   , messages:List[Dict]
                   , model:str
                   , chat_url:Union[str, None]=None
                   , function_call:Union[str, None]=None
                   , functions:Union[List[str], None]=None
                   , **options) -> Dict:
    """Chat completion API call
    
    Args:
        apikey (str): API key
        messages (List[Dict]): prompt message
        model (str): model to use
        chat_url (Union[str, None], optional): chat url. Defaults to None.
        function_call (Union[str, None], optional): function call. Defaults to None.
        functions (Union[List[str], None], optional): functions. Defaults to None.
        **options : options inherited from the `openai.ChatCompletion.create` function.
    
    Returns:
        Dict: API response
    """
    # request data
    payload = {
        "model": model,
        "messages": messages
    }
    if function_call is not None:
        payload.update({"function_call": function_call})
    if functions is not None:
        payload.update({"functions": functions})
    # inherit options
    payload.update(options)
    # request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }
    # initialize chat url
    if not chat_url:
        if url is not None: # deprecated warning
            warnings.warn("The `url` parameter is deprecated. Please use `base_url` instead.", DeprecationWarning)
            chat_url = url
        else:
            chat_url = os.path.join(base_url, "v1/chat/completions")
    
    chat_url = normalize_url(chat_url)
    # get response
    response = requests.post(chat_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json()

def usage_status(api_key:str, duration:int=99, url:Union[str, None]=None):
    """Get usage status
    
    Args:
        api_key (str): API key
        duration (int, optional): duration to check. Defaults to 99, which is the maximum duration.
        url (Union[str, None], optional): base url. Defaults to None.
    
    Returns:
        Tuple[float, float, List[float]]: total storage, total usage, daily costs
    """
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    if url is None: url = base_url
    url = normalize_url(base_url)
    # Get storage limit
    subscription_url = os.path.join(url, "v1/dashboard/billing/subscription")
    subscription_response = requests.get(subscription_url, headers=headers)
    if subscription_response.status_code == 200:
        data = subscription_response.json()
        total_storage = data.get("hard_limit_usd")
    else:
        raise Exception(subscription_response.text)
    # start_date
    today = datetime.datetime.now()
    start_date = (today - datetime.timedelta(days=duration)).strftime("%Y-%m-%d")
    # end_date = today + 1
    end_date = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    billing_url = os.path.join(url, f"v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}")
    billing_response = requests.get(billing_url, headers=headers)
    # Get usage status
    if billing_response.status_code == 200:
        data = billing_response.json()
        total_usage = data.get("total_usage") / 100
        daily_costs = data.get("daily_costs")
        return total_storage, total_usage, daily_costs
    else:
        raise Exception(billing_response.text)

def valid_models(api_key:str, gpt_only:bool=True, url:Union[str, None]=None):
    """Get valid models
    Request url: https://api.openai.com/v1/models

    Args:
        api_key (str): API key
        gpt_only (bool, optional): whether to return only GPT models. Defaults to True.
        url (Union[str, None], optional): base url. Defaults to None.

    Returns:
        List[str]: list of valid models
    """
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    if url is None: url = base_url
    models_url = normalize_url(os.path.join(url, "v1/models"))
    models_response = requests.get(models_url, headers=headers)
    if models_response.status_code == 200:
        data = models_response.json()
        # model_list = data.get("data")
        model_list = [model.get("id") for model in data.get("data")]
        return [model for model in model_list if "gpt" in model] if gpt_only else model_list
    else:
        raise Exception(models_response.text)
    