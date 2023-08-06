import sys
from collections import UserDict
from rapidfuzz import process, fuzz, utils

dict_config = sys.modules[__name__]
dict_config.fuzzycfg = {"scorer": fuzz.WRatio, "processor": utils.default_process}


class FuzzDict(UserDict):
    """
    Dictionary-like object with fuzzy key matching support.

    This class extends the UserDict class and implements a dictionary-like
    object that allows fuzzy matching for keys. When accessing an item using
    the __getitem__ method, if an exact match is not found, it performs a
    fuzzy match using the rapidfuzz library.

    Attributes:
        data (dict): The underlying dictionary to store the data.

    Methods:
        __init__(self, initialdata=None, **kwargs):
            Initializes the FuzzDict object with optional initial data.

        __getitem__(self, key):
            Retrieves the value associated with the given key, supporting fuzzy matching.

    Usage example:
        from fuzzyydictyy import FuzzDict, dict_config
        from rapidfuzz import fuzz
        dict_config.fuzzycfg = {
            'scorer': fuzz.WRatio,
        }
        d = FuzzDict()
        d["hans"] = 3
        d["bobo"] = 30
        d["baba"] = 320
        print(d['hjan'])  # Output: 3 (Exact match for 'hjan' is not found)
        print(d['boba'])  # Output: 30 (Exact match for 'boba' is not found)
        print(d['babaa'])  # Output: 320 (Exact match for 'babaa' is not found)
    """

    def __init__(self, initialdata=None, **kwargs):
        """
        Initialize the FuzzDict object.

        Args:
            initialdata (Optional[dict]): Initial data to populate the FuzzDict object.
            **kwargs: Additional keyword arguments to pass to the base class.
        """
        super().__init__(**kwargs)
        self.data = {}
        if initialdata:
            self.data.update(initialdata)

    def __getitem__(self, key):
        """
        Retrieve the value associated with the given key, supporting fuzzy matching.

        If an exact match for the key is found in the data dictionary, the associated
        value is returned. Otherwise, a fuzzy match is performed using the rapidfuzz
        library and the value associated with the best match is returned.

        Args:
            key: The key to retrieve the value for.

        Returns:
            The value associated with the key.

        Raises:
            IndexError: If no match is found during fuzzy matching.
        """
        if key in self.data:
            return self.data[key]
        tmp = {}
        for k, i in self.data.items():
            tmp[f"{k}{repr(k)}"] = i
        return tmp[
            process.extract(
                f"{key}{repr(key)}", list(tmp), **dict_config.fuzzycfg, limit=1
            )[0][0]
        ]
