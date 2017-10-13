#!/bin/bash

standalone_server_jar='bin/selenium-server-standalone-3.6.0.jar'
log='selenium_server.log'
/usr/bin/java -jar "${standalone_server_jar}" -port 4555 -log "${log}" -timeout 86400 >"${log}" 2>"${log}"
