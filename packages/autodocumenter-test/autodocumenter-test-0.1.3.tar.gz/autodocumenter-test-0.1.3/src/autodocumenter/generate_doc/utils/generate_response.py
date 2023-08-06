import os
import openai
from openlimit import ChatRateLimiter

openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_response_sync(
    messages,
    model="gpt-3.5-turbo",
    temperature: float = 0.01,
    timeout=120,
    rate_limit=False,
    request_limit=500,
    token_limit=50000,
    stop=None,
):
    chat_params = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "timeout": timeout,
        "stop": stop,
    }
    if rate_limit:
        rate_limiter = ChatRateLimiter(
            request_limit=request_limit, token_limit=token_limit
        )
        with rate_limiter.limit(**chat_params):
            response = openai.ChatCompletion.create(**chat_params)
    else:
        response = openai.ChatCompletion.create(**chat_params)

    response = response["choices"][0]["message"]["content"]
    response = response.replace('"""', "").strip()
    # response = m2r2.convert(response)
    return response


async def generate_response_async(
    messages,
    model="gpt-3.5-turbo",
    temperature: float = 0.01,
    timeout=30,
    rate_limit=False,
    request_limit=500,
    token_limit=50000,
    stop=None,
):
    chat_params = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "timeout": timeout,
        "stop": stop,
    }
    if rate_limit:
        rate_limiter = ChatRateLimiter(
            request_limit=request_limit, token_limit=token_limit
        )
        async with rate_limiter.limit(**chat_params):
            response = await openai.ChatCompletion.acreate(**chat_params)
    else:
        response = await openai.ChatCompletion.acreate(**chat_params)

    response = response["choices"][0]["message"]["content"]
    response = response.replace('"""', "").strip()
    # response = m2r2.convert(response)
    return response
