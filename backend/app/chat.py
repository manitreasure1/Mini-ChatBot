
from openai import OpenAI
from app.config import Config

config = Config()  # type: ignore

client =OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=config.NEBUIS_API_KEY
)

def chatbot(message) -> str:
    completion = client.chat.completions.create(
        model='meta-llama/Meta-Llama-3.1-70B-Instruct',
        messages=[
            
            {
                'role':'system',
                'content':'You are an Ai bot, helping student\'s with any question'
            },
            {
                'role':'user',
                'content':f'{message}'
            },
            {
                'role':'assistant',
                'content':'Hello how can I assit you today, any question for me?'
            } 
        ],
        max_tokens=100,
        temperature=1,
        top_p=1,
        n=1,
        stream=False,
        stream_options=None,
        stop=None, 
        presence_penalty=0,
        frequency_penalty=0,
        logit_bias=None,
        logprobs=False,
        top_logprobs=None,
    )
    completion_to_json =completion.model_dump()
    return completion_to_json['choices'][0].message.content.strip()
    


