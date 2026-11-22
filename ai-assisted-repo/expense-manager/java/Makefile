JAVA_HOME_CANDIDATE := $(shell find $(HOME)/.corretto -maxdepth 3 -type d -name "Home" 2>/dev/null | head -n 1)
ifneq ($(JAVA_HOME_CANDIDATE),)
    export JAVA_HOME := $(JAVA_HOME_CANDIDATE)
    export PATH := $(JAVA_HOME)/bin:$(PATH)
endif

JAVAC ?= javac
JAVA ?= java
JUNIT_JAR = lib/junit-platform-console-standalone-1.10.2.jar
BIN = bin
SRCS = $(shell find src -name "*.java")
TEST_SRCS = $(shell find tests -name "*.java")

.PHONY: all run test setup clean compile

all: test

run: test

compile:
	@mkdir -p $(BIN)
	@$(JAVAC) -cp "$(JUNIT_JAR)" -d $(BIN) $(SRCS) $(TEST_SRCS)

test: compile
	@$(JAVA) -jar $(JUNIT_JAR) execute --class-path $(BIN) --scan-class-path --disable-banner --details=summary

setup:
	@./setup.sh

clean:
	@rm -rf $(BIN)

