
set -ex


SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")


#rpmbuild -ba SPECS/prcredis.spec \
#  --undefine=_disable_source_fetch

echo $SCRIPTPATH
