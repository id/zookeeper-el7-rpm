.PHONY:	rpm clean

VERSION ?= 3.4.9
RELEASE ?= 2
SOURCE = zookeeper-$(VERSION).tar.gz
TOPDIR = /tmp/zookeeper-rpm
PWD = $(shell pwd)
URL = $(shell curl -s https://www.apache.org/dyn/closer.cgi/zookeeper/zookeeper-$(VERSION)/zookeeper-$(VERSION).tar.gz?asjson=1 | python -c 'import sys,json; data=json.load(sys.stdin); print data["preferred"] + data["path_info"]')

rpm: $(SOURCE)
	@rpmbuild -v -bb \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)" \
			--define "_topdir $(TOPDIR)" \
			--define "zk_version $(VERSION)" \
			--define "zk_release $(RELEASE)" \
			zookeeper.spec

source: $(SOURCE)

$(SOURCE): KEYS $(SOURCE).asc
	@wget -q $(URL)
	gpg --verify $(SOURCE).asc $(SOURCE)

clean:
	@rm -rf $(TOPDIR) x86_64
	@rm -f $(SOURCE)

$(SOURCE).asc:
	@wget -q https://dist.apache.org/repos/dist/release/zookeeper/zookeeper-$(VERSION)/$(SOURCE).asc

KEYS:
	@wget -q https://dist.apache.org/repos/dist/release/zookeeper/KEYS
	gpg --import KEYS
