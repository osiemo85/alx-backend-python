#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the correct result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_error_key):
        """Test access_nested_map raises KeyError with expected message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_error_key}'")


class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function."""

    @patch("utils.requests.get")
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected payload."""
        # Create a Mock response object with the desired payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call get_json and verify the result
        result = get_json(test_url)
        self.assertEqual(result, test_payload)

        # Ensure requests.get was called once with the correct URL
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator."""

    def test_memoize(self):
        """Test memoize caches a_property correctly."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            test_instance = TestClass()
            # Call a_property twice
            result_1 = test_instance.a_property
            result_2 = test_instance.a_property

            # Ensure a_method is only called once
            mock_method.assert_called_once()
            # Verify the result is as expected
            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)


if __name__ == "__main__":
    unittest.main()
