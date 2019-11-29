# Exits on errors and logs commands with "+" before executing them.
set -ex

# Script full path and its directory full path.
SCRIPT=$(readlink -f "$0")
SCRIPTDIRPATH=$(dirname "$SCRIPT")

rpmbuild -ba SPECS/redis.spec \
  --undefine=_disable_source_fetch \
  --define "_topdir $SCRIPTDIRPATH"
