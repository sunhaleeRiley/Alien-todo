import streamlit as st
import json
import uuid
from datetime import datetime
from pathlib import Path

# ── 페이지 설정 ────────────────────────────────────────────────────
st.set_page_config(
    page_title="👽 Alien Mission Control",
    page_icon="👽",
    layout="centered",
)

# ── 데이터 영속성: JSON 파일 ───────────────────────────────────────
DATA_FILE = Path("todos_data.json")

def load_data():
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {"todos": [], "lang": "ko"}

def save_data(todos, lang):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"todos": todos, "lang": lang}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ── i18n ──────────────────────────────────────────────────────────
I18N = {
    "ko": {
        "app_title":       "👾 외계인 임무 관리 본부",
        "app_subtitle":    "지구 정복 전에 할일부터 처리하자",
        "lbl_total":       "전체 임무",
        "lbl_done":        "완료",
        "lbl_remain":      "남은 임무",
        "lbl_rate":        "달성률",
        "lbl_progress":    "임무 진행률",
        "prog_text":       lambda d, t: f"{d} / {t} 완료",
        "placeholder":     "새 임무를 입력하세요...",
        "lbl_add":         "추가",
        "cat_work":        "💼 업무",
        "cat_personal":    "🏠 개인",
        "cat_study":       "📚 공부",
        "filter_all":      "전체",
        "filter_work":     "💼 업무",
        "filter_personal": "🏠 개인",
        "filter_study":    "📚 공부",
        "filter_done":     "✅ 완료만",
        "filter_todo":     "⏳ 미완료만",
        "empty_all":       "👽 아직 임무가 없어요. 지구 정복 계획을 세워봐요!",
        "empty_filter":    "👽 해당 조건의 임무가 없어요.",
        "save_label":      "저장",
        "cancel_label":    "취소",
        "delete_label":    "삭제",
        "edit_label":      "수정",
        "cat_labels":      {"work": "💼 업무", "personal": "🏠 개인", "study": "📚 공부"},
    },
    "en": {
        "app_title":       "👾 Alien Mission Control",
        "app_subtitle":    "Conquer your tasks before conquering Earth",
        "lbl_total":       "Total",
        "lbl_done":        "Done",
        "lbl_remain":      "Remaining",
        "lbl_rate":        "Progress",
        "lbl_progress":    "Mission Progress",
        "prog_text":       lambda d, t: f"{d} / {t} done",
        "placeholder":     "Enter a new mission...",
        "lbl_add":         "Add",
        "cat_work":        "💼 Work",
        "cat_personal":    "🏠 Personal",
        "cat_study":       "📚 Study",
        "filter_all":      "All",
        "filter_work":     "💼 Work",
        "filter_personal": "🏠 Personal",
        "filter_study":    "📚 Study",
        "filter_done":     "✅ Done",
        "filter_todo":     "⏳ Pending",
        "empty_all":       "👽 No missions yet. Plan your Earth conquest!",
        "empty_filter":    "👽 No missions match this filter.",
        "save_label":      "Save",
        "cancel_label":    "Cancel",
        "delete_label":    "Delete",
        "edit_label":      "Edit",
        "cat_labels":      {"work": "💼 Work", "personal": "🏠 Personal", "study": "📚 Study"},
    },
}

CAT_COLORS = {
    "work":     {"bg": "#EEEDFE", "text": "#3C3489", "btn": "#534AB7"},
    "personal": {"bg": "#E1F5EE", "text": "#085041", "btn": "#0F6E56"},
    "study":    {"bg": "#E6F1FB", "text": "#0C447C", "btn": "#185FA5"},
}

# ── 세션 상태 초기화 ───────────────────────────────────────────────
if "initialized" not in st.session_state:
    data = load_data()
    st.session_state.todos        = data.get("todos", [])
    st.session_state.lang         = data.get("lang", "ko")
    st.session_state.selected_cat = "work"
    st.session_state.current_filter = "all"
    st.session_state.editing_id   = None
    st.session_state.initialized  = True

T = I18N[st.session_state.lang]

# ── 전역 CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── 전체 배경 & 레이아웃 ── */
.stApp { background: #F5F5F3 !important; }
.block-container {
    max-width: 720px !important;
    padding: 2rem 1.5rem 4rem !important;
}

/* Streamlit 기본 헤더/푸터 숨기기 */
#MainMenu, footer, header { visibility: hidden; height: 0; }
.stDeployButton { display: none; }

/* ── 공통 카드 ── */
.card {
    background: white;
    border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
}

/* ── 헤더 카드 ── */
.header-card {
    background: white;
    border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 14px;
}
/* CSS 외계인 얼굴 */
.alien-head {
    width: 52px; height: 52px;
    background: #7BC62D;
    border-radius: 50%;
    border: 2.5px solid #5A9E1A;
    flex-shrink: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 4px; position: relative;
}
.alien-head::before {
    content: '';
    position: absolute; top: -12px; left: 50%;
    transform: translateX(-50%);
    width: 3px; height: 13px;
    background: #5A9E1A; border-radius: 3px 3px 0 0;
}
.alien-head::after {
    content: '';
    position: absolute; top: -14px; left: 50%;
    transform: translateX(-50%);
    width: 6px; height: 6px;
    background: #5A9E1A; border-radius: 50%;
}
.alien-eyes { display: flex; gap: 5px; align-items: center; }
.eye { background: white; border-radius: 50%; position: relative; }
.eye::after {
    content: ''; position: absolute;
    background: #1a1a2e; border-radius: 50%;
    top: 30%; left: 25%; width: 50%; height: 50%;
}
.eye.sm { width: 9px; height: 9px; }
.eye.lg { width: 12px; height: 12px; }
.alien-mouth {
    width: 18px; height: 4px;
    background: #5A9E1A; border-radius: 0 0 8px 8px;
}
.header-title {
    font-size: 19px; font-weight: 700;
    color: #2C2C2A; line-height: 1.25; margin: 0;
}
.header-sub {
    font-size: 12px; color: #888780; margin-top: 2px;
}

/* ── 통계 그리드 ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px; margin-bottom: 1rem;
}
.stat-box {
    background: white;
    border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 12px;
    padding: 0.8rem 0.5rem;
    text-align: center;
}
.stat-n { font-size: 26px; font-weight: 700; color: #2C2C2A; line-height: 1; }
.stat-l { font-size: 11px; color: #888780; margin-top: 4px; }

/* ── 프로그레스 바 ── */
.prog-card {
    background: white;
    border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin-bottom: 1rem;
}
.prog-row {
    display: flex; justify-content: space-between;
    font-size: 12px; color: #888780; margin-bottom: 8px;
}
.prog-track {
    height: 10px; background: #F0F0EE;
    border-radius: 20px; overflow: hidden;
}
.prog-fill {
    height: 100%; background: #7BC62D;
    border-radius: 20px; transition: width 0.4s ease;
}

/* ── 할일 카드 ── */
.todo-row {
    background: white;
    border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin-bottom: 7px;
    display: flex; align-items: center; gap: 10px;
    transition: box-shadow 0.15s;
}
.todo-row:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.todo-row.done { opacity: 0.5; }
.todo-text-done { text-decoration: line-through; color: #aaa; }
.cat-pill {
    display: inline-block; padding: 3px 9px;
    border-radius: 20px; font-size: 11px;
    white-space: nowrap; font-weight: 500;
}

/* ── 빈 상태 ── */
.empty-box {
    background: white;
    border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 14px;
    padding: 3rem 1rem; text-align: center;
    color: #888780; font-size: 14px;
}

/* ── 섹션 구분선 제거 ── */
hr { display: none !important; }
[data-testid="stVerticalBlock"] > [style*="flex-direction: column"] > [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* ── 버튼 기본 초기화 ── */
.stButton button {
    border-radius: 20px !important;
    border: 0.5px solid rgba(0,0,0,0.12) !important;
    background: white !important;
    color: #666 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 5px 14px !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
    line-height: 1.4 !important;
    width: 100%;
}
.stButton button:hover {
    background: #F0F0EE !important;
    border-color: rgba(0,0,0,0.2) !important;
}
.stButton button:focus { box-shadow: none !important; outline: none !important; }

/* ── 추가 버튼 ── */
.btn-add .stButton button {
    background: #7BC62D !important;
    color: white !important;
    border-color: #7BC62D !important;
    font-weight: 700 !important;
    font-size: 14px !important;
}
.btn-add .stButton button:hover { background: #6ab526 !important; }

/* ── 언어 버튼 active ── */
.btn-lang-active .stButton button {
    background: #7BC62D !important;
    color: white !important;
    border-color: #7BC62D !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    padding: 3px 12px !important;
}
.btn-lang .stButton button {
    font-size: 12px !important;
    font-weight: 700 !important;
    padding: 3px 12px !important;
    color: #888 !important;
}

/* ── 필터 버튼 active ── */
.btn-filter-active .stButton button {
    background: #7BC62D !important;
    color: white !important;
    border-color: #7BC62D !important;
    font-size: 12px !important;
    padding: 4px 10px !important;
}
.btn-filter .stButton button {
    font-size: 12px !important;
    padding: 4px 10px !important;
}

/* ── 카테고리 버튼 active ── */
.btn-cat-work-active .stButton button {
    background: #534AB7 !important; color: white !important; border-color: #534AB7 !important;
}
.btn-cat-personal-active .stButton button {
    background: #0F6E56 !important; color: white !important; border-color: #0F6E56 !important;
}
.btn-cat-study-active .stButton button {
    background: #185FA5 !important; color: white !important; border-color: #185FA5 !important;
}

/* ── 완료 체크 버튼 ── */
.btn-check-done .stButton button {
    background: #7BC62D !important; color: white !important;
    border-color: #7BC62D !important;
    border-radius: 50% !important;
    width: 28px !important; height: 28px !important;
    padding: 0 !important; font-size: 13px !important;
    min-width: 28px !important; min-height: 28px !important;
}
.btn-check-undone .stButton button {
    background: white !important; color: transparent !important;
    border: 2px solid #CCC !important;
    border-radius: 50% !important;
    width: 28px !important; height: 28px !important;
    padding: 0 !important;
    min-width: 28px !important; min-height: 28px !important;
}
.btn-check-undone .stButton button:hover {
    border-color: #7BC62D !important;
}

/* ── 삭제 버튼 ── */
.btn-del .stButton button {
    background: transparent !important; color: #BBB !important;
    border: none !important; padding: 2px 6px !important;
    font-size: 15px !important;
}
.btn-del .stButton button:hover {
    color: #E24B4A !important; background: #FEF0F0 !important;
}

/* ── 수정/저장/취소 버튼 ── */
.btn-edit .stButton button {
    background: transparent !important; color: #AAA !important;
    border: none !important; font-size: 14px !important;
    padding: 2px 6px !important;
}
.btn-edit .stButton button:hover { color: #555 !important; background: #F0F0EE !important; }

.btn-save .stButton button {
    background: #7BC62D !important; color: white !important;
    border-color: #7BC62D !important; font-size: 13px !important;
}
.btn-cancel .stButton button {
    background: white !important; color: #888 !important;
    font-size: 13px !important;
}

/* ── 텍스트 입력 ── */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 0.5px solid rgba(0,0,0,0.15) !important;
    background: #F8F8F6 !important;
    color: #2C2C2A !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7BC62D !important;
    background: white !important;
    box-shadow: 0 0 0 2px rgba(123,198,45,0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: #BBB !important; }
.stTextInput label { display: none !important; }

/* ── 갭 제거 ── */
div[data-testid="column"] { padding: 0 3px !important; }
.element-container { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── 헬퍼 ──────────────────────────────────────────────────────────
def persist():
    save_data(st.session_state.todos, st.session_state.lang)

def add_todo(text):
    if not text.strip():
        return False
    st.session_state.todos.insert(0, {
        "id":   str(uuid.uuid4()),
        "text": text.strip()[:80],
        "cat":  st.session_state.selected_cat,
        "done": False,
    })
    persist()
    return True

def toggle_todo(tid):
    for t in st.session_state.todos:
        if t["id"] == tid:
            t["done"] = not t["done"]
            break
    persist()

def delete_todo(tid):
    st.session_state.todos = [t for t in st.session_state.todos if t["id"] != tid]
    persist()

def update_todo(tid, new_text):
    for t in st.session_state.todos:
        if t["id"] == tid:
            t["text"] = new_text.strip()[:80]
            break
    persist()

def get_filtered():
    f = st.session_state.current_filter
    todos = st.session_state.todos
    if f == "work":     return [t for t in todos if t["cat"] == "work"]
    if f == "personal": return [t for t in todos if t["cat"] == "personal"]
    if f == "study":    return [t for t in todos if t["cat"] == "study"]
    if f == "done":     return [t for t in todos if t["done"]]
    if f == "todo":     return [t for t in todos if not t["done"]]
    return todos


# ════════════════════════════════════════════════════════════════════
# 렌더링
# ════════════════════════════════════════════════════════════════════

# ── 헤더 + 언어 토글 ─────────────────────────────────────────────
h_col, lang_col = st.columns([7, 3])

with h_col:
    st.markdown(f"""
    <div class="header-card">
      <div class="alien-head">
        <div class="alien-eyes">
          <div class="eye sm"></div>
          <div class="eye lg"></div>
          <div class="eye sm"></div>
        </div>
        <div class="alien-mouth"></div>
      </div>
      <div>
        <div class="header-title">{T["app_title"]}</div>
        <div class="header-sub">{T["app_subtitle"]}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with lang_col:
    st.write("")
    lc1, lc2 = st.columns(2)
    with lc1:
        cls = "btn-lang-active" if st.session_state.lang == "ko" else "btn-lang"
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button("KO", key="btn_ko"):
            st.session_state.lang = "ko"
            persist()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with lc2:
        cls = "btn-lang-active" if st.session_state.lang == "en" else "btn-lang"
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button("EN", key="btn_en"):
            st.session_state.lang = "en"
            persist()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── 통계 카드 ─────────────────────────────────────────────────────
total  = len(st.session_state.todos)
done_n = sum(1 for t in st.session_state.todos if t["done"])
remain = total - done_n
pct    = round(done_n / total * 100) if total else 0

st.markdown(f"""
<div class="stats-row">
  <div class="stat-box"><div class="stat-n">{total}</div><div class="stat-l">{T["lbl_total"]}</div></div>
  <div class="stat-box"><div class="stat-n">{done_n}</div><div class="stat-l">{T["lbl_done"]}</div></div>
  <div class="stat-box"><div class="stat-n">{remain}</div><div class="stat-l">{T["lbl_remain"]}</div></div>
  <div class="stat-box"><div class="stat-n">{pct}%</div><div class="stat-l">{T["lbl_rate"]}</div></div>
</div>
""", unsafe_allow_html=True)

# ── 프로그레스 바 ─────────────────────────────────────────────────
st.markdown(f"""
<div class="prog-card">
  <div class="prog-row">
    <span>{T["lbl_progress"]}</span>
    <span>{T["prog_text"](done_n, total)}</span>
  </div>
  <div class="prog-track">
    <div class="prog-fill" style="width:{pct}%"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 입력 영역 ─────────────────────────────────────────────────────
with st.container():
    ic, bc = st.columns([8, 2])
    with ic:
        new_text = st.text_input(
            "task", label_visibility="collapsed",
            placeholder=T["placeholder"],
            key="new_task_input", max_chars=80,
        )
    with bc:
        st.markdown('<div class="btn-add">', unsafe_allow_html=True)
        if st.button(f"＋ {T['lbl_add']}", key="add_btn", use_container_width=True):
            if add_todo(new_text):
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 카테고리 버튼
    cats = [("work", T["cat_work"]), ("personal", T["cat_personal"]), ("study", T["cat_study"])]
    cc = st.columns(3)
    for col, (ckey, clabel) in zip(cc, cats):
        with col:
            is_act = st.session_state.selected_cat == ckey
            cls = f"btn-cat-{ckey}-active" if is_act else "btn-filter"
            st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
            if st.button(clabel, key=f"cat_{ckey}", use_container_width=True):
                st.session_state.selected_cat = ckey
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# ── 필터 ──────────────────────────────────────────────────────────
filters = [
    ("all",      T["filter_all"]),
    ("work",     T["filter_work"]),
    ("personal", T["filter_personal"]),
    ("study",    T["filter_study"]),
    ("done",     T["filter_done"]),
    ("todo",     T["filter_todo"]),
]
fc = st.columns(len(filters))
for col, (fkey, flabel) in zip(fc, filters):
    with col:
        is_act = st.session_state.current_filter == fkey
        cls = "btn-filter-active" if is_act else "btn-filter"
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button(flabel, key=f"f_{fkey}", use_container_width=True):
            st.session_state.current_filter = fkey
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# ── 할일 목록 ─────────────────────────────────────────────────────
filtered = get_filtered()

if not filtered:
    msg = T["empty_all"] if not st.session_state.todos else T["empty_filter"]
    st.markdown(f'<div class="empty-box">{msg}</div>', unsafe_allow_html=True)
else:
    for todo in filtered:
        cc = CAT_COLORS[todo["cat"]]
        clabel = T["cat_labels"][todo["cat"]]
        is_done = todo["done"]

        if st.session_state.editing_id == todo["id"]:
            # 편집 모드
            ec, sc, xc = st.columns([7, 1.5, 1.5])
            with ec:
                edited = st.text_input(
                    "edit", label_visibility="collapsed",
                    value=todo["text"],
                    key=f"ei_{todo['id']}", max_chars=80,
                )
            with sc:
                st.markdown('<div class="btn-save">', unsafe_allow_html=True)
                if st.button(T["save_label"], key=f"sv_{todo['id']}", use_container_width=True):
                    if edited.strip():
                        update_todo(todo["id"], edited)
                    st.session_state.editing_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with xc:
                st.markdown('<div class="btn-cancel">', unsafe_allow_html=True)
                if st.button(T["cancel_label"], key=f"cx_{todo['id']}", use_container_width=True):
                    st.session_state.editing_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            # 일반 모드
            chk, txt, badge, edt, dlt = st.columns([1, 5.5, 2, 0.8, 0.8])

            with chk:
                cls = "btn-check-done" if is_done else "btn-check-undone"
                st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                if st.button("✓" if is_done else " ", key=f"ck_{todo['id']}"):
                    toggle_todo(todo["id"])
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with txt:
                style = "text-decoration:line-through;color:#aaa;" if is_done else "color:#2C2C2A;"
                st.markdown(
                    f'<div style="padding:5px 0;font-size:14px;line-height:1.4;{style}">'
                    f'{todo["text"]}</div>',
                    unsafe_allow_html=True
                )

            with badge:
                st.markdown(
                    f'<div style="padding:5px 0;">'
                    f'<span class="cat-pill" style="background:{cc["bg"]};color:{cc["text"]}">'
                    f'{clabel}</span></div>',
                    unsafe_allow_html=True
                )

            with edt:
                st.markdown('<div class="btn-edit">', unsafe_allow_html=True)
                if st.button("✏️", key=f"ed_{todo['id']}", help=T["edit_label"]):
                    st.session_state.editing_id = todo["id"]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with dlt:
                st.markdown('<div class="btn-del">', unsafe_allow_html=True)
                if st.button("🗑", key=f"dl_{todo['id']}", help=T["delete_label"]):
                    delete_todo(todo["id"])
                    if st.session_state.editing_id == todo["id"]:
                        st.session_state.editing_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
