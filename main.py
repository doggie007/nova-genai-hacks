from langchain_openai import ChatOpenAI

CARTESIA_API_KEY="34bccfa1-25f3-4250-b24b-41db9dc48b84"
TEAM_API_KEY="sk-1-nnzryEbytTnAqTcIyH7Q"
PROXY_ENDPOINT="https://nova-litellm-proxy.onrender.com"


# llm = ChatOpenAI(
#     openai_api_key="sk-1-nnzryEbytTnAqTcIyH7Q",
#     openai_api_base="https://nova-litellm-proxy.onrender.com",
#     model="gpt-4o"
# )
#
# template = """Generate a kids story based on this prompt: {query}"""
#
# prompt = template.format(query='My sons dad was in jail. Write a story to make sure he doesnt end like him')
#
# response = llm.invoke(prompt)
#
# print(response.content)
#


from openai import OpenAI
import requests

def example_image_generation():
    """
    Examples of image generation from the proxy
    """
    client = OpenAI(
        api_key=TEAM_API_KEY,
        base_url=PROXY_ENDPOINT
    )

    image = client.images.generate(
        prompt="donald trump having full control over america and full of power on top of the world",
        model="dall-e-3",
    )

    print(image)
    url = image.data[0].url
    open("example_image_generation.png", "wb").write(requests.get(url).content)

if __name__ == "__main__":
    example_image_generation()
