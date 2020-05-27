version = $(shell cat VERSION)
git_hash = $(shell git rev-parse --short HEAD)

.PHONY: build package clean

all: clean build package

build:
	cp info.plist.template info.plist
	sed -i -e "s/\$${VERSION}/${version}/" info.plist

package:
	mkdir dist
	zip -r dist/alfred-tx-translate-${version}-${git_hash}.alfredworkflow . -x \*.git\*  -x .idea\* -x token -x tags -x dist\* -x \*.swp -x info.plist.template -x \*.DS_Store\* -x \*.pyc\* -x \*snapshot\*

clean:
	rm -rf dist info.plist
