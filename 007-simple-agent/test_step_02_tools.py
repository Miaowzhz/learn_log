import unittest

from step_02_tools import calculate_study_budget, get_topic_outline


class CalculateStudyBudgetTests(unittest.TestCase):
    def test_calculates_total_minutes(self) -> None:
        result = calculate_study_budget.invoke(
            {"days": 7, "minutes_per_day": 45}
        )
        self.assertEqual(result, "总学习时间：315 分钟（7 天 x 45 分钟）")

    def test_rejects_zero_days(self) -> None:
        with self.assertRaises(ValueError):
            calculate_study_budget.invoke({"days": 0, "minutes_per_day": 45})

    def test_rejects_negative_minutes(self) -> None:
        with self.assertRaises(ValueError):
            calculate_study_budget.invoke({"days": 7, "minutes_per_day": -1})


class GetTopicOutlineTests(unittest.TestCase):
    def test_finds_topic_case_insensitively(self) -> None:
        result = get_topic_outline.invoke({"topic": "  LangChain  "})
        self.assertIn("工具", result)
        self.assertIn("Agent", result)

    def test_finds_fastapi(self) -> None:
        result = get_topic_outline.invoke({"topic": "FastAPI"})
        self.assertIn("依赖注入", result)

    def test_reports_unsupported_topic(self) -> None:
        result = get_topic_outline.invoke({"topic": "Django"})
        self.assertEqual(
            result,
            "暂不支持 Django；可选主题：Python、FastAPI、LangChain",
        )


if __name__ == "__main__":
    unittest.main()
