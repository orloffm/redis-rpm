# This file builds our core PRC Redis package.
# It downloads sources and builds the RPM that
# installs Redis and makes necessary changes to the machine.

# Exit on errors and output all commands with "+ " before running.
set -ex

# Script full path and its directory full path.
SCRIPT=$(readlink -f "$0")
SCRIPTDIR=$(dirname "$SCRIPT")

# Redis locations
REDIS_VERSION=5.0.7
REDIS_FILE=redis-$REDIS_VERSION
REDIS_FILE_WEXT=$REDIS_FILE.tar.gz
REDIS_URL=http://download.redis.io/releases/$REDIS_FILE_WEXT

# This subdirectory is where the RPM magic happens.
RPM_TOPDIR=$SCRIPTDIR/rpmbuild
RPM_SOURCES=$RPM_TOPDIR/SOURCES

# But first we download the sources and build them ourselves.
# We'll do that in this folder.
STAGING_DIR=$SCRIPTDIR/staging
REDIS_DIR=$STAGING_DIR/$REDIS_FILE
mkdir -p $STAGING_DIR
cd $STAGING_DIR

# Download the file if doesn't exist.
if [ ! -e $REDIS_FILE_WEXT ]; then
  wget $REDIS_URL
fi
 
# Extract and build if not built previously.
REDIS_OUTPUT=$STAGING_DIR/redis-binaries
if [ ! -d $REDIS_FILE ]; then
  tar -xvzf $REDIS_FILE_WEXT > /dev/null
  cd $REDIS_DIR
  
  # Compile silently.
  make > /dev/null

  # Copy binaries to "output" subfolder.
  make install PREFIX=$REDIS_OUTPUT > /dev/null
fi

# Prepare the intermediate .tar.gz with binaries.
# We do that to not reinvent the bike. Let RPM
# do its thing and manage the files. Otherwise
# this file would get polluted with variables
# and paths it doesn't need to know about.
INTERMEDIATE_TARGZ=$RPM_TOPDIR/SOURCES/redis-binaries.tar.gz
mkdir -p $RPM_TOPDIR/SOURCES
if [ ! -e $INTERMEDIATE_TARGZ ]; then
  cd $REDIS_OUTPUT
  tar -cvzf $INTERMEDIATE_TARGZ * > /dev/null
fi

# Default config to SOURCES
REDIS_CONF=$REDIS_DIR/redis.conf
if [ ! -e $RPM_SOURCES/redis.conf ]; then
  cp $REDIS_CONF $RPM_SOURCES
fi

cd $SCRIPTDIR

# Build the spec.
rpmbuild -bb $RPM_TOPDIR/SPECS/redis-prc-core.spec \
  --define "_topdir $RPM_TOPDIR" \
  -v

# And now copy the result here.
cp -l rpmbuild/RPMS/x86_64/*.rpm .
