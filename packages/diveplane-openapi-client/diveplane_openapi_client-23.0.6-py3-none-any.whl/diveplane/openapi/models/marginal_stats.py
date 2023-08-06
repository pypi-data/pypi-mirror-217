# coding: utf-8

"""
Diveplane API

OpenAPI implementation for interacting with the Diveplane API. 
"""

try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from diveplane.openapi.configuration import Configuration


class MarginalStats(object):
    """
    Auto-generated OpenAPI type.

    Marginal feature statistics.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'count': 'float',
        'mean': 'float',
        'median': 'float',
        'mode': 'object',
        'min': 'float',
        'max': 'float',
        'uniques': 'float'
    }

    attribute_map = {
        'count': 'count',
        'mean': 'mean',
        'median': 'median',
        'mode': 'mode',
        'min': 'min',
        'max': 'max',
        'uniques': 'uniques'
    }

    nullable_attributes = [
        'count', 
        'mean', 
        'median', 
        'mode', 
        'min', 
        'max', 
        'uniques', 
    ]

    discriminator = None

    def __init__(self, count=None, mean=None, median=None, mode=None, min=None, max=None, uniques=None, local_vars_configuration=None):  # noqa: E501
        """MarginalStats - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._count = None
        self._mean = None
        self._median = None
        self._mode = None
        self._min = None
        self._max = None
        self._uniques = None

        self.count = count
        self.mean = mean
        self.median = median
        self.mode = mode
        self.min = min
        self.max = max
        self.uniques = uniques

    @property
    def count(self):
        """Get the count of this MarginalStats.


        :return: The count of this MarginalStats.
        :rtype: float
        """
        return self._count

    @count.setter
    def count(self, count):
        """Set the count of this MarginalStats.


        :param count: The count of this MarginalStats.
        :type count: float
        """

        self._count = count

    @property
    def mean(self):
        """Get the mean of this MarginalStats.


        :return: The mean of this MarginalStats.
        :rtype: float
        """
        return self._mean

    @mean.setter
    def mean(self, mean):
        """Set the mean of this MarginalStats.


        :param mean: The mean of this MarginalStats.
        :type mean: float
        """

        self._mean = mean

    @property
    def median(self):
        """Get the median of this MarginalStats.


        :return: The median of this MarginalStats.
        :rtype: float
        """
        return self._median

    @median.setter
    def median(self, median):
        """Set the median of this MarginalStats.


        :param median: The median of this MarginalStats.
        :type median: float
        """

        self._median = median

    @property
    def mode(self):
        """Get the mode of this MarginalStats.


        :return: The mode of this MarginalStats.
        :rtype: object
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Set the mode of this MarginalStats.


        :param mode: The mode of this MarginalStats.
        :type mode: object
        """

        self._mode = mode

    @property
    def min(self):
        """Get the min of this MarginalStats.


        :return: The min of this MarginalStats.
        :rtype: float
        """
        return self._min

    @min.setter
    def min(self, min):
        """Set the min of this MarginalStats.


        :param min: The min of this MarginalStats.
        :type min: float
        """

        self._min = min

    @property
    def max(self):
        """Get the max of this MarginalStats.


        :return: The max of this MarginalStats.
        :rtype: float
        """
        return self._max

    @max.setter
    def max(self, max):
        """Set the max of this MarginalStats.


        :param max: The max of this MarginalStats.
        :type max: float
        """

        self._max = max

    @property
    def uniques(self):
        """Get the uniques of this MarginalStats.


        :return: The uniques of this MarginalStats.
        :rtype: float
        """
        return self._uniques

    @uniques.setter
    def uniques(self, uniques):
        """Set the uniques of this MarginalStats.


        :param uniques: The uniques of this MarginalStats.
        :type uniques: float
        """

        self._uniques = uniques

    def to_dict(self, serialize=False, exclude_null=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                elif 'exclude_null' in args:
                    return x.to_dict(serialize, exclude_null)
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            elif value is None and (exclude_null or attr not in self.nullable_attributes):
                continue
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MarginalStats):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MarginalStats):
            return True

        return self.to_dict() != other.to_dict()
