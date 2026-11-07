# Disable auto partition selection - partition table is set in sdkconfig.defaults
set(EDGE_AGENT_PROJECT_LOG_PREFIX "[edge_agent]")
message(STATUS "${EDGE_AGENT_PROJECT_LOG_PREFIX} Using partition table from sdkconfig.defaults")
