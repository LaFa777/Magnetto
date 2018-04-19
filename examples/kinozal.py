from settings import trackers
from magnetto import KinozalApi
from grab import Grab

grab = Grab()
grab.setup(log_file="/tmp/magnetto/kinozal.html")
grab.setup(cookiefile="/tmp/magnetto/kinozal.cookie")

api = KinozalApi(grab)
api.authorization(trackers[KinozalApi]['login'], trackers[KinozalApi]['password'])

print(api.search("начало web", limit=1))
