import aiohttp
import asyncio
import json

async def stream_api_call(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as response:
            if response.status == 200:
                async for chunk in response.content.iter_any():
                    _token = chunk.decode()
                    _token = _token.replace("data: ", "")
                    token = {}
                    if "[DONE]" not in _token:
                        _token = json.loads(_token)['meta_info']['output_top_logprobs'][-1]
                        token['text'] = _token[0][2]
                        token['logprobs'] = [{"index": t[1], "logprob": t[0], "decoded": t[2]} for t in _token]
                        yield token
                    else:
                        yield _token

async def main():
    api_url = "http://127.0.0.1:16746/generate"
    params = {
    "text": "Once upon a time,",
    "sampling_params": {
      "max_new_tokens": 200,
      "temperature": 0,
      "top_p": 1, 
      "top_k": 1,
    },
    "stream": True,
    "return_logprob": True,
    "return_text_in_logprobs": True,
    "top_logprobs_num": 3
  }
    async for data in stream_api_call(api_url, params):
        print(data)

if __name__ == "__main__":
    asyncio.run(main())