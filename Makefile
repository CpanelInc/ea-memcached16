OBS_PROJECT := EA4
OBS_PACKAGE := ea-memcached16
DISABLE_BUILD := arch=i586 repository=CentOS_6.5_standard repository=CentOS_7
include $(EATOOLS_BUILD_DIR)obs.mk
