"""Pengujian otomatis sederhana untuk logika FuGu (tidak memerlukan Streamlit)."""
import unittest

from fugu_logic import (
    filter_programs,
    filter_scholarships,
    filter_universities,
    load_all_data,
    recommend_programs,
)


class FuGuLogicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_all_data()

    def test_sample_data_ids_link_consistently(self):
        program_ids = {p["id"] for p in self.data["programs"]}
        university_ids = {u["id"] for u in self.data["universities"]}
        for university in self.data["universities"]:
            self.assertTrue(set(university["program_ids"]).issubset(program_ids), university["id"])
        for program in self.data["programs"]:
            self.assertTrue(set(program["university_ids"]).issubset(university_ids), program["id"])

    def test_program_search_and_interest_filter(self):
        found = filter_programs(self.data["programs"], query="algoritma")
        self.assertEqual([p["id"] for p in found], ["informatika"])
        by_interest = filter_programs(self.data["programs"], interest="Lingkungan & Alam")
        self.assertTrue(by_interest)
        self.assertTrue(all("Lingkungan & Alam" in p["interest_tags"] for p in by_interest))

    def test_university_region_cost_and_program_filters(self):
        found = filter_universities(
            self.data["universities"], region="Sumatera", cost="Terjangkau", program_id="agribisnis"
        )
        self.assertEqual([u["id"] for u in found], ["u06"])

    def test_scholarship_filters(self):
        found = filter_scholarships(
            self.data["scholarships"], audience="Mahasiswa", focus="Sains & Riset"
        )
        self.assertEqual([s["id"] for s in found], ["scholarship-05"])
        self.assertEqual(filter_scholarships(self.data["scholarships"], query="tidak-ada-hasil"), [])

    def test_recommendations_are_explainable_and_sorted(self):
        profile = {
            "interests": ["Teknologi & Komputer", "Angka & Analisis"],
            "region": "Jawa",
            "budget": "Utamakan biaya terjangkau",
            "style": "Praktik & proyek",
        }
        results = recommend_programs(self.data["programs"], self.data["universities"], profile, limit=5)
        self.assertTrue(results)
        scores = [item["score"] for item in results]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertTrue(all(0 <= score <= 100 for score in scores))
        self.assertTrue(all(item["criteria"] and item["reasons"] for item in results))
        self.assertEqual(results[0]["program"]["id"], "informatika")

    def test_no_interests_returns_no_recommendations(self):
        self.assertEqual(
            recommend_programs(self.data["programs"], self.data["universities"], {"interests": []}), []
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
