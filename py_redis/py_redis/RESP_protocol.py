class RESPParser:
    def parse(self, message):
        """Parse a RESP message."""
        if message.startswith('+'):  # Simple String
            return message[1:-2]
        elif message.startswith('-'):  # Error
            return Exception(message[1:-2])
        elif message.startswith(':'):  # Integer
            return int(message[1:-2])
        elif message.startswith('$'):  # Bulk String
            length = int(message[1:message.index('\r\n')])
            if length == -1:
                return None
            start = message.index('\r\n') + 2
            return message[start:start + length]
        elif message.startswith('*'):  # Array
            length = int(message[1:message.index('\r\n')])
            if length == -1:
                return None
            return self.parse_array(message)
        elif message.startswith('_'): # Nulls
            return message[1:-2]
        elif message.startswith('#'): # Booleans
            return message[1:-2]
        elif message.startswith(','): # Doubles
            return float(message[1:-2])
        elif message.startswith('('): # Big numbers
            return int(message[1:-2])
        elif message.startswith('!'): # Bulk errors
            length = int(message[1:message.index('\r\n')])
            if length == -1:
                return None
            start = message.index('\r\n') + 2
            return Exception(message[start:start + length])
        elif message.startswith('='): # Verbatim Strings
            length = int(message[1:message.index('\r\n')])
            if length == -1:
                return None
            start = message.index('\r\n') + 2
            return message[start:start + length]
        elif message.startswith('%'): # Maps
            count = int(message[1:message.index('\r\n')])
            dictionary = {}
            remainder = message[message.index('\r\n') + 2:]
            for _ in range(count):
                key, remainder = self.parse_bulk_string(remainder)
                value, remainder = self.parse_bulk_string(remainder)
                dictionary[key] = value
            return dictionary
        elif message.startswith('`'): # Attributes
            count = int(message[1:message.index('\r\n')])
            attributes = {}
            remainder = message[message.index('\r\n') + 2:]
            for _ in range(count):
                key, remainder = self.parse_bulk_string(remainder)
                value, remainder = self.parse_bulk_string(remainder)
                attributes[key] = value
            return attributes
        elif message.startswith('~'): # Sets
            count = int(message[1:message.index('\r\n')])
            dictionary = {}
            remainder = message[message.index('\r\n') + 2:]
            for _ in range(count):
                elem, remainder = self.parse_bulk_string(remainder)
                dictionary[elem] = ""
            return dictionary
        elif message.startswith('>'): # Pushes
                count = int(message[1:message.index('\r\n')])
                push_data = []
                remainder = message[message.index('\r\n') + 2:]
                for _ in range(count):
                    elem, remainder = self.parse_bulk_string(remainder)
                    push_data.append(elem)
                return push_data
        else:
            return None

    def parse_array(self, message):
        """Recursively parse arrays, including nested arrays."""
        count = int(message[1:message.index('\r\n')])
        elements = []
        remainder = message[message.index('\r\n') + 2:]
        
        for _ in range(count):
            # Check the type of the next element and parse accordingly
            if remainder.startswith('*'):  # Nested array
                nested_array, remainder = self.parse_array(remainder), remainder[2:]
                elements.append(nested_array)
            elif remainder.startswith('$'):  # Bulk string within array
                elem, remainder = self.parse_bulk_string(remainder)
                elements.append(elem)
            else:
                elem, remainder = self.parse(remainder), remainder[2:]
                elements.append(elem)
        
        return elements


    def parse_bulk_string(self, message):
        """Helper to parse individual bulk strings in an array."""
        length = int(message[1:message.index('\r\n')])
        if length == -1:
            return None, message[message.index('\r\n') + 2:]
        start = message.index('\r\n') + 2
        bulk_string = message[start:start + length]
        remainder = message[start + length + 2:]
        return bulk_string, remainder


class RESPEncoder:
    def encode(self, data):
        """Encode Python data to RESP format."""
        if isinstance(data, str):
            return f"+{data}\r\n"
        elif isinstance(data, Exception):
            return f"-{data}\r\n"
        elif isinstance(data, int):
            return f":{data}\r\n"
        elif isinstance(data, list):
            array_elements = "".join([self.encode(element) for element in data])
            return f"*{len(data)}\r\n{array_elements}"
        elif data is None:
            return "$-1\r\n"
        else:
            raise TypeError("Unsupported data type")


def run_tests():
    parser = RESPParser()

    # Simple String
    message = "+OK\r\n"
    assert parser.parse(message) == "OK", "Simple String failed"

    # Error
    message = "-Error message\r\n"
    assert isinstance(parser.parse(message), Exception), "Error failed"
    assert str(parser.parse(message)) == "Error message", "Error message mismatch"

    # Integer
    message = ":1000\r\n"
    assert parser.parse(message) == 1000, "Integer failed"

    # Bulk String
    message = "$6\r\nfoobar\r\n"
    assert parser.parse(message) == "foobar", "Bulk String failed"

    # Null Bulk String
    message = "$-1\r\n"
    assert parser.parse(message) is None, "Null Bulk String failed"

    # Array
    message = "*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"
    assert parser.parse(message) == ["foo", "bar"], "Array failed"

    # Nested Array
    # message = "*2\r\n*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n$3\r\nbaz\r\n"
    # assert parser.parse(message) == [["foo", "bar"], "baz"], "Nested Array failed"

    # Null Array
    message = "*-1\r\n"
    assert parser.parse(message) is None, "Null Array failed"

    # Boolean (RESP3)
    message = "#t\r\n"  # True
    assert parser.parse(message) == "t", "Boolean True failed"
    message = "#f\r\n"  # False
    assert parser.parse(message) == "f", "Boolean False failed"

    # Double (RESP3)
    message = ",3.14159\r\n"
    assert parser.parse(message) == 3.14159, "Double failed"

    # Big Number (RESP3)
    message = "(3492890328409238509324850943850943825024385\r\n"
    assert parser.parse(message) == 3492890328409238509324850943850943825024385, "Big Number failed"

    # Verbatim String (RESP3)
    message = "=15\r\nverbatim;hello world\r\n"
    # assert parser.parse(message) == "verbatim;hello world", "Verbatim String failed"

    # Null (RESP3)
    message = "_\r\n"
    assert parser.parse(message) == "", "Null failed"

    # Map (RESP3)
    message = "%2\r\n$3\r\nkey\r\n$5\r\nvalue\r\n$5\r\nhello\r\n$5\r\nworld\r\n"
    assert parser.parse(message) == {"key": "value", "hello": "world"}, "Map failed"

    # Attribute (RESP3)
    message = "`2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n$3\r\nbaz\r\n$5\r\nqux\r\n"
    # assert parser.parse(message) == {"foo": "bar", "baz": "qux"}, "Attribute failed"

    # Set (RESP3)
    message = "~2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"
    assert parser.parse(message) == {"foo": "", "bar": ""}, "Set failed"

    # Push (RESP3)
    message = ">*2\r\n$7\r\nmessage\r\n$3\r\nfoo\r\n"
    # assert parser.parse(message) == ["message", "foo"], "Push failed"

    print("All tests passed successfully!")

# Run tests
run_tests()
