from .utils import *


class Vector:
    @overload
    def __init__(self, object: Iterable) -> None:
        pass

    @overload
    def __init__(self, size: int, dtype: Optional[type] = int) -> None:
        pass

    def __init__(
        self,
        arg1: Optional[Union[Iterable, int]],
        arg2: Optional[type] = int,
    ) -> None:
        if isinstance(arg1, int):
            self.__size = arg1
            self.__dtype = arg2
            self._initialize_data_structure(size=arg1, dtype=arg2)

        else:
            self._initialize_data_structure(object=arg1)

        self.__supported_types = int, float, str, bool
        self.__precision = 4

    def __str__(self) -> str:
        buffer = [" " for _ in range(self.size)]

        for i, value in enumerate(self.__data):
            if self.dtype == float:
                splited_value = str(value).split(".")

                if len(splited_value) == 1:
                    if splited_value[0] == "0":
                        formatted_value = f"0."

                    else:
                        formatted_value = f"{splited_value[0]}."

                if len(splited_value) == 2:
                    if splited_value[0] == "0" and splited_value[1] == "0":
                        formatted_value = f"0."

                    elif splited_value[0] == "0" and splited_value[1] != "0":
                        if len(splited_value[1]) > self.__precision:
                            formatted_value = "{:.{}e}".format(value, self.__precision)
                        else:
                            formatted_value = f"0.{splited_value[1]}"

                    elif splited_value[0] != "0" and splited_value[1] == "0":
                        formatted_value = f"{splited_value[0]}."

                    else:
                        if len(splited_value[1]) > self.__precision:
                            formatted_value = "{:.{}e}".format(value, self.__precision)
                        else:
                            formatted_value = f"{splited_value[0]}.{splited_value[1]}"

            elif self.dtype == int:
                formatted_value = str(value)

            elif self.dtype == bool:
                formatted_value = str(value)

            else:
                formatted_value = f"'{str(value)}'"

            buffer[i] = formatted_value

        max_element_length = max(len(str(item)) for item in buffer)

        output = ""

        for value in buffer:
            output += f"│ {value}{' ' * (max_element_length - len(value) + 1)} │\n"

        return output

    def __setitem__(self, index: int, value: object) -> None:
        if self.dtype == int:
            self.__data[index] = int(value)

        elif self.dtype == float:
            self.__data[index] = float(value)

        elif self.dtype == str:
            self.__data[index] = str(value)

        elif self.dtype == bool:
            self.__data[index] = bool(value)

    def __getitem__(self, index: int) -> object:
        return self.__data[index]

    def _empty_element(self) -> int | float | str | bool:
        if self.dtype == float:
            return 0.0

        elif self.dtype == str:
            return ""

        elif self.dtype == bool:
            return False

        else:
            return 0

    def _estimate_data_type(self, object: Iterable) -> type:
        type_counts = {int: 0, float: 0, str: 0, bool: 0}

        for element in object:
            if isinstance(element, int):
                type_counts[int] += 1
            elif isinstance(element, float):
                type_counts[float] += 1
            elif isinstance(element, str):
                type_counts[str] += 1
            elif isinstance(element, bool):
                type_counts[bool] += 1

        if type_counts[int] > 0 and type_counts[float] > 0:
            return float
        else:
            return max(type_counts, key=type_counts.get)

    def _fill_data(self, object: Optional[Iterable] = None) -> None:
        empty_element = self._empty_element()

        self.__data = [empty_element for _ in range(self.size)]

        if object is not None:
            for i, element in enumerate(object):
                try:
                    self.__data[i] = element
                except IndexError:
                    self.__data[i] = empty_element

    def _initialize_data_structure(
        self,
        object: Optional[Iterable] = None,
        size: Optional[int] = None,
        dtype: Optional[type] = None,
    ) -> None:
        if object is not None:
            self.__size = len(object)
            self.__dtype = self._estimate_data_type(object)
            self._fill_data(object)

        elif size is not None:
            self.__size = size
            self.__dtype = dtype
            self._fill_data()

        else:
            raise ValueError(
                "Matrix._initilize_data_structure() has recived wrong parameters"
            )

    def _adjust_size(self) -> None:
        buffer = self.__data.copy()

        init_item = self._empty_element()

        self.__data = [init_item for _ in range(self.size)]

        for i in range(self.size):
            try:
                self.__data[i] = buffer[i]
            except:
                continue

    def _change_data_type(self, new_dtype: type) -> None:
        if new_dtype not in self.__supported_types:
            raise ValueError(
                f"dl.Vector.dtype must take one of this value: {self.__supported_types}"
            )
        self.__data = list(map(new_dtype, self.__data))

    @property
    def size(self) -> int:
        return self.__size

    @size.setter
    def size(self, new_size: int) -> None:
        if isinstance(new_size, int):
            self.__size = new_size
            self._adjust_size()
        else:
            raise ValueError("Vector size must be an integer")

    @property
    def dtype(self) -> type:
        return self.__dtype

    @dtype.setter
    def dtype(self, new_value: type) -> None:
        if new_value in (int, float, str, bool):
            self.__dtype = new_value
        else:
            raise ValueError("`dl.Vector.dtype` property must be an type object")

    def change_dtype(self, new_dtype: type) -> str:
        self.dtype = new_dtype
        self._change_data_type(new_dtype)

    def set_precision(self, new_precision: int) -> None:
        if isinstance(new_precision, int):
            self.__precision = new_precision
        else:
            raise ValueError("Number precision must be an integer")

    def to_list(self) -> list[Union[int, float, str, bool]]:
        return self.__data

    def to_tuple(self) -> tuple[Union[int, float, str, bool]]:
        return tuple(self.__data)

    def copy(self) -> list[Union[int, float, str, bool]]:
        return self.__data
