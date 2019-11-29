set -ex
mkdir BUILD &2>/dev/null

rpmbuild -ba SPECS/redis.spec \
  --undefine=_disable_source_fetch \
  --buildroot BUILD