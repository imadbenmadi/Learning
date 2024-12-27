import sys


# MATH


def example_bool():
    is_non_empty = bool("Hello")
    is_zero = bool(0)
    assert is_non_empty is True
    assert is_zero is False

    class MyClass:
        def __bool__(self):
            return True

    if MyClass():
        ...


def example_int():
    string_num = "123"
    converted_num = int(string_num)
    assert converted_num == 123

    class MyNum:
        def __int__(self):
            return 42

    assert int(MyNum()) == 42


def example_float():
    string_num = "123.45"
    converted_num = float(string_num)
    assert converted_num == 123.45

    class MyNum:
        def __float__(self):
            return 42.0

    assert float(MyNum()) == 42.0


def example_complex():
    real_part = 3.5
    imaginary_part = 4.2
    complex_num = complex(real_part, imaginary_part)
    assert complex_num == 3.5 + 4.2j

    class MyNum:
        def __complex__(self):
            return 1j

    assert complex(MyNum()) == 1j


def example_max_min():
    numbers = [5, 3, 9, 1, 7]
    assert max(numbers) == 9
    assert min(numbers) == 1

    assert max(5, 3, 9, 1, 7) == 9
    assert min(5, 3, 9, 1, 7) == 1


def example_divmod():
    quotient, remainder = 10 // 3, 10 % 3
    quotient, remainder = divmod(10, 3)
    assert (quotient, remainder) == (3, 1)


def example_abs():
    assert abs(-10) == 10
    assert abs(-10.0) == 10.0
    assert abs(3 + 4j) == 5

    class MyNum:
        def __abs__(self):
            return 42

    assert abs(MyNum()) == 42


def example_pow():
    base = 2
    exponent = 3
    modulus = 5

    result_no_modulus = base**exponent
    result_no_modulus = pow(base, exponent)
    result_with_modulus = pow(base, exponent, modulus)

    assert result_no_modulus == 8
    assert result_with_modulus == 3


def example_round():
    assert round(3.14159, 2) == 3.14
    assert round(2.675, 2) == 3.67  # Warning float errors
    assert round(314159, -4) == 310000

    class MyNum:
        def __round__(self, n=None):
            return 0

    assert round(MyNum(), 2) == 0


def example_sum():
    numbers = [1, 2, 3, 4, 5]
    assert sum(numbers) == 15
    even_count = sum(1 for x in numbers if x % 2 == 0)
    assert even_count == 2

    class MyNum:
        def __init__(self, x):
            self.x = x

        def __add__(self, other):
            return MyNum(self.x + other.x)

    my_sum = sum([MyNum(1), MyNum(2), MyNum(3)], start=MyNum(0))
    assert my_sum.x == 6


# COLLECTIONS


def example_dict():
    person = {"name": "Alice", "age": 30, "city": "New York"}
    person = dict(name="Alice", age=30, city="New York")
    person = dict([("name", "Alice"), ("age", 30), ("city", "New York")])

    assert person["name"] == "Alice"
    assert person["age"] == 30
    assert person["city"] == "New York"


def example_list():
    fruits_set = {"apple", "banana", "cherry"}
    fruits = list(fruits_set)
    assert fruits[0] in fruits_set
    assert len(fruits) == 3


def example_tuple():
    coordinates = tuple([3, 4])
    coordinates = (3, 4)
    assert coordinates[0] == 3
    assert coordinates[1] == 4
    # coordinates[0] = 42 # ERROR


def example_set():
    fruits = set(["apple", "apple", "banana", "cherry"])
    fruits = {"apple", "banana", "cherry"}
    assert len(fruits) == 3
    assert "banana" in fruits


def example_frozenset():
    colors = frozenset(["red", "green", "blue"])
    assert len(colors) == 3
    assert "red" in colors
    # colors.add("yellow") # ERROR
    d = {colors: "this works!"}


# STRINGS AND BYTES


def example_bytes():
    data = bytes(b"Hello")
    assert len(data) == 5
    assert data[0] == 72  # ASCII value of 'H'
    # data[0] = 104  # ERROR

    assert data.decode() == "Hello"
    assert "Hello".encode() == data


def example_bytearray():
    data = bytearray(b"Hello")
    assert len(data) == 5
    assert data[0] == 72  # ASCII value of 'H'
    data[0] = 104  # 'h'


def example_str():
    assert str(42) == "42"
    assert str(True) == "True"
    assert str(dict) == "<class 'dict'>"


def example_memoryview():
    raw_bytes = b"\x01\x00\x00\x00\x02\x00\x00\x00" b"\x03\x00\x00\x00\x04\x00\x00\x00"

    data = memoryview(raw_bytes).cast("i", shape=(2, 2))

    assert data[0, 0] == 1
    assert data.tolist() == [[1, 2], [3, 4]]
    assert data[0:1].tolist() == [[1, 2]]


def example_open():
    with open("example.txt", "w") as f:
        f.write("Hello, World!")
    with open("example.txt", "r") as f:
        content = f.read()
        assert content == "Hello, World!"


def example_chr_ord():
    assert chr(65) == "A"
    assert ord("A") == 65

    assert chr(128512) == "😀"
    assert ord("😀") == 128512


def example_bin_oct_hex():
    assert bin(42) == "0b101010"
    assert oct(42) == "0o52"
    assert hex(42) == "0x2a"

    assert int("0b101010", 2) == 42
    assert int("0o52", 8) == 42
    assert int("0x2a", 16) == 42


def example_format():
    name = "Alice"
    age = 31

    formatted_str = "Name: {}, Age: {}".format(name, age)
    assert formatted_str == "Name: Alice, Age: 31"

    f_str = f"Name: {name}, Age: {age}"
    assert f_str == "Name: Alice, Age: 31"

    formatted_str = "Name: {}, Age: {:x}".format(name, age)
    assert formatted_str == "Name: Alice, Age: 1f"

    f_str = f"Name: {name}, Age: {age:x}"
    assert f_str == "Name: Alice, Age: 1f"

    assert format(31) == "31"
    assert format(31, "x") == "1f"

    class MyCls:
        def __format__(self, format_spec=""):
            if format_spec == "x":
                return "<HEX>"
            return "<NORMAL>"


def example_input():
    name = input("Enter your name: ")
    assert isinstance(name, str)


def example_ascii_repr():
    assert ascii("hello") == "'hello'"
    assert repr("hello") == "'hello'"

    assert ascii("😀") == "'\\U0001f600'"
    assert repr("😀") == "'😀'"


# ITERATION


def example_iter_next():
    iterable = iter([1, 2, 3])
    assert next(iterable) == 1
    assert next(iterable) == 2
    assert next(iterable) == 3

    for x in [1, 2, 3]:
        print(x)


def example_enumerate():
    colors = ["red", "green", "blue"]
    enumerated_colors = list(enumerate(colors))
    assert enumerated_colors[0] == (0, "red")
    assert enumerated_colors[1] == (1, "green")
    assert enumerated_colors[2] == (2, "blue")

    for index, color in enumerate(colors):
        print(index, color)


def example_zip():
    numbers = [1, 2, 3]
    letters = ["a", "b", "c"]
    zipped = list(zip(numbers, letters))
    assert zipped[0] == (1, "a")
    assert zipped[1] == (2, "b")
    assert zipped[2] == (3, "c")

    for number, letter in zip(numbers, letters):
        print(number, letter)


def example_reversed():
    numbers = [1, 2, 3, 4, 5]
    reversed_numbers = list(reversed(numbers))
    assert reversed_numbers == [5, 4, 3, 2, 1]

    for x in reversed(numbers):
        print(x)

    class MyClass:
        def __reversed__(self):
            ...

    assert next(iter(reversed({"a": 1, "b": 2, "c": 3}))) == "c"


def example_sorted():
    numbers = [5, 2, 8, 1, 3]
    sorted_numbers = sorted(numbers)
    assert sorted_numbers == [1, 2, 3, 5, 8]


def example_filter():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    assert even_numbers == [2, 4, 6, 8, 10]
    even_numbers = [x for x in numbers if x % 2 == 0]


def example_map():
    numbers = [1, 2, 3, 4, 5]
    squared_numbers = list(map(lambda x: x**2, numbers))
    assert squared_numbers == [1, 4, 9, 16, 25]
    squared_numbers = [x**2 for x in numbers]


def example_all_any():
    assert all([True, True, True])
    assert not all([True, False, True])

    assert any([True, True, True])
    assert any([True, False, True])

    assert all([])
    assert not any([])


def example_range():
    numbers = list(range(1, 6))
    assert numbers == [1, 2, 3, 4, 5]

    for n in range(10):
        print(n)

    assert 42 in range(10000000000000000000000)  # OK


def example_slice():
    numbers = [1, 2, 3, 4, 5]

    assert numbers[slice(1, 4)] == [2, 3, 4]
    assert numbers[1:4] == [2, 3, 4]

    # x = 1:4 # ERROR
    x = slice(1, 4)

    class MySeq:
        def __getitem__(self, item):
            if isinstance(item, slice):
                ...
            ...

    assert numbers[slice(1, 4, 2)] == [2, 4]
    assert numbers[1:4:2] == [2, 4]


# ASYNC ITERATION


async def example_aiter_anext():
    async def async_generator():
        yield 1
        yield 2
        yield 3

    async_gen = async_generator()
    async_iter = aiter(async_gen)

    assert await anext(async_iter) == 1
    assert await anext(async_iter) == 2
    assert await anext(async_iter) == 3

    async for x in async_generator():
        ...


# DEBUGGING


def example_breakpoint():
    for i in range(5):
        if i == 3:
            breakpoint()
        print(i)


def example_help():
    help(str)


def example_print():
    message = "Hello, World!"
    print(message)
    print(message, file=sys.stderr)


# OBJECT INSPECTION/MODIFICATION


def example_object():
    sentinel = object()
    assert sentinel is not None

    d = {"val": None}
    val = d.get("val", sentinel)
    if val is sentinel:
        print("not found")


def example_getattr_setattr_delattr_hasattr():
    class Example:
        def __init__(self):
            self.attribute = 42

    instance = Example()

    assert getattr(instance, "attribute") == 42
    assert instance.attribute == 42

    assert getattr(instance, "nonexistent", "default") == "default"

    instance.new_attribute = "value"
    setattr(instance, "new_attribute", "value")

    assert hasattr(instance, "new_attribute")

    delattr(instance, "attribute")
    del instance.attribute
    assert not hasattr(instance, "attribute")


def example_dir():
    numbers = [1, 2, 3]
    dir_list = dir(numbers)
    assert "__len__" in dir_list
    assert "__getitem__" in dir_list
    # note: not guaranteed to be correct or complete


def example_id():
    obj = "Hello"
    obj_id = id(obj)
    assert obj_id == id("Hello")

    s = {1, 2, 3}
    s2 = {1, 2, 3}
    assert s == s2
    assert id(s) != id(s2)

    assert s is s
    assert s is not s2


def example_hash():
    obj = "Hello"
    obj_hash = hash(obj)
    assert obj_hash == hash("Hello")

    class MyCls:
        def __hash__(self):
            return 42

    assert hash(MyCls()) == 42


def example_len():
    numbers = [1, 2, 3, 4, 5]
    length = len(numbers)
    assert length == 5


def example_isinstance():
    value = 42

    # assert type(value) is int
    assert isinstance(value, int)
    assert not isinstance(value, str)

    assert isinstance(False, int)


def example_issubclass():
    class Parent:
        pass

    class Child(Parent):
        pass

    assert issubclass(Child, Parent)
    assert not issubclass(Parent, Child)


def example_callable():
    def func():
        return "Hello"

    class MyClass:
        def method(self):
            return "World"

    assert callable(func)
    obj = MyClass()
    assert callable(obj.method)
    assert not callable("Hello")


def example_super():
    class Parent:
        def greet(self):
            return "Hello from Parent"

    class Child(Parent):
        def greet(self):
            return super().greet() + ", and Hello from Child"

    child = Child()
    assert child.greet() == "Hello from Parent, and Hello from Child"


def example_type():
    number = 42
    type_of_number = type(number)
    assert type_of_number is int


def example_new_type():
    def greet(self):
        return f"Hello, {self.name}!"

    NewType = type("NewType", (object,), {"name": "World", "greet": greet})

    instance = NewType()
    assert instance.name == "World"
    assert instance.greet() == "Hello, World!"


# DESCRIPTORS


def example_classmethod_property_staticmethod():
    class MyClass:
        def __init__(self, value):
            self._value = value

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, val):
            self._value = val

        @classmethod
        def class_method(cls):
            return cls.__name__

        @staticmethod
        def static_method():
            return "Static method called"

    instance = MyClass(42)

    assert instance.value == 42
    instance.value = 0

    assert instance.class_method() == "MyClass"
    assert MyClass.static_method() == "Static method called"


# DYNAMIC/CODE


def example_eval():
    x = 1
    expression = "x + 3 + 4 * 2"
    result = eval(expression)
    assert result == 12


def example_exec():
    code = """
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
"""
    exec(code)


def example_compile():
    code = 'print("Hello, World!")'
    compiled_code = compile(code, "<string>", "exec")
    exec(compiled_code)


def example_globals():
    global var
    var = 42
    global_vars = globals()
    assert global_vars["var"] == 42

    global_vars["var"] = 43
    assert var == 43


def example_locals():
    local_var = 10
    local_vars = locals()
    assert local_vars["local_var"] == 10
    # dont modify


def example_vars():
    class MyClass:
        def __init__(self):
            self.attribute = 42

    obj = MyClass()
    obj.attribute2 = "hello"

    vars_dict = vars(obj)
    assert vars_dict["attribute"] == 42
    assert vars_dict["attribute2"] == "hello"


def example_import():
    math = __import__("math")
    assert math.sqrt(16) == 4.0

    math2 = __import__("math")
    assert math is math2

    _temp = __import__("spam.ham", globals(), locals(), ["eggs", "sausage"], 0)
    eggs, saus = _temp.eggs, _temp.sausage

    import importlib

    math3 = importlib.import_module("math")
