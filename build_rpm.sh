
# Exits on errors and logs commands with "+" before executing them.
set -ex

# Script full path and its directory full path.
SCRIPT=$(readlink -f "$0")
SCRIPTDIRPATH=$(dirname "$SCRIPT")

USER=prcuser #${1?Enter user account}
USER_GROUP=prcgroup #${2?Enter user group}

mkdir -p tempbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cp prcredis.spec tempbuild/SPECS




#rpmbuild -ba SPECS/prcredis.spec \
#  --undefine=_disable_source_fetch

echo $SCRIPTPATH
