.PHONY:	rpm clean

VERSION ?= 3.5.6
BUILD_NUMBER ?= 1
SOURCE = zookeeper-$(VERSION)-bin.tar.gz
TOPDIR = /tmp/zookeeper-rpm
PWD = $(shell pwd)
URL = $(shell curl -s https://www.apache.org/dyn/closer.cgi/zookeeper/zookeeper-$(VERSION)/apache-zookeeper-$(VERSION)-bin.tar.gz?asjson=1 | python -c 'import sys,json; data=json.load(sys.stdin); print data["preferred"] + data["path_info"]')

rpm: $(SOURCE)
	@rpmbuild -v -bb \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)/RPMS" \
			--define "_topdir $(TOPDIR)" \
			--define "version $(VERSION)" \
			--define "build_number $(BUILD_NUMBER)" \
			zookeeper.spec

source: $(SOURCE)

$(SOURCE): KEYS $(SOURCE).asc
	@wget --output-document=$(SOURCE) -q $(URL)
	gpg --verify $(SOURCE).asc $(SOURCE)

clean:
	@rm -rf $(TOPDIR) x86_64
	@rm -f $(SOURCE)
	@rm -f $(SOURCE).asc

$(SOURCE).asc:
	@wget --output-document=$(SOURCE).asc -q https://dist.apache.org/repos/dist/release/zookeeper/zookeeper-$(VERSION)/apache-$(SOURCE).asc

KEYS:
	@wget -q https://dist.apache.org/repos/dist/release/zookeeper/KEYS
	gpg --import KEYS
