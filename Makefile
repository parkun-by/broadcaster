SHELL:=/bin/bash

NAME   := skaborik/broadcaster
TAG    := $$(git describe --tags --abbrev=0)
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest

build:
	@docker build -t ${IMG} .
	@docker tag ${IMG} ${LATEST}

push:
	@docker push ${NAME}
