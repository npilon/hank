import unittest


class TestTask(unittest.TestCase):
    def test_json(self):
        import dataclasses
        import json

        from hank.task import Task

        sample_task = Task(plan="a_plan", params={"args": [42]})
        self.assertEqual(
            json.dumps(dataclasses.asdict(sample_task)),
            json.dumps(
                {"plan": "a_plan", "params": {"args": [42]}, "dispatcher": None}
            ),
        )
