.PHONY:	rpm clean

VERSION ?= 3.4.6
BUILD_NUMBER ?= 1
SOURCE = zookeeper-$(VERSION).tar.gz
TOPDIR = /tmp/zookeeper-rpm
PWD = $(shell pwd)

rpm: $(SOURCE)
	@rpmbuild -v -bb \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)" \
			--define "_topdir $(TOPDIR)" \
			--define "version $(VERSION)" \
			--define "build_number $(BUILD_NUMBER)" \
			zookeeper.spec

$(SOURCE):
	@spectool \
			--define "version $(VERSION)" \
			-g zookeeper.spec

clean:
	@rm -rf $(TOPDIR) x86_64
	@rm -f $(SOURCE)

