set -ex
rpmbuild -ba SPECS/redis.spec --undefine=_disable_source_fetch