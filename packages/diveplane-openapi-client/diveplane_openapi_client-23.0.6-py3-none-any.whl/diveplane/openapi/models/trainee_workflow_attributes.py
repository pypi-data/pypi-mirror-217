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


class TraineeWorkflowAttributes(object):
    """
    Auto-generated OpenAPI type.

    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'hyperparameter_map': 'dict[str, dict[str, object]]',
        'auto_optimize_enabled': 'bool',
        'auto_optimize_limit_size': 'int',
        'optimize_growth_factor': 'float',
        'optimize_threshold': 'int'
    }

    attribute_map = {
        'hyperparameter_map': 'hyperparameter_map',
        'auto_optimize_enabled': 'auto_optimize_enabled',
        'auto_optimize_limit_size': 'auto_optimize_limit_size',
        'optimize_growth_factor': 'optimize_growth_factor',
        'optimize_threshold': 'optimize_threshold'
    }

    nullable_attributes = [
    ]

    discriminator = None

    def __init__(self, hyperparameter_map=None, auto_optimize_enabled=None, auto_optimize_limit_size=None, optimize_growth_factor=None, optimize_threshold=None, local_vars_configuration=None):  # noqa: E501
        """TraineeWorkflowAttributes - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._hyperparameter_map = None
        self._auto_optimize_enabled = None
        self._auto_optimize_limit_size = None
        self._optimize_growth_factor = None
        self._optimize_threshold = None

        if hyperparameter_map is not None:
            self.hyperparameter_map = hyperparameter_map
        if auto_optimize_enabled is not None:
            self.auto_optimize_enabled = auto_optimize_enabled
        if auto_optimize_limit_size is not None:
            self.auto_optimize_limit_size = auto_optimize_limit_size
        if optimize_growth_factor is not None:
            self.optimize_growth_factor = optimize_growth_factor
        if optimize_threshold is not None:
            self.optimize_threshold = optimize_threshold

    @property
    def hyperparameter_map(self):
        """Get the hyperparameter_map of this TraineeWorkflowAttributes.


        :return: The hyperparameter_map of this TraineeWorkflowAttributes.
        :rtype: dict[str, dict[str, object]]
        """
        return self._hyperparameter_map

    @hyperparameter_map.setter
    def hyperparameter_map(self, hyperparameter_map):
        """Set the hyperparameter_map of this TraineeWorkflowAttributes.


        :param hyperparameter_map: The hyperparameter_map of this TraineeWorkflowAttributes.
        :type hyperparameter_map: dict[str, dict[str, object]]
        """

        self._hyperparameter_map = hyperparameter_map

    @property
    def auto_optimize_enabled(self):
        """Get the auto_optimize_enabled of this TraineeWorkflowAttributes.

        When True, the train operation returns when it's time for the model to be optimized again.

        :return: The auto_optimize_enabled of this TraineeWorkflowAttributes.
        :rtype: bool
        """
        return self._auto_optimize_enabled

    @auto_optimize_enabled.setter
    def auto_optimize_enabled(self, auto_optimize_enabled):
        """Set the auto_optimize_enabled of this TraineeWorkflowAttributes.

        When True, the train operation returns when it's time for the model to be optimized again.

        :param auto_optimize_enabled: The auto_optimize_enabled of this TraineeWorkflowAttributes.
        :type auto_optimize_enabled: bool
        """

        self._auto_optimize_enabled = auto_optimize_enabled

    @property
    def auto_optimize_limit_size(self):
        """Get the auto_optimize_limit_size of this TraineeWorkflowAttributes.

        The size of of the model at which to stop doing auto-optimization. Value of 0 means no limit.

        :return: The auto_optimize_limit_size of this TraineeWorkflowAttributes.
        :rtype: int
        """
        return self._auto_optimize_limit_size

    @auto_optimize_limit_size.setter
    def auto_optimize_limit_size(self, auto_optimize_limit_size):
        """Set the auto_optimize_limit_size of this TraineeWorkflowAttributes.

        The size of of the model at which to stop doing auto-optimization. Value of 0 means no limit.

        :param auto_optimize_limit_size: The auto_optimize_limit_size of this TraineeWorkflowAttributes.
        :type auto_optimize_limit_size: int
        """

        self._auto_optimize_limit_size = auto_optimize_limit_size

    @property
    def optimize_growth_factor(self):
        """Get the optimize_growth_factor of this TraineeWorkflowAttributes.

        The factor by which to increase the optimize threshold every time the model grows to the current threshold size.

        :return: The optimize_growth_factor of this TraineeWorkflowAttributes.
        :rtype: float
        """
        return self._optimize_growth_factor

    @optimize_growth_factor.setter
    def optimize_growth_factor(self, optimize_growth_factor):
        """Set the optimize_growth_factor of this TraineeWorkflowAttributes.

        The factor by which to increase the optimize threshold every time the model grows to the current threshold size.

        :param optimize_growth_factor: The optimize_growth_factor of this TraineeWorkflowAttributes.
        :type optimize_growth_factor: float
        """

        self._optimize_growth_factor = optimize_growth_factor

    @property
    def optimize_threshold(self):
        """Get the optimize_threshold of this TraineeWorkflowAttributes.

        The threshold for the number of cases at which the model should be re-optimized.

        :return: The optimize_threshold of this TraineeWorkflowAttributes.
        :rtype: int
        """
        return self._optimize_threshold

    @optimize_threshold.setter
    def optimize_threshold(self, optimize_threshold):
        """Set the optimize_threshold of this TraineeWorkflowAttributes.

        The threshold for the number of cases at which the model should be re-optimized.

        :param optimize_threshold: The optimize_threshold of this TraineeWorkflowAttributes.
        :type optimize_threshold: int
        """

        self._optimize_threshold = optimize_threshold

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
        if not isinstance(other, TraineeWorkflowAttributes):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TraineeWorkflowAttributes):
            return True

        return self.to_dict() != other.to_dict()
