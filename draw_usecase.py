import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Ellipse, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(24, 18))
ax.set_xlim(0, 24)
ax.set_ylim(0, 18)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

# ── Title ──────────────────────────────────────────────────────────────────
ax.text(12, 17.4, '반려동물 출입 시스템 – 유스케이스 다이어그램',
        ha='center', va='center', fontsize=16, fontweight='bold',
        color='#1a1a2e',
        fontproperties=matplotlib.font_manager.FontProperties(
            fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'))

# ── helper: Korean font ─────────────────────────────────────────────────────
FONT_PATH = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
KR = matplotlib.font_manager.FontProperties(fname=FONT_PATH, size=8)
KR_SM = matplotlib.font_manager.FontProperties(fname=FONT_PATH, size=7)
KR_LG = matplotlib.font_manager.FontProperties(fname=FONT_PATH, size=9)

def draw_actor(ax, x, y, label, color='#003366'):
    """Stick-figure actor"""
    # head
    head = plt.Circle((x, y + 0.55), 0.22, color=color, zorder=5)
    ax.add_patch(head)
    # body
    ax.plot([x, x], [y + 0.33, y - 0.15], color=color, lw=1.8, zorder=5)
    # arms
    ax.plot([x - 0.3, x + 0.3], [y + 0.1, y + 0.1], color=color, lw=1.8, zorder=5)
    # legs
    ax.plot([x, x - 0.25], [y - 0.15, y - 0.55], color=color, lw=1.8, zorder=5)
    ax.plot([x, x + 0.25], [y - 0.15, y - 0.55], color=color, lw=1.8, zorder=5)
    # label
    ax.text(x, y - 0.78, label, ha='center', va='top', fontproperties=KR,
            color=color, fontsize=8)

def draw_usecase(ax, x, y, label, w=2.6, h=0.68,
                 fc='#EEF5FF', ec='#3A6EA5', lw=1.5):
    """Ellipse use-case"""
    ell = Ellipse((x, y), width=w, height=h,
                  facecolor=fc, edgecolor=ec, linewidth=lw, zorder=4)
    ax.add_patch(ell)
    lines = label.split('\n')
    total = len(lines)
    for i, line in enumerate(lines):
        offset = (total - 1) / 2 * 0.12 - i * 0.12
        ax.text(x, y + offset, line, ha='center', va='center',
                fontproperties=KR_SM, color='#1a1a2e', fontsize=7, zorder=5)

def draw_package(ax, x1, y1, x2, y2, label, fc='#EAF4FB', ec='#5B9BD5', lw=1.5):
    """Package rectangle"""
    rect = FancyBboxPatch((x1, y1), x2 - x1, y2 - y1,
                          boxstyle='round,pad=0.05',
                          facecolor=fc, edgecolor=ec, linewidth=lw,
                          zorder=2, alpha=0.55)
    ax.add_patch(rect)
    ax.text(x1 + 0.15, y2 - 0.02, label, va='top', ha='left',
            fontproperties=KR_LG, color=ec, fontsize=8.5, fontweight='bold', zorder=3)

def arrow(ax, x1, y1, x2, y2, style='->', color='#555555', lw=1.2, ls='-'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, linestyle=ls),
                zorder=6)

def dashed_arrow(ax, x1, y1, x2, y2, label='', color='#888888'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->',
                                color=color, lw=1.0,
                                linestyle='dashed',
                                connectionstyle='arc3,rad=0.0'),
                zorder=6)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.12, label, ha='center', va='bottom',
                fontproperties=KR_SM, color=color, fontsize=6.5, zorder=7)

# ═══════════════════════════════════════════════════════════════════════════
#  SYSTEM BOUNDARY
# ═══════════════════════════════════════════════════════════════════════════
sys_rect = FancyBboxPatch((3.2, 0.6), 17.5, 16.0,
                          boxstyle='round,pad=0.1',
                          facecolor='#F8FBFF', edgecolor='#2C5F8A',
                          linewidth=2.2, zorder=1)
ax.add_patch(sys_rect)
ax.text(4.0, 16.45, '반려동물 출입 시스템', va='top', ha='left',
        fontproperties=KR_LG,
        color='#2C5F8A', fontsize=10, fontweight='bold', zorder=3)

# ═══════════════════════════════════════════════════════════════════════════
#  ACTORS  (outside system boundary)
# ═══════════════════════════════════════════════════════════════════════════
# Left side actors
draw_actor(ax, 1.2, 14.0, '사용자\n(반려인)', '#154360')
draw_actor(ax, 1.2, 9.0,  '반려동물',         '#1A5276')
draw_actor(ax, 1.2, 4.5,  '비인가 객체\n(사람/외부 동물)', '#6E2F2F')

# Right side actors
draw_actor(ax, 22.5, 13.5, '관리 서버',            '#145A32')
draw_actor(ax, 22.5, 7.5,  '시스템\n(임베디드 제어기)', '#6C3483')

# ═══════════════════════════════════════════════════════════════════════════
#  PACKAGES & USE CASES
# ═══════════════════════════════════════════════════════════════════════════

# ── 패키지 1: 반려동물 관리 ──────────────────────────────────────────────
draw_package(ax, 3.5, 12.8, 10.8, 16.3, '반려동물 관리',
             fc='#EBF5FB', ec='#2471A3')
UC1 = (7.0, 15.3)
UC2 = (7.0, 13.7)
draw_usecase(ax, *UC1, 'UC1: 반려동물 등록\n(RFID 칩 등록)', w=3.0, h=0.75,
             fc='#D6EAF8', ec='#2471A3')
draw_usecase(ax, *UC2, 'UC2: 반려동물 정보\n수정 / 삭제', w=3.0, h=0.75,
             fc='#D6EAF8', ec='#2471A3')

# ── 패키지 2: 시스템 설정 ────────────────────────────────────────────────
draw_package(ax, 11.2, 12.8, 18.5, 16.3, '시스템 설정',
             fc='#EAF9F0', ec='#1E8449')
UC3 = (14.8, 14.9)
draw_usecase(ax, *UC3,
             'UC3: 시스템 동작 설정\n(인식거리·개방시간·\n외출시간·경보음)',
             w=3.3, h=1.1, fc='#D5F5E3', ec='#1E8449')

# ── 패키지 3: 자동 출입 제어 ─────────────────────────────────────────────
draw_package(ax, 3.5, 7.2, 14.5, 12.4, '자동 출입 제어',
             fc='#FEF9E7', ec='#B7950B')
UC4 = (7.0, 11.2)
UC6 = (7.0, 9.3)
UC7 = (11.5, 10.0)
draw_usecase(ax, *UC4, 'UC4: 자동 출입 제어\n(RFID 인식 → 문 개방)',
             w=3.0, h=0.75, fc='#FEF3CD', ec='#B7950B')
draw_usecase(ax, *UC6, 'UC6: 네트워크 장애 시\n로컬 인증 출입',
             w=3.0, h=0.75, fc='#FEF3CD', ec='#B7950B')
draw_usecase(ax, *UC7, 'UC7: 객체 판별\n(사람/외부동물/등록동물)',
             w=3.1, h=0.75, fc='#FEF3CD', ec='#B7950B')

# ── 패키지 4: 모니터링 및 알림 ──────────────────────────────────────────
draw_package(ax, 14.8, 7.2, 20.5, 12.4, '모니터링 및 알림',
             fc='#F4ECF7', ec='#7D3C98')
UC5 = (17.5, 10.0)
draw_usecase(ax, *UC5,
             'UC5: 출입 모니터링\n및 알림 확인\n(미복귀 알림)',
             w=3.1, h=1.05, fc='#E8DAEF', ec='#7D3C98')

# ── 패키지 5: 비상 안전 제어 ────────────────────────────────────────────
draw_package(ax, 3.5, 0.8, 20.5, 6.9, '비상 안전 제어',
             fc='#FDEDEC', ec='#C0392B')
UC8 = (11.5, 4.5)
draw_usecase(ax, *UC8,
             'UC8: 비상 상황 자동 안전 제어\n(저전력·화재 시 잠금 자동 해제)',
             w=3.8, h=0.85, fc='#FADBD8', ec='#C0392B')

# ── secondary use cases inside emergency package ─────────────────────────
ax.text(6.0, 5.8, '• 배터리 임계치(3%) 감지 → 비상모드 전환',
        fontproperties=KR_SM, color='#922B21', fontsize=7)
ax.text(6.0, 5.2, '• 출입문 잠금 자동 해제 (Unlock)',
        fontproperties=KR_SM, color='#922B21', fontsize=7)
ax.text(6.0, 4.6, '• LED 점멸 / 비프음 알람 출력',
        fontproperties=KR_SM, color='#922B21', fontsize=7)
ax.text(6.0, 4.0, '• 앱으로 "저전력 비상 개방" 푸시 알림 전송',
        fontproperties=KR_SM, color='#922B21', fontsize=7)
ax.text(6.0, 3.4, '• [대안] 물리적 레버 수동 개방',
        fontproperties=KR_SM, color='#922B21', fontsize=7)
ax.text(6.0, 2.8, '• [대안] 오프라인 시에도 잠금 해제 독립 수행',
        fontproperties=KR_SM, color='#922B21', fontsize=7)

ax.text(14.0, 5.8, '• 화재 감지 센서 비상 신호 수신',
        fontproperties=KR_SM, color='#922B21', fontsize=7)
ax.text(14.0, 5.2, '• 관리 서버 경유 알림 전송',
        fontproperties=KR_SM, color='#922B21', fontsize=7)

# ═══════════════════════════════════════════════════════════════════════════
#  ASSOCIATIONS  (actor → usecase)
# ═══════════════════════════════════════════════════════════════════════════
# 사용자 → UC1, UC2, UC3, UC5
for uc in [UC1, UC2]:
    arrow(ax, 1.6, 14.0, uc[0] - 1.5, uc[1], color='#154360')
arrow(ax, 1.6, 14.0, UC3[0] - 1.6, UC3[1], color='#154360')
arrow(ax, 1.6, 14.0, UC5[0] - 1.6, UC5[1] + 0.3, color='#154360')

# 반려동물 → UC4, UC6, UC7
arrow(ax, 1.6, 9.0, UC4[0] - 1.5, UC4[1], color='#1A5276')
arrow(ax, 1.6, 9.0, UC6[0] - 1.5, UC6[1], color='#1A5276')
arrow(ax, 1.6, 9.0, UC7[0] - 1.6, UC7[1] + 0.2, color='#1A5276')

# 비인가 객체 → UC7
arrow(ax, 1.6, 4.5, UC7[0] - 1.6, UC7[1] - 0.3, color='#6E2F2F')

# 관리 서버 → UC1, UC2, UC3, UC4, UC5, UC7, UC8
for uc, dy in [(UC1, 0.2), (UC2, -0.2)]:
    arrow(ax, 22.0, 13.5, uc[0] + 1.5, uc[1], color='#145A32')
arrow(ax, 22.0, 13.5, UC3[0] + 1.7, UC3[1], color='#145A32')
arrow(ax, 22.0, 13.5, UC4[0] + 1.5, UC4[1] + 0.2, color='#145A32')
arrow(ax, 22.0, 13.5, UC5[0] + 1.6, UC5[1] + 0.3, color='#145A32')
arrow(ax, 22.0, 13.5, UC7[0] + 1.6, UC7[1] + 0.2, color='#145A32')
arrow(ax, 22.0, 7.5, UC8[0] + 1.9, UC8[1] + 0.2, color='#145A32')

# 시스템(임베디드) → UC6, UC8
arrow(ax, 22.0, 7.5, UC6[0] + 1.5, UC6[1], color='#6C3483')
arrow(ax, 22.0, 7.5, UC8[0] + 1.9, UC8[1] - 0.2, color='#6C3483')

# ═══════════════════════════════════════════════════════════════════════════
#  RELATIONSHIPS BETWEEN USE CASES
# ═══════════════════════════════════════════════════════════════════════════
# UC7 <<extend>> UC4  (객체 판별 승인 → 자동 출입)
ax.annotate('', xy=(UC4[0] + 0.5, UC4[1] - 0.1),
            xytext=(UC7[0] - 0.4, UC7[1] + 0.1),
            arrowprops=dict(arrowstyle='->', color='#888888',
                            lw=1.1, linestyle='dashed'),
            zorder=6)
ax.text((UC4[0] + UC7[0]) / 2 + 0.1, (UC4[1] + UC7[1]) / 2 + 0.2,
        '<<extend>>', ha='center', fontproperties=KR_SM,
        color='#888888', fontsize=6.5)

# UC6 <<include>> UC4  (로컬 인증도 출입 제어 포함)
ax.annotate('', xy=(UC4[0], UC4[1] - 0.37),
            xytext=(UC6[0], UC6[1] + 0.37),
            arrowprops=dict(arrowstyle='->', color='#888888',
                            lw=1.1, linestyle='dashed'),
            zorder=6)
ax.text(UC4[0] - 0.7, (UC4[1] + UC6[1]) / 2,
        '<<include>>', ha='center', fontproperties=KR_SM,
        color='#888888', fontsize=6.5)

# UC4 <<extend>> UC8  (비상 상황 발생 시)
ax.annotate('', xy=(UC8[0] - 0.5, UC8[1] + 0.4),
            xytext=(UC4[0] - 0.1, UC4[1] - 0.37),
            arrowprops=dict(arrowstyle='->', color='#C0392B',
                            lw=1.1, linestyle='dashed'),
            zorder=6)
ax.text(UC4[0] - 1.8, (UC4[1] + UC8[1]) / 2 + 0.5,
        '<<extend>>\n비상 발생 시', ha='center', fontproperties=KR_SM,
        color='#C0392B', fontsize=6.5)

# ═══════════════════════════════════════════════════════════════════════════
#  LEGEND
# ═══════════════════════════════════════════════════════════════════════════
legend_x, legend_y = 19.5, 5.9
ax.text(legend_x, legend_y, '범례', fontproperties=KR, fontsize=8,
        fontweight='bold', color='#333333')
# solid line = association
ax.plot([legend_x, legend_x + 1.0], [legend_y - 0.5, legend_y - 0.5],
        color='#555555', lw=1.5)
ax.annotate('', xy=(legend_x + 1.0, legend_y - 0.5),
            xytext=(legend_x + 0.85, legend_y - 0.5),
            arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5))
ax.text(legend_x + 1.15, legend_y - 0.5, '연관 (Association)',
        fontproperties=KR_SM, fontsize=7, va='center', color='#333333')
# dashed = extend/include
ax.plot([legend_x, legend_x + 1.0], [legend_y - 1.1, legend_y - 1.1],
        color='#888888', lw=1.2, linestyle='dashed')
ax.annotate('', xy=(legend_x + 1.0, legend_y - 1.1),
            xytext=(legend_x + 0.85, legend_y - 1.1),
            arrowprops=dict(arrowstyle='->', color='#888888', lw=1.2))
ax.text(legend_x + 1.15, legend_y - 1.1,
        '<<extend>> / <<include>>',
        fontproperties=KR_SM, fontsize=7, va='center', color='#555555')

plt.tight_layout(pad=0.3)
plt.savefig('/workspace/usecase_diagram.png', dpi=150, bbox_inches='tight',
            facecolor='#FAFAFA')
print("Saved usecase_diagram.png")
