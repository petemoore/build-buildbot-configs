c = BuildmasterConfig = {}
c['slavePortnum'] = 9010

from buildbot.status.html import WebStatus
c['status'] = [
        WebStatus(http_port=8010, allowForce=True)
]

c['buildbotURL'] = 'http://preproduction-master.srv.releng.scl3.mozilla.com:8010/'

from buildbot import manhole
c['manhole'] = manhole.PasswordManhole("tcp:1235:interface=127.0.0.1", "cltbld", "password")

from config import BRANCHES, SLAVES, PROJECTS
from thunderbird_config import BRANCHES as THUNDERBIRD_BRANCHES
ACTIVE_BRANCHES = BRANCHES.keys()
ACTIVE_THUNDERBIRD_BRANCHES = THUNDERBIRD_BRANCHES.keys()
ACTIVE_PROJECTS = [p for p in PROJECTS.keys() if p != 'fuzzing']
ACTIVE_RELEASE_BRANCHES = []
ACTIVE_THUNDERBIRD_RELEASE_BRANCHES = []
ACTIVE_MOBILE_RELEASE_BRANCHES = []
ACTIVE_B2G_BRANCHES = []

ENABLE_RELEASES = False

QUEUEDIR = "/dev/shm/queue"
