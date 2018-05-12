import sys
sys.path.append('..')
import settings
from settings import trackers
from magnetto import RutrackerApi, Limit, Category
from grab import Grab


grab = Grab()
grab.setup(proxy=settings.PROXY, proxy_userpwd=settings.PROXY_USERPWD,
           proxy_type=settings.PROXY_TYPE)

grab.setup(log_file=settings.LOG_DIR + "/rutracker.html")
grab.setup(cookiefile=settings.COOCKIE_DIR + "/rutracker.coockie")

api = RutrackerApi(grab)
api.authorization(trackers[RutrackerApi]['login'],
                  trackers[RutrackerApi]['password'])

print(api.search(query="начало", filters=[Limit(1), Category.FILMS]))

print(api.get_last_request_data())
