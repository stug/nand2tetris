#!/bin/sh
cd `dirname $0`
java -classpath "${CLASSPATH}:bin/classes" TextComparer $*
