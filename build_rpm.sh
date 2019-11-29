set -ex

whereiam=${.sh.file%/*}
root_tree=${whereiam%/*}

#rpmbuild -ba SPECS/prcredis.spec \
#  --undefine=_disable_source_fetch

echo $whereiam
echo $root_tree