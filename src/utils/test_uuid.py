import unittest

from .uuid_custom import generate_uuid


class TestUUID(unittest.TestCase):
    def test_generate_uuid(self):
        uuid = generate_uuid()
        self.assertEqual(
            len(uuid),
            36,
            f"UUID length expected to be 36 but actual length is {len(uuid)}")
