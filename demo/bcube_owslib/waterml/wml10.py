from __future__ import (absolute_import, division, print_function)

from bcube_owslib.waterml.wml import SitesResponse, TimeSeriesResponse, VariablesResponse, namespaces
from bcube_owslib.etree import etree

def ns(namespace):
    return namespaces.get(namespace)

class WaterML_1_0(object):
    def __init__(self, element):

        if isinstance(element, str) or isinstance(element, unicode):
            self._root = etree.fromstring(str(element))
        else:
            self._root = element

        if hasattr(self._root, 'getroot'):
            self._root = self._root.getroot()

        self._ns = 'wml1.0'

    @property
    def response(self):
        try:
            if self._root.tag == str(ns(self._ns) + 'variablesResponse'):
                return VariablesResponse(self._root, self._ns)
            elif self._root.tag == str(ns(self._ns) + 'timeSeriesResponse'):
                return TimeSeriesResponse(self._root, self._ns)
            elif self._root.tag == str(ns(self._ns) + 'sitesResponse'):
                return SitesResponse(self._root, self._ns)
        except:
            raise

        raise ValueError('Unable to determine response type from xml')
