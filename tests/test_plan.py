import unittest

from hank.plans import Plan, plan


@plan
def basic_plan():
    pass


class TestPlan(unittest.TestCase):
    def test_plan(self):
        self.assertTrue(isinstance(basic_plan, Plan))
        test_task = basic_plan.task(params={})
        self.assertEqual(test_task.plan, "/tests/test_plan/basic_plan")
