import requests
import adapters
import os

def main():
    obj = getattr(adapters, "RutrackerProxy")(os.environ['LOGIN'], os.environ['PASSWORD'])
    print(obj.isLogin())

if __name__ == '__main__':
    main()
