CXX ?= $(shell command -v clang++ >/dev/null 2>&1 && echo clang++ || echo g++)
CXXFLAGS ?= -std=c++17 -Wall -Wextra -O2 -Iinclude

GTEST_PREFIX ?= $(shell command -v brew >/dev/null 2>&1 && brew --prefix googletest 2>/dev/null)
ifneq ($(GTEST_PREFIX),)
    GTEST_CXXFLAGS = -I$(GTEST_PREFIX)/include
    GTEST_LDFLAGS = -L$(GTEST_PREFIX)/lib -lgtest -lgtest_main -pthread
else
    GTEST_CXXFLAGS = $(shell pkg-config --cflags gtest_main 2>/dev/null)
    GTEST_LDFLAGS = $(shell pkg-config --libs gtest_main 2>/dev/null || echo "-lgtest -lgtest_main -pthread")
endif

SRCS = $(wildcard src/*.cpp) tests/test_expense_manager.cpp
TARGET = test_runner

.PHONY: all run build test setup clean

all: run

build: $(TARGET)

$(TARGET): $(SRCS)
	@$(CXX) $(CXXFLAGS) $(GTEST_CXXFLAGS) -o $(TARGET) $(SRCS) $(GTEST_LDFLAGS)

run: build
	@./$(TARGET)

test: run

setup:
	@./setup.sh

clean:
	@rm -f $(TARGET) *.o

