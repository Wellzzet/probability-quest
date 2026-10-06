"""Персонаж в SVG: базовая фигура + слои доспехов."""

SKINS = {"Светлая": "#F6D3B3", "Тёплая": "#E8B48A", "Смуглая": "#C68A5E", "Тёмная": "#8D5A3B"}
HAIRS = {"Чёрные": "#1E1A22", "Каштановые": "#5A3522", "Рыжие": "#B5522B", "Русые": "#B08A55", "Фиолетовые": "#6B4FA0"}
OUTFITS = {"Синий": "#3B5BA5", "Изумрудный": "#2E8B6E", "Бордовый": "#8E2F45", "Фиолетовый": "#5E4A9C", "Серый": "#5B6070"}
HAIRSTYLES = ["Короткие", "Длинные"]

# подписи вариантов внешности: ключ (как в сохранении) -> (ru, en, kk)
LOOK_LABELS = {
    "Светлая": ("Светлая", "Light", "Ақ"), "Тёплая": ("Тёплая", "Warm", "Жылы"),
    "Смуглая": ("Смуглая", "Tan", "Қоңыр"), "Тёмная": ("Тёмная", "Dark", "Қара торы"),
    "Чёрные": ("Чёрные", "Black", "Қара"), "Каштановые": ("Каштановые", "Chestnut", "Қара қоңыр"),
    "Рыжие": ("Рыжие", "Red", "Жирен"), "Русые": ("Русые", "Fair", "Сарғылт"), "Фиолетовые": ("Фиолетовые", "Purple", "Күлгін"),
    "Синий": ("Синий", "Blue", "Көк"), "Изумрудный": ("Изумрудный", "Emerald", "Зүмірет"), "Бордовый": ("Бордовый", "Burgundy", "Күрең"),
    "Фиолетовый": ("Фиолетовый", "Purple", "Күлгін"), "Серый": ("Серый", "Grey", "Сұр"),
    "Короткие": ("Короткие", "Short", "Қысқа"), "Длинные": ("Длинные", "Long", "Ұзын"),
}

STEEL, STEEL_D, GOLD = "#BCC4D0", "#7D8696", "#E0B44A"

ARMOR_ORDER = ["boots", "chest", "belt", "shoulders", "gauntlets", "helmet", "shield", "sword"]


def _armor(piece):
    s, d, g = STEEL, STEEL_D, GOLD
    if piece == "boots":
        return (f'<rect x="81" y="224" width="26" height="32" rx="5" fill="{s}" stroke="{d}" stroke-width="2"/>'
                f'<rect x="113" y="224" width="26" height="32" rx="5" fill="{s}" stroke="{d}" stroke-width="2"/>'
                f'<ellipse cx="93" cy="259" rx="16" ry="8" fill="{d}"/><ellipse cx="127" cy="259" rx="16" ry="8" fill="{d}"/>'
                f'<rect x="81" y="236" width="26" height="4" fill="{g}"/><rect x="113" y="236" width="26" height="4" fill="{g}"/>')
    if piece == "chest":
        return (f'<path d="M78 128 Q110 118 142 128 L146 186 Q110 198 74 186 Z" fill="{s}" stroke="{d}" stroke-width="2"/>'
                f'<path d="M110 124 L110 192" stroke="{d}" stroke-width="2"/>'
                f'<circle cx="110" cy="152" r="13" fill="{g}" stroke="#9C7A25" stroke-width="2"/>'
                f'<text x="110" y="158" text-anchor="middle" font-family="Georgia,serif" font-size="16" '
                f'font-weight="bold" fill="#3A2A05">P</text>')
    if piece == "belt":
        return (f'<rect x="73" y="182" width="74" height="11" rx="3" fill="#6B4425"/>'
                f'<rect x="102" y="180" width="16" height="15" rx="3" fill="none" stroke="{g}" stroke-width="3"/>')
    if piece == "shoulders":
        return (f'<ellipse cx="78" cy="131" rx="18" ry="12" fill="{s}" stroke="{g}" stroke-width="2.5"/>'
                f'<ellipse cx="142" cy="131" rx="18" ry="12" fill="{s}" stroke="{g}" stroke-width="2.5"/>')
    if piece == "gauntlets":
        return (f'<rect x="47" y="178" width="20" height="12" rx="3" fill="{d}"/>'
                f'<rect x="153" y="178" width="20" height="12" rx="3" fill="{d}"/>'
                f'<circle cx="57" cy="195" r="10" fill="{s}" stroke="{d}" stroke-width="2"/>'
                f'<circle cx="163" cy="195" r="10" fill="{s}" stroke="{d}" stroke-width="2"/>')
    if piece == "helmet":
        return (f'<path d="M128 40 Q140 14 160 12 Q146 24 140 44 Z" fill="#B23A48"/>'
                f'<path d="M69 86 Q69 36 110 33 Q151 36 151 86 L141 86 L141 72 Q110 63 79 72 L79 86 Z" '
                f'fill="{s}" stroke="{d}" stroke-width="2"/>'
                f'<path d="M79 72 Q110 63 141 72" stroke="{g}" stroke-width="3" fill="none"/>'
                f'<rect x="107" y="66" width="6" height="16" rx="2" fill="{d}"/>')
    if piece == "shield":
        return (f'<path d="M24 160 L80 160 L80 192 Q80 222 52 236 Q24 222 24 192 Z" fill="#2F4B8F" '
                f'stroke="{g}" stroke-width="3"/>'
                f'<path d="M52 166 L52 228 M30 190 L74 190" stroke="{g}" stroke-width="2" opacity="0.8"/>'
                f'<text x="52" y="186" text-anchor="middle" font-family="Georgia,serif" font-size="13" '
                f'font-weight="bold" fill="{g}">B</text>')
    if piece == "sword":
        return (f'<path d="M160 104 L166 96 L172 104 L172 186 L160 186 Z" fill="#E4E9F0" stroke="{d}" stroke-width="1.5"/>'
                f'<path d="M166 102 L166 184" stroke="{d}" stroke-width="1"/>'
                f'<rect x="150" y="185" width="32" height="7" rx="3" fill="{g}"/>'
                f'<rect x="162" y="192" width="8" height="18" fill="#5A3A20"/>'
                f'<circle cx="166" cy="213" r="5" fill="{g}"/>')
    return ""


def avatar_svg(look: dict, worn=(), ghost=(), glow=False, size=220) -> str:
    skin = SKINS.get(look.get("skin"), "#F6D3B3")
    hair = HAIRS.get(look.get("hair"), "#1E1A22")
    outfit = OUTFITS.get(look.get("outfit"), "#3B5BA5")
    long_hair = look.get("style") == "Длинные"
    worn, ghost = set(worn), set(ghost) - set(worn)

    def layer(piece):
        if piece in worn:
            return _armor(piece)
        if piece in ghost:
            return f'<g opacity="0.22">{_armor(piece)}</g>'
        return ""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 290" width="{size}" '
        f'height="{int(size * 290 / 220)}" role="img" aria-label="Character">',
        '<defs><radialGradient id="halo" cx="50%" cy="45%" r="55%">'
        '<stop offset="0%" stop-color="#E0B44A" stop-opacity="0.55"/>'
        '<stop offset="100%" stop-color="#E0B44A" stop-opacity="0"/></radialGradient></defs>',
    ]
    if glow:
        parts.append('<ellipse cx="110" cy="148" rx="108" ry="138" fill="url(#halo)"/>')
    parts.append('<ellipse cx="110" cy="268" rx="70" ry="10" fill="#000" opacity="0.25"/>')
    if long_hair:
        parts.append(f'<path d="M72 80 Q66 130 80 150 L92 120 Z M148 80 Q154 130 140 150 L128 120 Z" fill="{hair}"/>')
    # ноги
    parts.append('<rect x="84" y="196" width="20" height="60" rx="6" fill="#34304A"/>'
                 '<rect x="116" y="196" width="20" height="60" rx="6" fill="#34304A"/>'
                 '<ellipse cx="93" cy="259" rx="14" ry="7" fill="#4A3020"/>'
                 '<ellipse cx="127" cy="259" rx="14" ry="7" fill="#4A3020"/>')
    parts.append(layer("boots"))
    # руки (за туловищем) и туловище
    parts.append(f'<path d="M80 132 L58 190" stroke="{outfit}" stroke-width="17" stroke-linecap="round"/>'
                 f'<path d="M140 132 L162 190" stroke="{outfit}" stroke-width="17" stroke-linecap="round"/>')
    parts.append(f'<path d="M76 126 Q110 116 144 126 L150 200 L70 200 Z" fill="{outfit}"/>'
                 f'<path d="M98 122 L110 140 L122 122" stroke="#fff" stroke-opacity="0.5" stroke-width="3" fill="none"/>')
    parts.append(f'<rect x="102" y="110" width="16" height="14" fill="{skin}"/>')
    parts.append(layer("chest"))
    parts.append(layer("belt"))
    parts.append(layer("shoulders"))
    parts.append(layer("sword"))
    parts.append(f'<circle cx="57" cy="195" r="8" fill="{skin}"/><circle cx="163" cy="195" r="8" fill="{skin}"/>')
    parts.append(layer("gauntlets"))
    # голова
    parts.append(f'<circle cx="110" cy="80" r="38" fill="{skin}"/>')
    parts.append(f'<path d="M71 80 Q72 38 110 37 Q148 38 149 80 Q141 58 112 56 Q96 66 78 62 Q73 70 71 80 Z" fill="{hair}"/>')
    parts.append('<circle cx="96" cy="86" r="4.2" fill="#221C2B"/><circle cx="124" cy="86" r="4.2" fill="#221C2B"/>'
                 '<circle cx="97.5" cy="84.5" r="1.4" fill="#fff"/><circle cx="125.5" cy="84.5" r="1.4" fill="#fff"/>'
                 '<circle cx="88" cy="98" r="5" fill="#F08A8A" opacity="0.35"/>'
                 '<circle cx="132" cy="98" r="5" fill="#F08A8A" opacity="0.35"/>'
                 '<path d="M101 101 Q110 108 119 101" stroke="#221C2B" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    parts.append(layer("helmet"))
    parts.append(layer("shield"))
    parts.append("</svg>")
    return "".join(parts)
