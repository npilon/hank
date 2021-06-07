import unittest


class TestTask(unittest.TestCase):
    def test_json(self):
        import dataclasses
        import json

        from hank.task import Task

        sample_task = Task(plan="a_plan", params={"args": [42]})
        self.assertEqual(
            Task(**json.loads(json.dumps(dataclasses.asdict(sample_task)))),
            sample_task,
        )
