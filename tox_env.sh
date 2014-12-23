#!/bin/bash -e
[ -z "${1}" ] && exit 1
TOX_DIR="${1}"

function hgme {
    repo="${1}"
    if [ ! -d "${TOX_DIR}/${repo}" ]; then
        hg clone https://hg.mozilla.org/build/${repo} "${TOX_DIR}/${repo}"
    else
        # this is equivalent to hg purge but doesn't require the hg purge plugin to be enabled
        hg status -un0 -R "${TOX_DIR}/${repo}" | xargs rm -rf
        hg pull -u -R "${TOX_DIR}/${repo}"
    fi
}

hgme tools
hgme buildbotcustom
hgme buildbot

hg -R "${TOX_DIR}/buildbot" checkout production-0.8
cd "${TOX_DIR}/buildbot/master" && python setup.py install
