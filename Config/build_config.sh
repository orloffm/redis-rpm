# This file builds our PRC Redis Configs package.
# The Configs package only places the configs in place
# if the basic core package is installed.

# Exit on errors and output all commands with "+ " before running.
set -ex

# Script full path and its directory full path.
SCRIPT=$(readlink -f "$0")
SCRIPTDIR=$(dirname "$SCRIPT")

# This subdirectory is where the RPM magic happens.
RPM_TOPDIR=$SCRIPTDIR/rpmbuild
RPM_SOURCES=$RPM_TOPDIR/SOURCES

cd $SCRIPTDIR

# Build the spec.
rpmbuild -bb $RPM_TOPDIR/SPECS/redis-prc-config.spec \
  --define "_topdir $RPM_TOPDIR" \
  -v

# And now copy the result here.
rm -f *.rpm
cp -l rpmbuild/RPMS/x86_64/*.rpm .

# Write contents of RPM for info.
rpm -qlp *.rpm
