import requests
import trackers
import os

def main():
    obj = getattr(trackers.apis, "Rutracker")(os.environ['LOGIN'], os.environ['PASSWORD'])
    print(obj.is_login())

if __name__ == '__main__':
    main()
