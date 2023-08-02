import os
import openai
def is_api_key_valid():
    # print('current env variable', os.getenv('OPENAI_API_KEY'))
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt="This is a test.",
            max_tokens=5
        )
    except:
        return False
    else:
        return True

if __name__ == '__main__':    
    key = 'sk-YIpChAlgzCQOHk2D7MjT3BlbkFJpO5W3dOAqJ38ZU6y0xh9'
    os.environ['OPENAI_API_KEY'] = key

    openai.api_key = os.getenv('OPENAI_API_KEY')

    print(is_api_key_valid())

