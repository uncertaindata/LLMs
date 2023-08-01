from dotenv import load_dotenv
import os
def funct():
    print('Hello World')
    load_dotenv()
    print(os.getenv("OPEN_API_KEY"))
if __name__ == '__main__':
    funct()
