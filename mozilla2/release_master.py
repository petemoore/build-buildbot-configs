from buildbot.changes.pb import PBChangeSource
from buildbot.scheduler import Scheduler, Dependent

import buildbotcustom.misc
import buildbotcustom.process.factory
reload(buildbotcustom.misc)
reload(buildbotcustom.process.factory)

from buildbotcustom.misc import get_l10n_repositories, isHgPollerTriggered
from buildbotcustom.process.factory import StagingRepositorySetupFactory, \
  ReleaseTaggingFactory, SingleSourceFactory, MercurialBuildFactory, \
  ReleaseUpdatesFactory, UpdateVerifyFactory, ReleaseFinalVerification

# this is where all of our important configuration is stored. build number,
# version number, sign-off revisions, etc.
import release_config
reload(release_config)
from release_config import *

# for the 'build' step we use many of the same vars as the nightlies do.
# we import those so we don't have to duplicate them in release_config
import config as nightly_config
reload(nightly_config)

builders = []
schedulers = []
change_source = []
status = []

##### Change sources and Schedulers
change_source.append(PBChangeSource())

tag_scheduler = Scheduler(
    name='tag',
    branch='mozilla-central',
    treeStableTimer=0,
    builderNames=['tag'],
    fileIsImportant=lambda c: not isHgPollerTriggered(c, nightly_config.HGURL)
)
build_scheduler = Dependent(
    name='build',
    upstream=tag_scheduler,
    builderNames=['source', 'linux_build', 'win32_build', 'macosx_build']
)

# Purposely, there is not a Scheduler for ReleaseFinalVerification
# This is a step run very shortly before release, and is triggered manually
# from the waterfall

schedulers.append(tag_scheduler)
schedulers.append(build_scheduler)

##### Builders
repositories = {
    mozillaCentral: {
        'revision': mozillaCentralRevision,
        'relbranchOverride': relbranchOverride,
        'bumpFiles': ['config/milestone.txt', 'browser/config/version.txt',
                      'browser/app/module.ver']
    }
}
l10n_repos = get_l10n_repositories(l10nRevisionFile, l10nCentral,
                                   relbranchOverride)
repositories.update(l10n_repos)

tag_factory = ReleaseTaggingFactory(
    repositories=repositories,
    buildToolsRepo=buildTools,
    productName=productName,
    appName=appName,
    appVersion=appVersion,
    milestone=milestone,
    baseTag=baseTag,
    buildNumber=buildNumber,
    hgUsername=hgUsername,
    hgSshKey=hgSshKey
)

builders.append({
    'name': 'tag',
    'slavenames': ['moz2-linux-slave1', 'moz2-linux-slave02',
                   'moz2-linux-slave03', 'moz2-linux-slave05',
                   'moz2-linux-slave06', 'moz2-linux-slave11',
                   'moz2-linux-slave12', 'moz2-linux-slave13',
                   'moz2-linux-slave14', 'moz2-linux-slave15',
                   'moz2-linux-slave16'],
    'category': 'release',
    'builddir': 'tag',
    'factory': tag_factory
})


source_factory = SingleSourceFactory(
    repository=mozillaCentral,
    productName=productName,
    appVersion=appVersion,
    baseTag=baseTag
)

builders.append({
    'name': 'source',
    'slavenames': ['moz2-linux-slave1', 'moz2-linux-slave02',
                   'moz2-linux-slave03', 'moz2-linux-slave05',
                   'moz2-linux-slave06', 'moz2-linux-slave11',
                   'moz2-linux-slave12', 'moz2-linux-slave13',
                   'moz2-linux-slave14', 'moz2-linux-slave15',
                   'moz2-linux-slave16'],
    'category': 'release',
    'builddir': 'source',
    'factory': source_factory
})


for platform in releasePlatforms:
    # shorthand
    pf = nightly_config.BRANCHES['mozilla-central']['platforms'][platform]

    build_factory = MercurialBuildFactory(
        env=pf['env'],
        objdir=pf['platform_objdir'],
        platform=platform + '-release',
        branch='mozilla-central',
        sourceRepo=mozillaCentral.replace('mozilla-central', ''),
        configRepo=nightly_config.CONFIG_REPO_URL,
        configSubDir=nightly_config.CONFIG_SUBDIR,
        profiledBuild=pf['profiled_build'],
        buildRevision='%s_RELEASE' % baseTag,
        stageServer=nightly_config.STAGE_SERVER,
        stageUsername=nightly_config.STAGE_USERNAME,
        stageGroup=nightly_config.STAGE_GROUP,
        stageSshKey=nightly_config.STAGE_SSH_KEY,
        stageBasePath=nightly_config.STAGE_BASE_PATH,
        codesighs=False,
        uploadPackages=False,
        uploadSymbols=True,
        createSnippet=False,
        doCleanup=True # this will clean-up the mac build dirs, but not delete
                       # the entire thing
    )

    builders.append({
        'name': '%s_build' % platform,
        'slavenames': pf['slaves'],
        'category': 'release',
        'builddir': '%s_build' % platform,
        'factory': build_factory
    })


updates_factory = ReleaseUpdatesFactory(
    cvsroot=cvsroot,
    patcherToolsTag=patcherToolsTag,
    mozillaCentral=mozillaCentral,
    buildTools=buildTools,
    patcherConfig=patcherConfig,
    baseTag=baseTag,
    appName=appName,
    productName=productName,
    appVersion=appVersion,
    oldVersion=oldVersion,
    buildNumber=buildNumber,
    ftpServer=ftpServer,
    bouncerServer=bouncerServer,
    stagingServer=stagingServer,
    useBetaChannel=useBetaChannel,
    stageUsername=nightly_config.STAGE_USERNAME,
    stageSshKey=nightly_config.STAGE_SSH_KEY,
    ausUser=nightly_config.AUS2_USER,
    ausHost=nightly_config.AUS2_HOST
)

builders.append({
    'name': 'updates',
    'slavenames': ['moz2-linux-slave1', 'moz2-linux-slave02',
                   'moz2-linux-slave03', 'moz2-linux-slave05',
                   'moz2-linux-slave06', 'moz2-linux-slave11',
                   'moz2-linux-slave12', 'moz2-linux-slave13',
                   'moz2-linux-slave14', 'moz2-linux-slave15',
                   'moz2-linux-slave16'],
    'category': 'release',
    'builddir': 'updates',
    'factory': updates_factory
})


for platform in releasePlatforms:
    pf = nightly_config.BRANCHES['mozilla-central']['platforms'][platform]

    platformVerifyConfig = None
    if platform == 'linux':
        platformVerifyConfig = linuxVerifyConfig
    if platform == 'macosx':
        platformVerifyConfig = macVerifyConfig
    if platform == 'win32':
        platformVerifyConfig = win32VerifyConfig

    update_verify_factory = UpdateVerifyFactory(
        mozillaCentral=mozillaCentral,
        buildTools=buildTools,
        cvsroot=cvsroot,
        patcherToolsTag=patcherToolsTag,
        hgUsername=hgUsername,
        baseTag=oldBaseTag,
        appName=appName,
        platform=platform,
        productName=productName,
        oldVersion=oldVersion,
        oldBuildNumber=oldBuildNumber,
        version=appVersion,
        buildNumber=buildNumber,
        ausServerUrl=ausServerUrl,
        stagingServer=stagingServer,
        verifyConfig=platformVerifyConfig,
        hgSshKey=hgSshKey
    )

    builders.append({
        'name': '%s_update_verify' % platform,
        'slavenames': pf['slaves'],
        'category': 'release',
        'builddir': '%s_update_verify' % platform,
        'factory': update_verify_factory
    })


final_verification_factory = ReleaseFinalVerification(
    buildTools=buildTools,
    linuxConfig=linuxVerifyConfig,
    macConfig=macVerifyConfig,
    win32Config=win32VerifyConfig
)

builders.append({
    'name': 'final_verification',
    'slavenames': ['moz2-linux-slave1', 'moz2-linux-slave02',
                   'moz2-linux-slave03', 'moz2-linux-slave05',
                   'moz2-linux-slave06', 'moz2-linux-slave11',
                   'moz2-linux-slave12', 'moz2-linux-slave13',
                   'moz2-linux-slave14', 'moz2-linux-slave15',
                   'moz2-linux-slave16'],
    'category': 'release',
    'builddir': 'final_verification',
    'factory': final_verification_factory
})
