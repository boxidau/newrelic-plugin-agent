"""
LM Sensors Support
"""
import logging
import re

from newrelic_plugin_agent.plugins import base

LOGGER = logging.getLogger(__name__)
PATTERN = re.compile(r'^(Core [\d]{1,3}):.*?'
                      '([\d]{1,3}\.[\d]).*?'
                      '([\d]{1,3}\.[\d]).*?'
                      '([\d]{1,3}\.[\d])')

class Sensors(base.SubprocessStatsPlugin):

    GUID = 'com.meetme.newrelic_sensors_agent'
    def error_message(self):
        pass

    def add_datapoints(self, stats):
        """Add all of the data points for a node

        :param str stats: The stats content from Apache as a string

        """
        high = 50.0
        critical = 100.0
        temps = []
        for line in stats.split('\n'):
            temp_line = re.split(PATTERN, line)
            if len(temp_line) == 6:
              high = float(temp_line[3])
              critical = float(temp_line[4])
              temp = float(temp_line[2])
              temps.append(temp)
              self.add_gauge_value(temp_line[1], 'C', temp)
        self.add_gauge_value('High', 'C', high)
        self.add_gauge_value('Critical', 'C', critical)
