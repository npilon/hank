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

    def test_main_plan(self):
        def main_plan():
            pass

        main_plan.__module__ = "__main__"
        main_plan = plan(main_plan)
        main_task = main_plan.task(params={})
        self.assertEqual(main_task.plan, "/main_plan")
