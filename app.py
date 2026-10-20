from __future__ import annotations

import streamlit as st

from fugu_logic import (
    filter_programs,
    filter_scholarships,
    filter_universities,
    load_all_data,
    recommend_programs,
)

st.set_page_config(
    page_title="FuGu — Future Guidance",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
  .stApp { background: #EEF3F8; }
  .block-container { max-width: 1180px; padding-top: 1.35rem; padding-bottom: 3rem; }
  h1, h2, h3 { color: #172B4D; letter-spacing: -0.02em; }
  p, li, label { color: #374151; }
  [data-testid="stMetric"] { background: #F8FAFC; padding: 0.9rem; border: 1px solid #E2E8F0; border-radius: 14px; }
  div[data-testid="stVerticalBlockBorderWrapper"] { background: #FFFFFF; border-color: #DCE4EE; border-radius: 16px; }
  div.stButton > button, div.stFormSubmitButton > button { border-radius: 10px; min-height: 2.65rem; font-weight: 600; }
  div.stButton > button[kind="primary"], div.stFormSubmitButton > button[kind="primary"] { background: #2563EB; border-color: #2563EB; color: white; }
  div.stButton > button:hover, div.stFormSubmitButton > button:hover { border-color: #1D4ED8; color: #1D4ED8; }
  .fugu-brand { font-size: 2.05rem; font-weight: 800; color: #1D4ED8; letter-spacing: -0.06em; margin: 0; }
  .fugu-tagline { margin-top: -0.35rem; color: #64748B; font-size: 0.92rem; }
  .eyebrow { text-transform: uppercase; letter-spacing: .12em; font-size: .75rem; color: #2563EB; font-weight: 700; }
  .hero-copy { color: #526174; max-width: 720px; font-size: 1.06rem; line-height: 1.7; }
  .small-muted { color: #64748B; font-size: .88rem; }
  .tag-pill { display: inline-block; margin: .12rem .18rem .12rem 0; padding: .26rem .58rem; border-radius: 999px; background: #EFF6FF; border: 1px solid #DBEAFE; color: #1D4ED8; font-size: .78rem; }
  .disclaimer { border-left: 4px solid #94A3B8; padding: .65rem .9rem; background: #F8FAFC; color: #475569; border-radius: 0 10px 10px 0; font-size: .88rem; }
  .score-number { color: #1D4ED8; font-size: 1.55rem; font-weight: 800; }
  @media (max-width: 720px) { .block-container { padding-left: 1rem; padding-right: 1rem; } .fugu-brand { font-size: 1.7rem; } }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

INTEREST_OPTIONS = [
    "Teknologi & Komputer",
    "Bisnis & Kewirausahaan",
    "Desain & Kreativitas",
    "Kesehatan & Biologi",
    "Lingkungan & Alam",
    "Sosial & Komunikasi",
    "Pendidikan",
    "Angka & Analisis",
]
REGION_OPTIONS = ["Bebas lokasi", "Jawa", "Sumatera", "Sulawesi", "Bali & Nusa Tenggara"]
STYLE_OPTIONS = ["Tidak ada preferensi", "Praktik & proyek", "Teori & riset"]
BUDGET_OPTIONS = ["Tidak ada preferensi", "Utamakan biaya terjangkau"]


def initialize_state() -> None:
    defaults = {
        "nav": "Home",
        "explore_section": "Kenali Dirimu",
        "profile": None,
        "profile_error": "",
        "selected_program_id": "informatika",
        "program_detail_picker": "informatika",
        "university_program_filter": "Semua program",
        "selected_scholarship_id": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_data_or_stop() -> dict:
    try:
        data = load_all_data()
    except (OSError, ValueError) as exc:
        st.error(f"Data aplikasi tidak bisa dibaca: {exc}")
        st.info("Pastikan folder data/ dan ketiga berkas JSON ada di dalam proyek FuGu.")
        st.stop()
    return data


def start_exploration() -> None:
    st.session_state["nav"] = "Eksplorasi"
    st.session_state["explore_section"] = "Kenali Dirimu"


def go_to_recommendations() -> None:
    st.session_state["nav"] = "Eksplorasi"
    st.session_state["explore_section"] = "Rekomendasi"


def go_to_program_detail(program_id: str) -> None:
    st.session_state["selected_program_id"] = program_id
    st.session_state["program_detail_picker"] = program_id
    st.session_state["explore_section"] = "Detail Program"
    st.session_state["nav"] = "Eksplorasi"


def go_to_universities(program_id: str = "Semua program") -> None:
    st.session_state["university_program_filter"] = program_id
    st.session_state["explore_section"] = "Universitas Pilihan"
    st.session_state["nav"] = "Eksplorasi"


def go_to_quiz() -> None:
    st.session_state["explore_section"] = "Kenali Dirimu"
    st.session_state["nav"] = "Eksplorasi"


def save_profile() -> None:
    interests = st.session_state.get("profile_interests", [])
    if not interests:
        st.session_state["profile_error"] = "Pilih setidaknya satu bidang minat agar rekomendasi bisa dihitung."
        return
    st.session_state["profile"] = {
        "interests": list(interests),
        "region": st.session_state.get("profile_region", "Bebas lokasi"),
        "budget": st.session_state.get("profile_budget", "Tidak ada preferensi"),
        "style": st.session_state.get("profile_style", "Tidak ada preferensi"),
    }
    st.session_state["profile_error"] = ""
    st.session_state["explore_section"] = "Rekomendasi"


def tag_line(tags: list[str]) -> str:
    if not tags:
        return ""
    return " ".join(f'<span class="tag-pill">{tag}</span>' for tag in tags)


def disclaimer() -> None:
    st.markdown(
        '<div class="disclaimer"><strong>Catatan data demo:</strong> FuGu versi ini menggunakan data ilustratif. '
        "Nama kampus, kisaran biaya, dan beasiswa pada aplikasi adalah contoh untuk menguji fitur—bukan informasi resmi. "
        "Rekomendasi hanya mencocokkan preferensi yang Anda masukkan; bukan pengukuran bakat, jaminan hasil studi, atau prediksi kelulusan.</div>",
        unsafe_allow_html=True,
    )


def render_home(data: dict) -> None:
    left, right = st.columns([1.45, 1], gap="large")
    with left:
        st.markdown('<div class="eyebrow">Future Guidance</div>', unsafe_allow_html=True)
        st.title("Temukan arah kuliah yang terasa cocok untukmu.")
        st.markdown(
            '<p class="hero-copy">FuGu membantu kamu mengeksplorasi bidang minat, mengenal pilihan program studi, '
            "membandingkan kampus contoh, dan membaca ringkasan beasiswa—selangkah demi selangkah.</p>",
            unsafe_allow_html=True,
        )
        st.button("Mulai Eksplorasi", type="primary", on_click=start_exploration, key="home_start")
        st.caption("Tidak perlu mengetahui jurusan tujuan sejak awal. Mulai dari hal yang menarik perhatianmu.")
    with right:
        with st.container(border=True):
            st.markdown("### Mulai dari rasa ingin tahu")
            st.markdown("Pilih minat yang ingin kamu pelajari lebih jauh. Tidak ada jawaban benar atau salah.")
            st.markdown("**01 · Kenali diri**  \nTentukan minat dan preferensi belajar.")
            st.markdown("**02 · Bandingkan opsi**  \nCari jurusan dan kampus contoh dengan filter.")
            st.markdown("**03 · Pahami alasannya**  \nBaca komponen skor rekomendasi satu per satu.")
    st.write("")
    st.subheader("Jelajahi FuGu")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        with st.container(border=True):
            st.markdown("### 🧭 Kenali Dirimu")
            st.write("Mulai dari beberapa bidang yang membuatmu penasaran.")
            st.button("Pilih minat", on_click=start_exploration, key="home_interests")
    with c2:
        with st.container(border=True):
            st.markdown("### 🎓 Eksplorasi Jurusan")
            st.write(f"Telusuri {len(data['programs'])} program contoh dengan pencarian dan filter.")
            st.button("Cari jurusan", on_click=lambda: st.session_state.update({"nav": "Eksplorasi", "explore_section": "Jelajah Jurusan"}), key="home_programs")
    with c3:
        with st.container(border=True):
            st.markdown("### 🌱 Informasi Beasiswa")
            st.write("Baca contoh kategori bantuan dan dokumen yang umum perlu diperiksa.")
            st.button("Lihat beasiswa", on_click=lambda: st.session_state.update({"nav": "Beasiswa"}), key="home_scholarships")
    if st.session_state.get("profile"):
        st.write("")
        st.success("Kamu sudah mengisi preferensi sebelumnya di sesi ini.")
        st.button("Lihat rekomendasi terakhir", on_click=go_to_recommendations, key="home_saved_recs")
    st.write("")
    disclaimer()


def render_quiz() -> None:
    st.subheader("Kenali Dirimu")
    st.write("Pilih minat dan preferensi yang paling mendekati keinginanmu saat ini. Kamu boleh mengubahnya kapan saja.")
    with st.form("profile_form", border=True):
        st.markdown("#### Bidang yang ingin kamu eksplorasi")
        st.multiselect(
            "Pilih satu atau beberapa bidang minat",
            options=INTEREST_OPTIONS,
            key="profile_interests",
            placeholder="Contoh: Teknologi & Komputer",
            help="Pilihan ini digunakan untuk menghitung kecocokan tag minat pada data program contoh.",
        )
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Wilayah kampus yang disukai", REGION_OPTIONS, key="profile_region")
            st.selectbox("Kisaran biaya", BUDGET_OPTIONS, key="profile_budget")
        with col2:
            st.selectbox("Gaya belajar", STYLE_OPTIONS, key="profile_style")
        st.caption("Pilihan lokasi dan biaya hanya dicocokkan dengan data kampus fiktif di aplikasi ini.")
        st.form_submit_button("Buat Rekomendasi", type="primary", on_click=save_profile, use_container_width=True)
    if st.session_state.get("profile_error"):
        st.error(st.session_state["profile_error"])
    with st.expander("Bagaimana profil ini digunakan?"):
        st.write("Minat yang dipilih dibandingkan dengan tag program. Preferensi gaya belajar, wilayah, dan biaya menambah komponen skor jika kamu menetapkannya. Tidak ada data pribadi yang diminta untuk menghitung rekomendasi.")


def render_program_explorer(data: dict) -> None:
    programs = data["programs"]
    st.subheader("Eksplorasi Jurusan")
    st.write("Cari berdasarkan nama, bidang, mata kuliah contoh, atau gambaran karier. Gunakan filter untuk mempersempit hasil.")
    fields = ["Semua bidang"] + sorted({p["field"] for p in programs})
    interests = ["Semua minat"] + INTEREST_OPTIONS
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        query = st.text_input("Cari jurusan", placeholder="Misalnya: data, desain, kesehatan", key="program_query")
    with col2:
        selected_field = st.selectbox("Bidang", fields, key="program_field_filter")
    with col3:
        level = st.selectbox("Jenjang", ["Semua jenjang", "S1", "D4"], key="program_level_filter")
    interest = st.selectbox("Filter minat", interests, key="program_interest_filter")
    filtered = filter_programs(programs, query, selected_field, level, interest)
    st.caption(f"Menampilkan {len(filtered)} dari {len(programs)} program contoh.")
    if not filtered:
        st.info("Belum ada program yang cocok dengan filter tersebut. Coba ubah kata pencarian atau pilih Semua.")
        return
    for program in filtered:
        with st.container(border=True):
            st.markdown(f"### {program['name']}")
            st.caption(f"{program['field']} · {program['level']} · {program['duration']}")
            st.write(program["summary"])
            st.markdown(tag_line(program.get("interest_tags", [])), unsafe_allow_html=True)
            st.write("")
            st.button("Lihat Detail Program", key=f"program_details_{program['id']}", on_click=go_to_program_detail, args=(program["id"],), type="primary")


def render_program_detail(data: dict) -> None:
    programs = data["programs"]
    universities = data["universities"]
    lookup = {p["id"]: p for p in programs}
    ids = list(lookup.keys())
    selected_id = st.session_state.get("selected_program_id", ids[0])
    if selected_id not in lookup:
        selected_id = ids[0]
    st.subheader("Detail Program Studi")
    current_index = ids.index(selected_id)
    selected_id = st.selectbox(
        "Pilih program studi",
        options=ids,
        index=current_index,
        format_func=lambda pid: lookup[pid]["name"],
        key="program_detail_picker",
    )
    st.session_state["selected_program_id"] = selected_id
    program = lookup[selected_id]
    with st.container(border=True):
        st.markdown(f"## {program['name']}")
        a, b, c = st.columns(3)
        a.metric("Jenjang contoh", program["level"])
        b.metric("Durasi referensi", program["duration"].split(" ")[0])
        c.metric("Bidang", program["field"])
        st.markdown("### Gambaran singkat")
        st.write(program["summary"])
        st.markdown("### Minat yang terhubung pada data")
        st.markdown(tag_line(program.get("interest_tags", [])), unsafe_allow_html=True)
        st.markdown("### Mata kuliah contoh")
        for subject in program.get("subjects", []):
            st.markdown(f"- {subject}")
        st.markdown("### Contoh arah karier")
        st.write("Karier dipengaruhi keterampilan, pengalaman, sertifikasi, dan kebutuhan pasar kerja; contoh ini bukan jaminan hasil.")
        for career in program.get("career_examples", []):
            st.markdown(f"- {career}")
        offering = [u for u in universities if program["id"] in u.get("program_ids", [])]
        st.markdown("### Kampus dalam data demo")
        if offering:
            for university in offering:
                st.markdown(f"- **{university['name']}** — {university['city']}, {university['region']}; kisaran biaya: {university['tuition_band']} (simulasi)")
        else:
            st.info("Belum ada kampus contoh yang ditautkan ke program ini.")
    c1, c2 = st.columns(2)
    with c1:
        st.button("Cari kampus untuk program ini", type="primary", on_click=go_to_universities, args=(program["id"],), key="detail_find_universities")
    with c2:
        st.button("Kembali ke daftar jurusan", on_click=lambda: st.session_state.update({"explore_section": "Jelajah Jurusan"}), key="detail_back_programs")
    st.caption("Nama institusi, data program, durasi, dan kisaran biaya di proyek ini adalah ilustrasi untuk demo, bukan basis data pendidikan resmi.")


def render_universities(data: dict) -> None:
    universities = data["universities"]
    programs = data["programs"]
    program_lookup = {p["id"]: p for p in programs}
    st.subheader("Temukan Universitas Pilihanmu")
    st.write("Bandingkan kampus fiktif berdasarkan wilayah, kisaran biaya contoh, dan program studi yang tercantum.")
    col1, col2, col3 = st.columns([1.5, 1, 1])
    with col1:
        query = st.text_input("Cari kampus atau kota", placeholder="Misalnya: Surakarta", key="university_query")
    with col2:
        region = st.selectbox("Wilayah", ["Semua wilayah", "Jawa", "Sumatera", "Sulawesi", "Bali & Nusa Tenggara"], key="university_region_filter")
    with col3:
        cost = st.selectbox("Kisaran biaya demo", ["Semua kisaran", "Terjangkau", "Menengah", "Fleksibel"], key="university_cost_filter")
    selected_program = st.selectbox(
        "Program yang tersedia",
        options=["Semua program"] + list(program_lookup.keys()),
        format_func=lambda pid: "Semua program" if pid == "Semua program" else program_lookup[pid]["name"],
        key="university_program_filter",
    )
    filtered = filter_universities(universities, query, region, cost, selected_program)
    st.caption(f"Menampilkan {len(filtered)} dari {len(universities)} kampus contoh.")
    if not filtered:
        st.info("Tidak ada kampus contoh yang cocok. Coba ubah filter wilayah, biaya, atau program.")
        return
    for university in filtered:
        with st.container(border=True):
            st.markdown(f"### {university['name']}")
            st.caption(f"{university['city']} · {university['region']} · Kisaran biaya demo: {university['tuition_band']}")
            st.write(university["description"])
            offered = [program_lookup[pid]["name"] for pid in university.get("program_ids", []) if pid in program_lookup]
            st.markdown("**Program contoh:** " + (", ".join(offered) if offered else "Belum ditentukan"))
            first_program_id = university.get("program_ids", [None])[0]
            if first_program_id:
                st.button("Lihat salah satu program", key=f"uni_program_{university['id']}", on_click=go_to_program_detail, args=(first_program_id,))


def render_recommendations(data: dict) -> None:
    profile = st.session_state.get("profile")
    st.subheader("Hasil Rekomendasi Jurusan")
    if not profile:
        st.info("Isi minat dan preferensi terlebih dahulu untuk melihat rekomendasi yang dapat dijelaskan.")
        st.button("Isi Kenali Dirimu", on_click=go_to_quiz, type="primary", key="recommendations_go_quiz")
        return
    st.markdown("**Profil yang digunakan**")
    st.markdown(tag_line(profile["interests"]), unsafe_allow_html=True)
    details = []
    details.append(f"Wilayah: {profile['region']}")
    details.append(f"Kisaran biaya: {profile['budget']}")
    details.append(f"Gaya belajar: {profile['style']}")
    st.caption(" · ".join(details))
    results = recommend_programs(data["programs"], data["universities"], profile, limit=6)
    if not results:
        st.info("Pilih minimal satu bidang minat untuk menghitung rekomendasi.")
        st.button("Ubah preferensi", on_click=go_to_quiz, key="recs_empty_edit")
        return
    st.markdown("### Pilihan untuk dipertimbangkan")
    st.write("Urutan di bawah hanya menunjukkan seberapa cocok data program contoh dengan preferensi yang kamu pilih.")
    for index, result in enumerate(results, start=1):
        program = result["program"]
        with st.container(border=True):
            left, right = st.columns([4, 1])
            with left:
                st.markdown(f"### {index}. {program['name']}")
                st.caption(f"{program['field']} · {program['level']}")
                st.write(program["summary"])
                st.markdown(tag_line(program.get("interest_tags", [])), unsafe_allow_html=True)
            with right:
                st.markdown(f'<div class="score-number">{result["score"]}%</div>', unsafe_allow_html=True)
                st.caption("Kecocokan preferensi")
            st.progress(result["score"] / 100, text="Skor kecocokan dari kriteria yang dipilih")
            with st.expander("Mengapa jurusan ini direkomendasikan?", expanded=(index == 1)):
                for criterion in result["criteria"]:
                    st.markdown(f"**{criterion['name']}: {criterion['points']}/{criterion['max_points']} poin**")
                    st.write(criterion["explanation"])
                st.caption(f"Perhitungan: {result['earned_points']} poin dari maksimum {result['max_points']} poin untuk kriteria yang diisi, dikonversi ke skala 0–100.")
                if result["universities"]:
                    st.markdown("**Kampus contoh yang mencantumkan program ini:**")
                    for university in result["universities"][:3]:
                        st.markdown(f"- {university['name']} — {university['region']}, kisaran biaya demo {university['tuition_band']}")
            st.button("Buka Detail Program", key=f"rec_detail_{program['id']}", on_click=go_to_program_detail, args=(program["id"],))
    st.write("")
    st.button("Ubah minat atau preferensi", on_click=go_to_quiz, key="recs_edit_profile")
    st.markdown(
        '<div class="disclaimer"><strong>Makna skor:</strong> angka ini bukan skor kecerdasan, bakat, prospek kerja, '
        "atau peluang diterima. Skor hanya merangkum kecocokan pilihanmu dengan tag dan atribut pada data contoh FuGu.</div>",
        unsafe_allow_html=True,
    )


def render_exploration(data: dict) -> None:
    st.title("Ruang Eksplorasi")
    sections = ["Kenali Dirimu", "Jelajah Jurusan", "Detail Program", "Universitas Pilihan", "Rekomendasi"]
    selected = st.radio("Bagian eksplorasi", sections, horizontal=True, key="explore_section", label_visibility="collapsed")
    st.divider()
    if selected == "Kenali Dirimu":
        render_quiz()
    elif selected == "Jelajah Jurusan":
        render_program_explorer(data)
    elif selected == "Detail Program":
        render_program_detail(data)
    elif selected == "Universitas Pilihan":
        render_universities(data)
    elif selected == "Rekomendasi":
        render_recommendations(data)
    st.write("")
    disclaimer()


def render_scholarships(data: dict) -> None:
    scholarships = data["scholarships"]
    st.title("Informasi Beasiswa")
    st.write("Gunakan pencarian dan filter untuk menjelajahi contoh kategori bantuan pendidikan. Data berikut hanya untuk demonstrasi antarmuka.")
    col1, col2, col3 = st.columns([2, 1, 1])
    audiences = ["Semua sasaran"] + sorted({item["audience"] for item in scholarships})
    focuses = ["Semua kategori"] + sorted({item["focus"] for item in scholarships})
    with col1:
        query = st.text_input("Cari beasiswa", placeholder="Nama, prestasi, kreatif, sains...", key="scholarship_query")
    with col2:
        audience = st.selectbox("Sasaran", audiences, key="scholarship_audience_filter")
    with col3:
        focus = st.selectbox("Kategori", focuses, key="scholarship_focus_filter")
    filtered = filter_scholarships(scholarships, query, audience, focus)
    st.caption(f"Menampilkan {len(filtered)} dari {len(scholarships)} beasiswa contoh.")
    if not filtered:
        st.info("Tidak ditemukan contoh beasiswa dengan filter tersebut. Coba ubah kata kunci atau pilih Semua.")
    for scholarship in filtered:
        with st.container(border=True):
            st.markdown(f"### {scholarship['name']}")
            st.caption(f"Sasaran: {scholarship['audience']} · Jenjang: {scholarship['level']} · Kategori: {scholarship['focus']}")
            st.write(scholarship["benefit"])
            st.markdown(f"**Batas waktu dalam data demo:** {scholarship['deadline']}")
            with st.expander("Lihat contoh kriteria dan dokumen", expanded=(st.session_state.get("selected_scholarship_id") == scholarship["id"])):
                st.markdown("**Kriteria ilustratif**")
                for item in scholarship["eligibility"]:
                    st.markdown(f"- {item}")
                st.markdown("**Contoh dokumen yang mungkin diminta**")
                for item in scholarship["documents"]:
                    st.markdown(f"- {item}")
            st.button(
                "Tandai untuk dibaca",
                key=f"scholarship_mark_{scholarship['id']}",
                on_click=lambda scholarship_id=scholarship["id"]: st.session_state.update({"selected_scholarship_id": scholarship_id}),
            )
    st.write("")
    st.markdown(
        '<div class="disclaimer"><strong>Periksa sumber resmi:</strong> semua nama, manfaat, kriteria, dan tenggat beasiswa '
        "pada halaman ini merupakan contoh fiktif. Sebelum mendaftar program nyata, pastikan penyelenggara, ketentuan, tenggat, "
        "dan dokumen melalui situs atau kanal resmi penyelenggara.</div>",
        unsafe_allow_html=True,
    )


def main() -> None:
    initialize_state()
    data = load_data_or_stop()
    header_left, header_right = st.columns([1.3, 4])
    with header_left:
        st.markdown('<p class="fugu-brand">FuGu</p><p class="fugu-tagline">Future Guidance</p>', unsafe_allow_html=True)
    with header_right:
        st.radio(
            "Navigasi utama",
            options=["Home", "Eksplorasi", "Beasiswa"],
            horizontal=True,
            key="nav",
            label_visibility="collapsed",
        )
    st.divider()
    nav = st.session_state["nav"]
    if nav == "Home":
        render_home(data)
    elif nav == "Eksplorasi":
        render_exploration(data)
    elif nav == "Beasiswa":
        render_scholarships(data)
    else:
        st.session_state["nav"] = "Home"
        render_home(data)
    st.divider()
    st.caption("FuGu · prototipe pembelajaran · data contoh · bukan konsultasi penerimaan atau beasiswa resmi")


if __name__ == "__main__":
    main()
