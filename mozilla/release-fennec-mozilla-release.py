releaseConfig = {}
releaseConfig['disable_tinderbox_mail'] = True

# Release Notification
releaseConfig['AllRecipients']       = ['release@mozilla.com','akeybl@mozilla.com','Callek@gmail.com']
releaseConfig['ImportantRecipients'] = ['release-drivers@mozilla.org',]
releaseConfig['releaseTemplates']    = 'release_templates'
releaseConfig['messagePrefix']       = '[release] '

# Basic product configuration
#  Names for the product/files
releaseConfig['productName']         = 'fennec'
releaseConfig['appName']             = 'mobile'
releaseConfig['binaryName']          = releaseConfig['productName'].capitalize()
releaseConfig['oldBinaryName']       = releaseConfig['binaryName']
releaseConfig['relbranchPrefix']     = 'MOBILE'
#  Current version info
releaseConfig['version']             = '10.0'
releaseConfig['appVersion']          = releaseConfig['version']
releaseConfig['milestone']           = releaseConfig['version']
releaseConfig['buildNumber']         = 1
releaseConfig['baseTag']             = 'FENNEC_10_0'
#  Old version info
releaseConfig['oldVersion']          = '9.0'
releaseConfig['oldAppVersion']       = releaseConfig['oldVersion']
releaseConfig['oldBuildNumber']      = 1
releaseConfig['oldBaseTag']          = 'FENNEC_9_0'
#  Next (nightly) version info
releaseConfig['nextAppVersion']      = releaseConfig['version']
releaseConfig['nextMilestone']       = releaseConfig['version']
#  Repository configuration, for tagging
releaseConfig['sourceRepositories']  = {
    'mobile': {
        'name': 'mozilla-release',
        'path': 'releases/mozilla-release',
        'revision': 'acddb6b6a01c',
        'relbranch': None,
        'bumpFiles': {
            'mobile/confvars.sh': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
            'browser/config/version.txt': {
                'version': releaseConfig['appVersion'],
                'nextVersion': releaseConfig['nextAppVersion']
            },
            'config/milestone.txt': {
                'version': releaseConfig['milestone'],
                'nextVersion': releaseConfig['nextMilestone']
            },
            'js/src/config/milestone.txt': {
                'version': releaseConfig['milestone'],
                'nextVersion': releaseConfig['nextMilestone']
            },
        }
    }
}
#  L10n repositories
releaseConfig['l10nRelbranch']       = None
releaseConfig['l10nRepoPath']        = 'releases/l10n/mozilla-release'
releaseConfig['l10nRevisionFile']    = 'l10n-changesets_mobile-release.json'
releaseConfig['l10nJsonFile']        = releaseConfig['l10nRevisionFile']
#  Support repositories
releaseConfig['otherReposToTag']     = {
    'build/compare-locales': 'RELEASE_AUTOMATION',
    'build/buildbot': 'production-0.8',
    'build/partner-repacks': 'default',
    'build/mozharness': 'default',
}

# Platform configuration
releaseConfig['enUSPlatforms']        = ('linux-android', 'linux-mobile', 'macosx-mobile',
                                         'win32-mobile')
releaseConfig['notifyPlatforms']      = ('linux-android',)
releaseConfig['signedPlatforms']      = ('linux-android',)
releaseConfig['unittestPlatforms']    = ()
releaseConfig['talosTestPlatforms']   = ()
releaseConfig['enableUnittests']      = True

# L10n configuration
releaseConfig['l10nPlatforms']       = ('linux-mobile', 'macosx-mobile', 'win32-mobile')
releaseConfig['l10nChunks']          = 6
releaseConfig['mergeLocales']        = True
releaseConfig['enableMultiLocale']   = True

# Mercurial account
releaseConfig['hgUsername']          = 'ffxbld'
releaseConfig['hgSshKey']            = '~cltbld/.ssh/ffxbld_dsa'

# Update-specific configuration
releaseConfig['ftpServer']           = 'ftp.mozilla.org'
releaseConfig['stagingServer']       = 'stage.mozilla.org'
releaseConfig['ausServerUrl']        = 'https://aus2.mozilla.org'
releaseConfig['ausHost']             = 'aus2-staging.mozilla.org'
releaseConfig['ausUser']             = 'cltbld'
releaseConfig['ausSshKey']           = 'cltbld_dsa'

# Partner repack configuration
releaseConfig['doPartnerRepacks']       = True
releaseConfig['partnersRepoPath']       = 'build/partner-repacks'
releaseConfig['partnerRepackPlatforms'] = ()

# mozconfigs
releaseConfig['mozconfigs']          = {
    'linux-android': 'mobile/config/mozconfigs/android/release',
    'linux-mobile': 'mobile/config/mozconfigs/linux-desktop/release',
    'macosx-mobile': 'mobile/config/mozconfigs/macosx-desktop/release',
    'win32-mobile': 'mobile/config/mozconfigs/win32-desktop/release',
}

# Misc configuration
releaseConfig['enable_repo_setup']       = False

# Fennec specific
releaseConfig['usePrettyNames']           = False
releaseConfig['disableBouncerEntries']    = True
releaseConfig['disableStandaloneRepacks'] = True
releaseConfig['disableL10nVerification']  = True
releaseConfig['disablePermissionCheck']   = True
releaseConfig['disableVirusCheck']        = True
releaseConfig['disablePushToMirrors']     = True

releaseConfig['mozharness_config'] = {
    'platforms': {
        'linux-android':
            'multi_locale/release_mozilla-release_linux-android.json',
    },
    'multilocaleOptions': [
        '--tag-override=%s_RELEASE' % releaseConfig['baseTag'],
        '--only-pull-locale-source',
        '--only-add-locales',
        '--only-package-multi',
    ]
}
releaseConfig['enableSigningAtBuildTime'] = False
releaseConfig['enablePartialMarsAtBuildTime'] = False
