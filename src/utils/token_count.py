import tiktoken



def token_count(messages, model="gpt-3.5-turbo"):  
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    # if model == "gpt-3.5-turbo" or model == "gpt" or model == "gpt-35-instant":
    #     # print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
    #     return token_count(messages, model="gpt-3.5-turbo-0301")
    # elif model == "gpt-4":
    #     # print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
    #     return token_count(messages, model="gpt-4-0314")

    # if "gpt-3.5" in model:
    #     # every message follows <|start|>{role/name}\n{content}<|end|>\n
    #     tokens_per_message = 4
    #     tokens_per_name = -1  # if there's a name, the role is omitted
    # elif "gpt-4" in model:
        # tokens_per_message = 3
        # tokens_per_name = 1
    # else:
    #     raise NotImplementedError(
    #         f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

    tokens_per_message = 4
    tokens_per_name = 1

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
