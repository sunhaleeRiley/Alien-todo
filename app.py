import streamlit as st
import uuid
from datetime import datetime

# ── 페이지 설정 ────────────────────────────────────────────────────
st.set_page_config(
    page_title="👽 Alien Mission Control",
    page_icon="👽",
    layout="centered",
)

# ── i18n 번역 테이블 ───────────────────────────────────────────────
I18N = {
    "ko": {
        "app_title":      "👾 외계인 임무 관리 본부",
        "app_subtitle":   "지구 정복 전에 할일부터 처리하자",
        "lbl_total":      "전체 임무",
        "lbl_done":       "완료",
        "lbl_remain":     "남은 임무",
        "lbl_rate":       "달성률",
        "lbl_progress":   "임무 진행률",
        "prog_text":      lambda d, t: f"{d} / {t} 완료",
        "placeholder":    "새 임무를 입력하세요...",
        "lbl_add":        "추가",
        "cat_work":       "💼 업무",
        "cat_personal":   "🏠 개인",
        "cat_study":      "📚 공부",
        "filter_all":     "전체",
        "filter_work":    "💼 업무",
        "filter_personal":"🏠 개인",
        "filter_study":   "📚 공부",
        "filter_done":    "✅ 완료만",
        "filter_todo":    "⏳ 미완료만",
        "empty_all":      "아직 임무가 없어요. 지구 정복 계획을 세워봐요!",
        "empty_filter":   "해당 조건의 임무가 없어요.",
        "edit_label":     "수정",
        "save_label":     "저장",
        "cancel_label":   "취소",
        "delete_label":   "삭제",
        "cat_labels":     {"work": "💼 업무", "personal": "🏠 개인", "study": "📚 공부"},
    },
    "en": {
        "app_title":      "👾 Alien Mission Control",
        "app_subtitle":   "Conquer your tasks before conquering Earth",
        "lbl_total":      "Total",
        "lbl_done":       "Done",
        "lbl_remain":     "Remaining",
        "lbl_rate":       "Progress",
        "lbl_progress":   "Mission Progress",
        "prog_text":      lambda d, t: f"{d} / {t} done",
        "placeholder":    "Enter a new mission...",
        "lbl_add":        "Add",
        "cat_work":       "💼 Work",
        "cat_personal":   "🏠 Personal",
        "cat_study":      "📚 Study",
        "filter_all":     "All",
        "filter_work":    "💼 Work",
        "filter_personal":"🏠 Personal",
        "filter_study":   "📚 Study",
        "filter_done":    "✅ Done",
        "filter_todo":    "⏳ Pending",
        "empty_all":      "No missions yet. Plan your Earth conquest!",
        "empty_filter":   "No missions match this filter.",
        "edit_label":     "Edit",
        "save_label":     "Save",
        "cancel_label":   "Cancel",
        "delete_label":   "Delete",
        "cat_labels":     {"work": "💼 Work", "personal": "🏠 Personal", "study": "📚 Study"},
    },
}

# ── 카테고리 색상 ──────────────────────────────────────────────────
CAT_COLORS = {
    "work":     {"bg": "#EEEDFE", "text": "#3C3489", "active": "#534AB7"},
    "personal": {"bg": "#E1F5EE", "text": "#085041", "active": "#0F6E56"},
    "study":    {"bg": "#E6F1FB", "text": "#0C447C", "active": "#185FA5"},
}

# ── 세션 상태 초기화 ───────────────────────────────────────────────
def init_state():
    if "todos" not in st.session_state:
        st.session_state.todos = []
    if "lang" not in st.session_state:
        st.session_state.lang = "ko"
    if "selected_cat" not in st.session_state:
        st.session_state.selected_cat = "work"
    if "current_filter" not in st.session_state:
        st.session_state.current_filter = "all"
    if "editing_id" not in st.session_state:
        st.session_state.editing_id = None

init_state()

# ── 편의 참조 ──────────────────────────────────────────────────────
T = I18N[st.session_state.lang]

# ── CSS 인젝션 ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');

:root {
  --green:        #7BC62D;
  --green-dark:   #5A9E1A;
  --green-light:  #EAF3DE;
  --dark:         #2C2C2A;
  --gray:         #888780;
  --gray-light:   #F5F5F3;
  --border:       rgba(0,0,0,0.12);
  --white:        #FFFFFF;
}

/* 앱 전체 배경 */
.stApp { background: var(--gray-light) !important; }
section[data-testid="stMain"] > div { padding-top: 1rem !important; }

/* 헤더 카드 */
.alien-header {
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--white);
  border: 0.5px solid var(--border);
  border-radius: 14px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.25rem;
}

/* CSS 외계인 얼굴 */
.alien-head {
  width: 54px; height: 54px;
  background: var(--green);
  border-radius: 50%;
  border: 2.5px solid var(--green-dark);
  flex-shrink: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 4px;
  position: relative;
}
.alien-head::before {
  content: '';
  position: absolute;
  top: -12px; left: 50%;
  transform: translateX(-50%);
  width: 3px; height: 14px;
  background: var(--green-dark);
  border-radius: 3px 3px 0 0;
}
.alien-head::after {
  content: '';
  position: absolute;
  top: -14px; left: 50%;
  transform: translateX(-50%);
  width: 6px; height: 6px;
  background: var(--green-dark);
  border-radius: 50%;
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
  width: 20px; height: 5px;
  background: var(--green-dark);
  border-radius: 0 0 8px 8px;
}
.header-text h1 {
  font-size: 20px; font-weight: 700;
  color: var(--dark); line-height: 1.2; margin: 0;
}
.header-text p {
  font-size: 13px; color: var(--gray); margin: 3px 0 0;
}

/* 통계 카드 그리드 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 1.25rem;
}
.stat-card {
  background: var(--white);
  border: 0.5px solid var(--border);
  border-radius: 10px;
  padding: 0.75rem 0.5rem;
  text-align: center;
}
.stat-num  { font-size: 24px; font-weight: 700; color: var(--dark); line-height: 1; }
.stat-lbl  { font-size: 11px; color: var(--gray); margin-top: 4px; }

/* 프로그레스 바 */
.progress-card {
  background: var(--white);
  border: 0.5px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.25rem;
}
.progress-top {
  display: flex; justify-content: space-between;
  font-size: 12px; color: var(--gray); margin-bottom: 8px;
}
.progress-track {
  height: 10px; background: var(--gray-light);
  border-radius: 20px; overflow: hidden;
}
.progress-fill {
  height: 100%; background: var(--green);
  border-radius: 20px; transition: width 0.4s ease;
}

/* 카테고리 배지 */
.cat-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  white-space: nowrap;
}

/* 할일 아이템 카드 */
.todo-card {
  background: var(--white);
  border: 0.5px solid var(--border);
  border-radius: 12px;
  padding: 0.875rem 1rem;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.todo-card.done { opacity: 0.55; }
.todo-card.done .todo-text { text-decoration: line-through; color: var(--gray); }
.todo-text { flex: 1; font-size: 14px; color: var(--dark); word-break: break-word; }

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  background: var(--white);
  border: 0.5px solid var(--border);
  border-radius: 12px;
}
.empty-icon { font-size: 48px; margin-bottom: 0.75rem; }
.empty-msg  { font-size: 14px; color: var(--gray); }

/* Streamlit 버튼 스타일 오버라이드 */
div[data-testid="stHorizontalBlock"] .stButton > button {
  border-radius: 20px !important;
  border: 0.5px solid rgba(0,0,0,0.12) !important;
  background: transparent !important;
  color: #888780 !important;
  font-size: 13px !important;
  padding: 4px 14px !important;
  transition: all 0.15s !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
  background: #F5F5F3 !important;
  border-color: rgba(0,0,0,0.2) !important;
}

/* 추가 버튼 */
.add-btn > button {
  background: #7BC62D !important;
  color: white !important;
  border: none !important;
  border-radius: 20px !important;
  font-weight: 600 !important;
}
.add-btn > button:hover { opacity: 0.85 !important; }

/* 완료 토글 체크 버튼 */
.check-done > button {
  background: #7BC62D !important;
  color: white !important;
  border-color: #7BC62D !important;
  border-radius: 50% !important;
  width: 28px !important; height: 28px !important;
  padding: 0 !important; font-size: 14px !important;
}
.check-undone > button {
  background: transparent !important;
  border: 2px solid rgba(0,0,0,0.2) !important;
  border-radius: 50% !important;
  width: 28px !important; height: 28px !important;
  padding: 0 !important; font-size: 14px !important;
}

/* 삭제 버튼 */
.del-btn > button {
  background: transparent !important;
  color: #888780 !important;
  border: none !important;
  border-radius: 6px !important;
  padding: 4px 8px !important;
  font-size: 16px !important;
}
.del-btn > button:hover {
  color: #E24B4A !important;
  background: #FCEBEB !important;
}

/* 수정 버튼 */
.edit-btn > button {
  background: transparent !important;
  color: #888780 !important;
  border: none !important;
  border-radius: 6px !important;
  padding: 4px 8px !important;
  font-size: 13px !important;
}

/* 필터/카테고리 active 버튼 */
.filter-active > button {
  background: #7BC62D !important;
  color: white !important;
  border-color: #7BC62D !important;
}
.cat-active-work > button {
  background: #534AB7 !important; color: white !important; border-color: #534AB7 !important;
}
.cat-active-personal > button {
  background: #0F6E56 !important; color: white !important; border-color: #0F6E56 !important;
}
.cat-active-study > button {
  background: #185FA5 !important; color: white !important; border-color: #185FA5 !important;
}

/* 언어 토글 */
.lang-ko-active > button, .lang-en-active > button {
  background: #7BC62D !important; color: white !important;
  border-color: #7BC62D !important; border-radius: 20px !important;
  font-size: 12px !important; font-weight: 600 !important;
  padding: 2px 12px !important;
}
.lang-ko > button, .lang-en > button {
  background: transparent !important; color: #888780 !important;
  border: 0.5px solid rgba(0,0,0,0.12) !important; border-radius: 20px !important;
  font-size: 12px !important; font-weight: 600 !important;
  padding: 2px 12px !important;
}

/* 입력 필드 */
.stTextInput input {
  border-radius: 8px !important;
  border: 0.5px solid rgba(0,0,0,0.12) !important;
  background: #F5F5F3 !important;
  font-size: 14px !important;
}
.stTextInput input:focus {
  border-color: #7BC62D !important;
  background: white !important;
  box-shadow: none !important;
}

/* 섹션 구분선 제거 */
hr { display: none; }
.block-container { max-width: 700px !important; padding: 1rem 1rem 3rem !important; }

/* 헤더/푸터 숨기기 */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── 헬퍼 함수들 ───────────────────────────────────────────────────
def add_todo(text: str):
    if not text.strip():
        return
    st.session_state.todos.insert(0, {
        "id":   str(uuid.uuid4()),
        "text": text.strip()[:80],
        "cat":  st.session_state.selected_cat,
        "done": False,
        "created_at": datetime.now().isoformat(),
    })

def toggle_todo(todo_id: str):
    for t in st.session_state.todos:
        if t["id"] == todo_id:
            t["done"] = not t["done"]
            break

def delete_todo(todo_id: str):
    st.session_state.todos = [t for t in st.session_state.todos if t["id"] != todo_id]

def update_todo_text(todo_id: str, new_text: str):
    if not new_text.strip():
        return
    for t in st.session_state.todos:
        if t["id"] == todo_id:
            t["text"] = new_text.strip()[:80]
            break

def get_filtered(todos, f):
    if f == "work":     return [t for t in todos if t["cat"] == "work"]
    if f == "personal": return [t for t in todos if t["cat"] == "personal"]
    if f == "study":    return [t for t in todos if t["cat"] == "study"]
    if f == "done":     return [t for t in todos if t["done"]]
    if f == "todo":     return [t for t in todos if not t["done"]]
    return todos


# ════════════════════════════════════════════════════════════════════
# UI 렌더링
# ════════════════════════════════════════════════════════════════════

# ── 헤더 + 언어 토글 ─────────────────────────────────────────────
col_header, col_lang = st.columns([8, 2])

with col_header:
    st.markdown(f"""
    <div class="alien-header">
      <div class="alien-head">
        <div class="alien-eyes">
          <div class="eye sm"></div>
          <div class="eye lg"></div>
          <div class="eye sm"></div>
        </div>
        <div class="alien-mouth"></div>
      </div>
      <div class="header-text">
        <h1>{T["app_title"]}</h1>
        <p>{T["app_subtitle"]}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_lang:
    st.write("")  # 수직 정렬용
    lc1, lc2 = st.columns(2)
    with lc1:
        ko_class = "lang-ko-active" if st.session_state.lang == "ko" else "lang-ko"
        st.markdown(f'<div class="{ko_class}">', unsafe_allow_html=True)
        if st.button("KO", key="btn_ko"):
            st.session_state.lang = "ko"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with lc2:
        en_class = "lang-en-active" if st.session_state.lang == "en" else "lang-en"
        st.markdown(f'<div class="{en_class}">', unsafe_allow_html=True)
        if st.button("EN", key="btn_en"):
            st.session_state.lang = "en"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ── 통계 계산 ─────────────────────────────────────────────────────
total  = len(st.session_state.todos)
done   = sum(1 for t in st.session_state.todos if t["done"])
remain = total - done
pct    = round(done / total * 100) if total else 0

# ── 통계 카드 ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="stats-grid">
  <div class="stat-card"><div class="stat-num">{total}</div><div class="stat-lbl">{T["lbl_total"]}</div></div>
  <div class="stat-card"><div class="stat-num">{done}</div><div class="stat-lbl">{T["lbl_done"]}</div></div>
  <div class="stat-card"><div class="stat-num">{remain}</div><div class="stat-lbl">{T["lbl_remain"]}</div></div>
  <div class="stat-card"><div class="stat-num">{pct}%</div><div class="stat-lbl">{T["lbl_rate"]}</div></div>
</div>
""", unsafe_allow_html=True)

# ── 프로그레스 바 ─────────────────────────────────────────────────
st.markdown(f"""
<div class="progress-card">
  <div class="progress-top">
    <span>{T["lbl_progress"]}</span>
    <span>{T["prog_text"](done, total)}</span>
  </div>
  <div class="progress-track">
    <div class="progress-fill" style="width:{pct}%"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 입력 영역 ─────────────────────────────────────────────────────
with st.container():
    inp_col, btn_col = st.columns([8, 2])
    with inp_col:
        new_text = st.text_input(
            label="new_task",
            label_visibility="collapsed",
            placeholder=T["placeholder"],
            key="new_task_input",
            max_chars=80,
        )
    with btn_col:
        st.markdown('<div class="add-btn">', unsafe_allow_html=True)
        if st.button(f"＋ {T['lbl_add']}", key="add_btn", use_container_width=True):
            if new_text.strip():
                add_todo(new_text)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Enter 키 처리 — text_input의 on_change 활용
    if new_text and st.session_state.get("_last_input") != new_text:
        st.session_state["_last_input"] = new_text

    # 카테고리 선택
    cat_cols = st.columns(3)
    cats = [("work", T["cat_work"]), ("personal", T["cat_personal"]), ("study", T["cat_study"])]
    for col, (cat_key, cat_label) in zip(cat_cols, cats):
        with col:
            is_active = st.session_state.selected_cat == cat_key
            css_class = f"cat-active-{cat_key}" if is_active else ""
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            if st.button(cat_label, key=f"cat_{cat_key}", use_container_width=True):
                st.session_state.selected_cat = cat_key
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ── 필터 ──────────────────────────────────────────────────────────
st.write("")
filter_options = [
    ("all",      T["filter_all"]),
    ("work",     T["filter_work"]),
    ("personal", T["filter_personal"]),
    ("study",    T["filter_study"]),
    ("done",     T["filter_done"]),
    ("todo",     T["filter_todo"]),
]
f_cols = st.columns(len(filter_options))
for col, (fkey, flabel) in zip(f_cols, filter_options):
    with col:
        is_active = st.session_state.current_filter == fkey
        css_class = "filter-active" if is_active else ""
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        if st.button(flabel, key=f"filter_{fkey}", use_container_width=True):
            st.session_state.current_filter = fkey
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── 할일 목록 ─────────────────────────────────────────────────────
st.write("")
filtered = get_filtered(st.session_state.todos, st.session_state.current_filter)

if not filtered:
    msg = T["empty_all"] if not st.session_state.todos else T["empty_filter"]
    st.markdown(f"""
    <div class="empty-state">
      <div class="empty-icon">👽</div>
      <div class="empty-msg">{msg}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for todo in filtered:
        cat_color = CAT_COLORS[todo["cat"]]
        cat_label = T["cat_labels"][todo["cat"]]
        done_class = " done" if todo["done"] else ""

        if st.session_state.editing_id == todo["id"]:
            # ── 편집 모드 ──
            edit_col, save_col, cancel_col = st.columns([7, 1.5, 1.5])
            with edit_col:
                edited = st.text_input(
                    label="edit",
                    label_visibility="collapsed",
                    value=todo["text"],
                    key=f"edit_input_{todo['id']}",
                    max_chars=80,
                )
            with save_col:
                st.markdown('<div class="add-btn">', unsafe_allow_html=True)
                if st.button(T["save_label"], key=f"save_{todo['id']}", use_container_width=True):
                    update_todo_text(todo["id"], edited)
                    st.session_state.editing_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with cancel_col:
                if st.button(T["cancel_label"], key=f"cancel_{todo['id']}", use_container_width=True):
                    st.session_state.editing_id = None
                    st.rerun()
        else:
            # ── 일반 모드 ──
            check_col, text_col, badge_col, edit_col, del_col = st.columns([1, 6, 2, 1, 1])

            with check_col:
                check_class = "check-done" if todo["done"] else "check-undone"
                st.markdown(f'<div class="{check_class}">', unsafe_allow_html=True)
                check_icon = "✓" if todo["done"] else " "
                if st.button(check_icon, key=f"check_{todo['id']}"):
                    toggle_todo(todo["id"])
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with text_col:
                text_style = "text-decoration:line-through;color:#888780;" if todo["done"] else ""
                st.markdown(
                    f'<div style="padding:6px 0;font-size:14px;color:#2C2C2A;{text_style}">'
                    f'{todo["text"]}</div>',
                    unsafe_allow_html=True
                )

            with badge_col:
                st.markdown(
                    f'<div style="padding:6px 0;">'
                    f'<span class="cat-badge" style="background:{cat_color["bg"]};color:{cat_color["text"]}">'
                    f'{cat_label}</span></div>',
                    unsafe_allow_html=True
                )

            with edit_col:
                st.markdown('<div class="edit-btn">', unsafe_allow_html=True)
                if st.button("✏️", key=f"edit_{todo['id']}", help=T["edit_label"]):
                    st.session_state.editing_id = todo["id"]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with del_col:
                st.markdown('<div class="del-btn">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_{todo['id']}", help=T["delete_label"]):
                    delete_todo(todo["id"])
                    if st.session_state.editing_id == todo["id"]:
                        st.session_state.editing_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
