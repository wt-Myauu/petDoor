import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties, fontManager
import os

# Register Noto CJK font
font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
fontManager.addfont(font_path)
prop = FontProperties(fname=font_path)

plt.rcParams['font.family'] = prop.get_name()

# ───────────────────────────────────────────────────
# Class data
# ───────────────────────────────────────────────────
classes = {
    # name: (x, y, width, height, color, stereotype, attributes, methods)
    "User": (
        0.5, 15.8, 4.2, 3.4,
        "#DDEEFF", None,
        ["- userId: String", "- name: String", "- email: String", "- password: String"],
        ["+ login()", "+ registerPet()", "+ deleteRegistration()", "+ viewAccessLog()", "+ remoteControl(cmd)", "+ configureSettings()"]
    ),
    "MobileApp": (
        5.5, 15.8, 4.2, 3.4,
        "#DDEEFF", "<<boundary>>",
        ["- appId: String", "- connectedDeviceId: String"],
        ["+ displayDoorStatus()", "+ sendCommand(cmd)", "+ showAccessLog()", "+ showNotification()"]
    ),
    "CloudServer": (
        10.5, 15.8, 4.5, 3.4,
        "#E8F5E9", "<<system>>",
        ["- serverId: String", "- isConnected: bool"],
        ["+ storePetData(pet)", "+ authenticate(data): bool", "+ sendPushNotification(msg)", "+ processCommand(cmd)", "+ queryLog(): List"]
    ),
    "Pet": (
        0.5, 11.0, 4.2, 3.0,
        "#FFF9C4", None,
        ["- petId: String", "- name: String", "- species: String", "- photo: Image"],
        ["+ getAuthMeans(): List", "+ updateInfo()", "+ delete()"]
    ),
    "PetDoorSystem": (
        5.5, 11.0, 4.2, 3.2,
        "#E8F5E9", "<<controller>>",
        ["- systemId: String", "- batteryLevel: int", "- isOnline: bool", "- state: DoorState"],
        ["+ monitorSensors()", "+ recognizeObject()", "+ controlDoor(cmd)", "+ triggerAlarm()", "+ sendStatus()"]
    ),
    "AccessLog": (
        10.5, 11.0, 4.5, 3.0,
        "#FFF9C4", None,
        ["- logId: String", "- petId: String", "- timestamp: DateTime", "- authMethod: String", "- direction: Direction"],
        ["+ record()", "+ queryByPet(petId)", "+ delete()"]
    ),
    "Notification": (
        15.5, 11.0, 4.2, 3.0,
        "#FDECEA", None,
        ["- notifId: String", "- type: NotifType", "- message: String", "- timestamp: DateTime"],
        ["+ send(userId)", "+ confirm()"]
    ),
    "AuthMeans": (
        0.5, 6.5, 4.2, 2.5,
        "#EDE7F6", "<<abstract>>",
        ["- authId: String", "- petId: String"],
        ["+ {abstract} validate(): bool", "+ getType(): String"]
    ),
    "SystemSettings": (
        5.5, 6.5, 4.2, 3.0,
        "#FFF9C4", None,
        ["- rfidRange: float", "- doorOpenDuration: int", "- soundSensitivity: float", "- returnTimeout: int"],
        ["+ update(params)", "+ applyToHardware()", "+ reset()"]
    ),
    "SecurityAlert": (
        10.5, 6.5, 4.5, 3.0,
        "#FDECEA", None,
        ["- alertId: String", "- eventType: AlertType", "- timestamp: DateTime", "- isResolved: bool"],
        ["+ trigger(eventType)", "+ resolve()", "+ notifyUser()"]
    ),
    "RFIDTag": (
        0.5, 2.5, 4.2, 2.5,
        "#EDE7F6", None,
        ["- tagId: String", "- uid: String"],
        ["+ scan(): String", "+ validate(): bool"]
    ),
    "Bark": (
        5.5, 2.5, 4.2, 2.5,
        "#EDE7F6", None,
        ["- barkId: String", "- soundData: byte[]", "- frequency: float"],
        ["+ record()", "+ convert()", "+ compare(b: Bark): float", "+ validate(): bool"]
    ),
    "DoorLock": (
        10.5, 2.5, 4.5, 2.5,
        "#E8F5E9", None,
        ["- lockId: String", "- state: LockState"],
        ["+ lock()", "+ unlock()", "+ getState(): LockState"]
    ),
    "RFIDReader": (
        15.5, 2.5, 4.2, 2.5,
        "#E8F5E9", None,
        ["- readerId: String", "- range: float"],
        ["+ scanTag(): String", "+ setRange(r: float)"]
    ),
    "Microphone": (
        15.5, 6.5, 4.2, 2.5,
        "#E8F5E9", None,
        ["- micId: String", "- sensitivity: float"],
        ["+ collectSound(): Bark", "+ setSensitivity(v: float)"]
    ),
}

# ───────────────────────────────────────────────────
# Relationship data: (from_class, to_class, label, rel_type, from_anchor, to_anchor)
# rel_type: 'association', 'generalization', 'composition', 'dependency', 'aggregation'
# ───────────────────────────────────────────────────
relationships = [
    # User - MobileApp
    ("User", "MobileApp", "uses", "dependency", "r", "l"),
    # User - Pet
    ("User", "Pet", "1..*  owns", "association", "b", "t"),
    # MobileApp - CloudServer
    ("MobileApp", "CloudServer", "sends cmd", "dependency", "r", "l"),
    # CloudServer - AccessLog
    ("CloudServer", "AccessLog", "manages", "association", "b", "t"),
    # CloudServer - Notification
    ("CloudServer", "Notification", "sends", "association", "b", "t"),
    # Pet - AuthMeans
    ("Pet", "AuthMeans", "1..*", "aggregation", "b", "t"),
    # AuthMeans - RFIDTag
    ("AuthMeans", "RFIDTag", "", "generalization", "b", "t"),
    # AuthMeans - Bark
    ("AuthMeans", "Bark", "", "generalization", "b", "t"),
    # PetDoorSystem - DoorLock
    ("PetDoorSystem", "DoorLock", "controls", "composition", "b", "t"),
    # PetDoorSystem - RFIDReader
    ("PetDoorSystem", "RFIDReader", "uses", "composition", "b", "t"),
    # PetDoorSystem - Microphone
    ("PetDoorSystem", "Microphone", "uses", "composition", "r", "l"),
    # PetDoorSystem - CloudServer
    ("PetDoorSystem", "CloudServer", "syncs", "dependency", "r", "l"),
    # PetDoorSystem - SystemSettings
    ("PetDoorSystem", "SystemSettings", "configured by", "dependency", "b", "t"),
    # PetDoorSystem - SecurityAlert
    ("PetDoorSystem", "SecurityAlert", "generates", "dependency", "r", "l"),
    # SecurityAlert - Notification
    ("SecurityAlert", "Notification", "triggers", "dependency", "r", "l"),
    # AccessLog - Pet
    ("AccessLog", "Pet", "references", "dependency", "l", "r"),
]


def get_class_center(name):
    x, y, w, h = classes[name][:4]
    return x + w / 2, y + h / 2


def get_class_box(name):
    x, y, w, h = classes[name][:4]
    return x, y, w, h


def draw_class_box(ax, name):
    x, y, w, h, color, stereotype, attrs, methods = classes[name]

    # Main box border
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="square,pad=0",
                          linewidth=1.2,
                          edgecolor="#333333",
                          facecolor=color,
                          zorder=2)
    ax.add_patch(rect)

    # Header height
    header_h = 0.55 if stereotype else 0.45
    attr_section_h = len(attrs) * 0.28
    method_section_h = len(methods) * 0.27

    # Adjust proportional position
    # Header section
    header_rect = FancyBboxPatch((x, y + h - header_h), w, header_h,
                                 boxstyle="square,pad=0",
                                 linewidth=0,
                                 edgecolor="none",
                                 facecolor="#00000015",
                                 zorder=3)
    ax.add_patch(header_rect)

    # Divider lines
    ax.plot([x, x + w], [y + h - header_h, y + h - header_h], color="#555555", lw=0.8, zorder=4)

    # Find divider between attrs and methods
    div2_y = y + h - header_h - attr_section_h - 0.12
    ax.plot([x, x + w], [div2_y, div2_y], color="#555555", lw=0.8, zorder=4)

    # Stereotype
    text_y = y + h - header_h / 2
    if stereotype:
        ax.text(x + w / 2, text_y + 0.08, stereotype,
                ha='center', va='center', fontsize=6.2, color="#5555AA",
                fontstyle='italic', zorder=5)
        ax.text(x + w / 2, text_y - 0.13, name,
                ha='center', va='center', fontsize=7.5, fontweight='bold',
                color="#111111", zorder=5)
    else:
        ax.text(x + w / 2, text_y, name,
                ha='center', va='center', fontsize=7.8, fontweight='bold',
                color="#111111", zorder=5)

    # Attributes
    for i, attr in enumerate(attrs):
        ay = y + h - header_h - 0.22 - i * 0.28
        ax.text(x + 0.12, ay, attr, ha='left', va='center', fontsize=6.0,
                color="#222222", zorder=5, family='monospace')

    # Methods
    for i, meth in enumerate(methods):
        my = div2_y - 0.20 - i * 0.27
        ax.text(x + 0.12, my, meth, ha='left', va='center', fontsize=6.0,
                color="#0033AA", zorder=5, family='monospace')


def get_edge_point(name, anchor):
    x, y, w, h = get_class_box(name)
    cx = x + w / 2
    cy = y + h / 2
    if anchor == 't':
        return cx, y + h
    elif anchor == 'b':
        return cx, y
    elif anchor == 'l':
        return x, cy
    elif anchor == 'r':
        return x + w, cy
    return cx, cy


ARROW_STYLES = {
    'generalization':  dict(arrowstyle='->', color='#222244', lw=1.2,
                            mutation_scale=12,
                            connectionstyle='arc3,rad=0.0'),
    'association':     dict(arrowstyle='->', color='#333333', lw=1.0,
                            mutation_scale=10,
                            connectionstyle='arc3,rad=0.0'),
    'dependency':      dict(arrowstyle='->', color='#666666', lw=0.9,
                            mutation_scale=10,
                            connectionstyle='arc3,rad=0.0',
                            linestyle='dashed'),
    'composition':     dict(arrowstyle='->', color='#1A1A6A', lw=1.1,
                            mutation_scale=10,
                            connectionstyle='arc3,rad=0.0'),
    'aggregation':     dict(arrowstyle='->', color='#1A5A1A', lw=1.1,
                            mutation_scale=10,
                            connectionstyle='arc3,rad=0.0'),
}


def draw_relationship(ax, from_cls, to_cls, label, rel_type, from_anchor, to_anchor):
    x1, y1 = get_edge_point(from_cls, from_anchor)
    x2, y2 = get_edge_point(to_cls, to_anchor)

    style = ARROW_STYLES.get(rel_type, ARROW_STYLES['association'])
    linestyle = style.pop('linestyle', 'solid')
    color = style.get('color', '#333333')

    ax.annotate("",
                xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle=style.get('arrowstyle', '->'),
                    color=color,
                    lw=style.get('lw', 1.0),
                    mutation_scale=style.get('mutation_scale', 10),
                    connectionstyle=style.get('connectionstyle', 'arc3,rad=0'),
                    linestyle=linestyle,
                ),
                zorder=1)
    style['linestyle'] = linestyle

    # Diamond for composition/aggregation at source
    if rel_type == 'composition':
        ax.annotate("", xy=(x1, y1), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='fancy', color='#1A1A6A', lw=0.5,
                                   mutation_scale=8), zorder=1)
        # draw filled diamond
        _draw_diamond(ax, x1, y1, from_anchor, filled=True, color='#1A1A6A')
    elif rel_type == 'aggregation':
        _draw_diamond(ax, x1, y1, from_anchor, filled=False, color='#1A5A1A')
    elif rel_type == 'generalization':
        # already arrow handles it
        pass

    # Label
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        offset = 0.18
        ax.text(mx + offset, my + offset, label,
                ha='center', va='center', fontsize=5.8,
                color='#333333', zorder=6,
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.5))


def _draw_diamond(ax, x, y, anchor, filled, color):
    size = 0.18
    if anchor == 't':
        pts = [(x, y), (x - size / 2, y + size), (x, y + 2 * size), (x + size / 2, y + size)]
    elif anchor == 'b':
        pts = [(x, y), (x - size / 2, y - size), (x, y - 2 * size), (x + size / 2, y - size)]
    elif anchor == 'l':
        pts = [(x, y), (x - size, y + size / 2), (x - 2 * size, y), (x - size, y - size / 2)]
    elif anchor == 'r':
        pts = [(x, y), (x + size, y + size / 2), (x + 2 * size, y), (x + size, y - size / 2)]
    else:
        return
    from matplotlib.patches import Polygon
    poly = Polygon(pts, closed=True, facecolor=color if filled else 'white',
                   edgecolor=color, linewidth=1.0, zorder=3)
    ax.add_patch(poly)


# ───────────────────────────────────────────────────
# Draw the figure
# ───────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(22, 20))
ax.set_xlim(0, 20.5)
ax.set_ylim(1.5, 20.5)
ax.set_aspect('equal')
ax.axis('off')

fig.patch.set_facecolor('#F8F9FA')
ax.set_facecolor('#F8F9FA')

# Title
ax.text(10.25, 20.0, "반려동물 출입 시스템 – 클래스 다이어그램 (Version 3)",
        ha='center', va='center', fontsize=13, fontweight='bold', color='#1A1A2E',
        zorder=10)

# Draw relationships first (below boxes)
for rel in relationships:
    try:
        draw_relationship(ax, *rel)
    except Exception as e:
        print(f"Relationship error {rel[0]}->{rel[1]}: {e}")

# Draw class boxes
for name in classes:
    try:
        draw_class_box(ax, name)
    except Exception as e:
        print(f"Box error {name}: {e}")

# Legend
legend_x, legend_y = 15.5, 19.8
ax.text(legend_x, legend_y, "범례 (Legend)", fontsize=7.5, fontweight='bold', color='#333333', zorder=10)
legend_items = [
    ("──▶  Association (연관)", "#333333", 'solid'),
    ("- - ▶  Dependency (의존)", "#666666", 'dashed'),
    ("──▶  Generalization (상속)", "#222244", 'solid'),
    ("◆──▶  Composition (합성)", "#1A1A6A", 'solid'),
    ("◇──▶  Aggregation (집합)", "#1A5A1A", 'solid'),
]
for i, (text, color, ls) in enumerate(legend_items):
    ax.text(legend_x, legend_y - 0.38 * (i + 1), text,
            fontsize=6.2, color=color, zorder=10,
            linespacing=1.2)

plt.tight_layout(pad=0.5)
out_path = "/workspace/class_diagram.png"
plt.savefig(out_path, dpi=160, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f"Saved: {out_path}")
