from copy import deepcopy

from production_config import \
    GLOBAL_VARS, MAC_LION_MINIS, MAC_SNOW_MINIS, \
    LINUX_VMS, LINUX_IXS, LINUX64_VMS, LINUX64_IXS, WIN32_IXS, WIN64_IXS, \
    WIN64_IXS, MOCK_DL120G7, \
    TRY_LINUX, TRY_LINUX_IXS, TRY_LINUX64, TRY_LINUX64_IXS, \
    TRY_MAC64, TRY_WIN32_IXS, TRY_WIN64_IXS, TRY_MOCK_DL120G7, \
    TRY_LION, \
    BUILDS_BEFORE_REBOOT, SYMBOL_SERVER_HOST

GLOBAL_VARS = deepcopy(GLOBAL_VARS)

SLAVES = {
    'linux':            LINUX_VMS + LINUX_IXS,
    'linux64':          LINUX64_VMS + LINUX64_IXS,
    'win32':            WIN32_IXS,
    'win64':            WIN64_IXS,
    'macosx':           [],
    'macosx64':         MAC_SNOW_MINIS,
    'macosx64-lion':    MAC_LION_MINIS,
    'mock':             MOCK_DL120G7
}

TRY_SLAVES = {
    'linux':       TRY_LINUX + TRY_LINUX_IXS,
    'linux64':     TRY_LINUX64 + TRY_LINUX64_IXS,
    'win32':       TRY_WIN32_IXS,
    'win64':       TRY_WIN64_IXS,
    'macosx64':    TRY_MAC64,
    'macosx64-lion': TRY_LION,
    'mock':        TRY_MOCK_DL120G7,
}

# Local overrides for default values
GLOBAL_VARS['download_base_url'] = 'http://ftp.mozilla.org/pub/mozilla.org/thunderbird-test'
GLOBAL_VARS['talos_masters'] = []
# List of unittest masters to notify of new builds to test,
# if a failure to notify the master should result in a warning,
# and sendchange retry count before give up
GLOBAL_VARS['unittest_masters'] = [
    ('buildbot-master36.build.mozilla.org:9301', True, 5),
]
GLOBAL_VARS['xulrunner_tinderbox_tree'] = None
GLOBAL_VARS['weekly_tinderbox_tree'] = 'MozillaTest'
GLOBAL_VARS['l10n_tinderbox_tree'] = 'MozillaTest'
GLOBAL_VARS['base_mirror_urls'] = ['http://hg.build.scl1.mozilla.com']
GLOBAL_VARS['base_bundle_urls'] = ['http://ftp.mozilla.org/pub/mozilla.org/thunderbird-test/bundles']
GLOBAL_VARS['aus2_user'] = 'tbirdbld'
GLOBAL_VARS['aus2_ssh_key'] = 'auspush'
GLOBAL_VARS['aus2_host'] = 'aus3-staging.mozilla.org'

# Local branch overrides
BRANCHES = {
    'comm-central': {
        'packaged_unittest_tinderbox_tree': 'Thunderbird',
        'tinderbox_tree': 'Thunderbird',
        'download_base_url': 'http://ftp.mozilla.org/pub/mozilla.org/thunderbird',
        'base_bundle_urls': ['http://ftp.mozilla.org/pub/mozilla.org/thunderbird/bundles'],
    },
    'comm-release': {
        'packaged_unittest_tinderbox_tree': 'MozillaTest',
        'tinderbox_tree': 'MozillaTest',
    },
    'comm-esr10': {
        'packaged_unittest_tinderbox_tree': 'MozillaTest',
        'tinderbox_tree': 'MozillaTest',
    },
    'comm-beta': {
        'packaged_unittest_tinderbox_tree': 'MozillaTest',
        'tinderbox_tree': 'MozillaTest',
    },
    'comm-aurora': {
        'packaged_unittest_tinderbox_tree': 'MozillaTest',
        'tinderbox_tree': 'MozillaTest',
    },
    'try-comm-central': {
        'tinderbox_tree': 'Try-Comm-Central',
        'packaged_unittest_tinderbox_tree': 'Try-Comm-Central',
        'download_base_url': 'http://ftp.mozilla.org/pub/mozilla.org/thunderbird/try-builds',
        'enable_mail_notifier': True,
        'notify_real_author': True,
        'package_url': 'http://ftp.mozilla.org/pub/mozilla.org/thunderbird/try-builds',
        'talos_masters': [],
        'platforms': {
            'win32': {
                'env': {
                    'SYMBOL_SERVER_HOST': 'build.mozilla.org',
                    'CVS_RSH': 'ssh',
                    'MOZ_OBJDIR': 'objdir-tb',
                    'TINDERBOX_OUTPUT': '1',
                    'MOZ_CRASHREPORTER_NO_REPORT': '1',
                    # Source server support, bug 506702
                    'PDBSTR_PATH': '/c/Program Files/Debugging Tools for Windows/srcsrv/pdbstr.exe',
                    'HG_SHARE_BASE_DIR': 'e:/builds/hg-shared',
                    'BINSCOPE': 'C:\Program Files\Microsoft\SDL BinScope\Binscope.exe',
                    'PATH': "${MOZILLABUILD}buildbotve\\scripts;${PATH}",
                }
            }
        }
    },
}

PLATFORM_VARS = {}

PROJECTS = {}
