"""Logika data dan rekomendasi FuGu. Seluruh data yang dimuat adalah contoh demo."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str) -> list[dict[str, Any]]:
    """Muat daftar objek JSON dari folder data/ proyek."""
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, list):
        raise ValueError(f"Format data {filename} harus berupa daftar JSON.")
    return value


def load_all_data() -> dict[str, list[dict[str, Any]]]:
    """Memuat tiga kumpulan data contoh yang dipakai aplikasi."""
    return {
        "programs": load_json("programs.json"),
        "universities": load_json("universities.json"),
        "scholarships": load_json("scholarships.json"),
    }


def filter_programs(
    programs: list[dict[str, Any]],
    query: str = "",
    field: str = "Semua bidang",
    level: str = "Semua jenjang",
    interest: str = "Semua minat",
) -> list[dict[str, Any]]:
    """Filter program berdasarkan kata pencarian, bidang, jenjang, dan tag minat."""
    needle = query.strip().casefold()
    results = []
    for program in programs:
        searchable = " ".join(
            [program.get("name", ""), program.get("field", ""), program.get("summary", "")]
            + program.get("subjects", [])
            + program.get("career_examples", [])
        ).casefold()
        if needle and needle not in searchable:
            continue
        if field != "Semua bidang" and program.get("field") != field:
            continue
        if level != "Semua jenjang" and program.get("level") != level:
            continue
        if interest != "Semua minat" and interest not in program.get("interest_tags", []):
            continue
        results.append(program)
    return results


def filter_universities(
    universities: list[dict[str, Any]],
    query: str = "",
    region: str = "Semua wilayah",
    cost: str = "Semua kisaran",
    program_id: str = "Semua program",
) -> list[dict[str, Any]]:
    """Filter kampus contoh berdasarkan teks, wilayah, kisaran biaya, dan program."""
    needle = query.strip().casefold()
    results = []
    for university in universities:
        searchable = " ".join(
            [university.get("name", ""), university.get("city", ""), university.get("region", ""), university.get("description", "")]
        ).casefold()
        if needle and needle not in searchable:
            continue
        if region != "Semua wilayah" and university.get("region") != region:
            continue
        if cost != "Semua kisaran" and university.get("tuition_band") != cost:
            continue
        if program_id != "Semua program" and program_id not in university.get("program_ids", []):
            continue
        results.append(university)
    return results


def filter_scholarships(
    scholarships: list[dict[str, Any]],
    query: str = "",
    audience: str = "Semua sasaran",
    focus: str = "Semua kategori",
) -> list[dict[str, Any]]:
    """Filter beasiswa simulasi tanpa menganggapnya sebagai penawaran resmi."""
    needle = query.strip().casefold()
    results = []
    for scholarship in scholarships:
        searchable = " ".join(
            [scholarship.get("name", ""), scholarship.get("audience", ""), scholarship.get("level", ""), scholarship.get("focus", ""), scholarship.get("benefit", "")]
        ).casefold()
        if needle and needle not in searchable:
            continue
        if audience != "Semua sasaran" and scholarship.get("audience") != audience:
            continue
        if focus != "Semua kategori" and scholarship.get("focus") != focus:
            continue
        results.append(scholarship)
    return results


def recommend_programs(
    programs: list[dict[str, Any]],
    universities: list[dict[str, Any]],
    profile: dict[str, Any],
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Beri skor kesesuaian berbasis preferensi eksplisit, bukan bakat atau peluang sukses."""
    interests = list(profile.get("interests", []))
    if not interests:
        return []

    preferred_region = profile.get("region", "Bebas lokasi")
    preferred_style = profile.get("style", "Tidak ada preferensi")
    preferred_budget = profile.get("budget", "Tidak ada preferensi")

    max_points = 70
    if preferred_style != "Tidak ada preferensi":
        max_points += 15
    if preferred_region != "Bebas lokasi":
        max_points += 10
    if preferred_budget == "Utamakan biaya terjangkau":
        max_points += 5

    results: list[dict[str, Any]] = []
    for program in programs:
        tags = program.get("interest_tags", [])
        matched_interests = [interest for interest in interests if interest in tags]
        interest_points = round(70 * len(matched_interests) / len(interests))
        earned = interest_points
        criteria = [
            {
                "name": "Minat yang dipilih",
                "points": interest_points,
                "max_points": 70,
                "explanation": (
                    f"{len(matched_interests)} dari {len(interests)} minat yang Anda pilih tercantum pada program ini. "
                    + ("Cocok: " + ", ".join(matched_interests) + "." if matched_interests else "Belum ada tag minat yang cocok secara langsung.")
                ),
            }
        ]

        linked_universities = [u for u in universities if program["id"] in u.get("program_ids", [])]

        if preferred_style != "Tidak ada preferensi":
            points = 15 if preferred_style in program.get("study_styles", []) else 0
            earned += points
            criteria.append({
                "name": "Gaya belajar pilihan",
                "points": points,
                "max_points": 15,
                "explanation": f"Program {'mencantumkan' if points else 'tidak mencantumkan'} gaya '{preferred_style}' pada data contoh.",
            })

        if preferred_region != "Bebas lokasi":
            matches_region = any(u.get("region") == preferred_region for u in linked_universities)
            points = 10 if matches_region else 0
            earned += points
            criteria.append({
                "name": "Ketersediaan di wilayah pilihan",
                "points": points,
                "max_points": 10,
                "explanation": (
                    f"Ada kampus contoh yang mencantumkan program ini di wilayah {preferred_region}."
                    if matches_region else f"Data demo belum mencantumkan kampus dengan program ini di wilayah {preferred_region}."
                ),
            })

        if preferred_budget == "Utamakan biaya terjangkau":
            matches_budget = any(u.get("tuition_band") == "Terjangkau" for u in linked_universities)
            points = 5 if matches_budget else 0
            earned += points
            criteria.append({
                "name": "Preferensi kisaran biaya",
                "points": points,
                "max_points": 5,
                "explanation": (
                    "Ada kampus contoh berlabel 'Terjangkau' untuk program ini. Label tersebut hanya bagian dari data demo."
                    if matches_budget else "Data demo tidak mencantumkan kampus berlabel 'Terjangkau' untuk program ini."
                ),
            })

        score = round(100 * earned / max_points) if max_points else 0
        reasons = [criterion["explanation"] for criterion in criteria]
        # Urutkan kampus relevan dengan wilayah dan biaya pilihan, tanpa mengubah skor jurusan.
        ranked_universities = sorted(
            linked_universities,
            key=lambda u: (
                0 if preferred_region != "Bebas lokasi" and u.get("region") == preferred_region else 1,
                0 if preferred_budget == "Utamakan biaya terjangkau" and u.get("tuition_band") == "Terjangkau" else 1,
                u.get("name", ""),
            ),
        )
        results.append({
            "program": program,
            "score": score,
            "matched_interests": matched_interests,
            "criteria": criteria,
            "reasons": reasons,
            "universities": ranked_universities,
            "earned_points": earned,
            "max_points": max_points,
        })

    results.sort(key=lambda row: (-row["score"], -len(row["matched_interests"]), row["program"]["name"]))
    return results[: max(0, limit)]
