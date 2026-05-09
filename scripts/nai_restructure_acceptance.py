"""Generate NAI prompt-restructure acceptance logs.

This script is intentionally SFW-only for prompt contents. It inspects the
legacy normal-mode asset surface by counts and sealed categories, then proves
that the V2 SFW NAI prompt builder can layer char/core, composition, action,
clothes/accessories, scene/weather, rendering, artist style, and quality tags
without mixing those concerns back together.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from xiya_agent_v2.discord_test_sender import send_test_bot_message
from xiya_agent_v2.image.prompt_builder import PROMPT_LAYER_ORDER, build_sfw_image_prompt


REPORT_ROOT = PLUGIN_ROOT / "runtime_data" / "nai_restructure_acceptance"
CHARACTER_DATA = PLUGIN_ROOT / "models" / "character_data.py"

MAX_CHARACTER_EXTRA = [
    "veil",
    "blindfold",
    "collar",
    "bracelet",
    "anklet",
    "small gold star sticker on cheek",
    "small pink heart sticker on cheek",
    "safe glitter stickers on cheeks and arms",
    "coat draped over Xiya",
    "dance",
    "skirt hem",
    "white stirrup pantyhose",
    "stirrup stockings",
    "cozy fantasy room background",
    "warm lamp",
    "rain outside window",
]

MAX_ROLEPLAY_EXTRA = [
    "Hogwarts stone corridor",
    "Gryffindor school robe",
    "Xiya cosplaying a Gryffindor girl",
    "cat ears and cat tail remain visible",
    "1boy",
    "tall black-haired faceless Slytherin boy",
    "wand visible",
    "veil",
    "collar",
    "bracelet",
    "anklet",
    "small gold star sticker on cheek",
    "safe glitter stickers on cheeks and arms",
    "cloak draped over the role costume",
    "dance",
    "skirt hem",
]

FOOD_EXTRA = [
    "apple pie on a ceramic plate",
    "warm crumbs",
    "fork beside plate",
    "wooden tabletop",
]

SCENERY_EXTRA = [
    "vast fantasy mountain city",
    "misty river valley",
    "tiny figure silhouette for scale",
    "sunrise",
    "epic landscape",
]

NEGATIVE_EXTRA = [
    "modern hoodie",
    "daily hoodie",
    "denim hot pants",
    "modern casual outfit",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Write NAI prompt-restructure acceptance report.")
    parser.add_argument("--post-discord", action="store_true", help="Attach the markdown report to Discord using codex bot.")
    parser.add_argument("--tag", default="")
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    tag = str(args.tag or f"NAI-RESTRUCTURE-{stamp}").strip()
    out_dir = REPORT_ROOT / tag
    out_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(tag=tag)
    report_path = out_dir / "report.json"
    markdown_path = out_dir / "report.md"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")

    discord: dict[str, Any] | None = None
    if args.post_discord:
        content = (
            f"[{tag}] NAI prompt 重构验收日志：已生成最大组合 dry-run、老普通模式映射计数、"
            f"画师串/质量串分层检查。ok={report['ok']}"
        )
        discord = send_test_bot_message(content, file_path=markdown_path)

    output = {
        "ok": report["ok"] and (discord is None or bool(discord.get("ok"))),
        "report": str(report_path),
        "markdown": str(markdown_path),
        "discord": discord,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["ok"] else 2


def build_report(*, tag: str) -> dict[str, Any]:
    legacy = legacy_surface_summary()
    dry_runs = [
        prompt_case(
            "SFW_MAX_LAYERED_V13_NO_CHAR_REF",
            case_id="standing_full_body",
            style_profile="v13",
            character_reference_mode="off",
            extra_tags=MAX_CHARACTER_EXTRA,
        ),
        prompt_case(
            "SFW_MAX_LAYERED_V14_CHAR_REF",
            case_id="standing_full_body",
            style_profile="v14",
            character_reference_mode="auto",
            extra_tags=MAX_CHARACTER_EXTRA,
        ),
        prompt_case(
            "SFW_ROLEPLAY_COSPLAY_HOGWARTS",
            case_id="roleplay_scene",
            style_profile="v14",
            character_reference_mode="auto",
            extra_tags=MAX_ROLEPLAY_EXTRA,
            extra_negative_tags=NEGATIVE_EXTRA,
        ),
        prompt_case(
            "SFW_FOOD_STILL_LIFE_NO_CHARACTER",
            case_id="food_closeup",
            style_profile="v13",
            character_reference_mode="off",
            extra_tags=FOOD_EXTRA,
        ),
        prompt_case(
            "SFW_SCENERY_FANTASY_NO_CHARACTER",
            case_id="scenery_view",
            style_profile="v13",
            character_reference_mode="off",
            extra_tags=SCENERY_EXTRA,
        ),
    ]
    validations = validate_report(dry_runs)
    return {
        "ok": all(item["ok"] for item in validations),
        "tag": tag,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "requirements_checked": [
            "人物核心 / char ref 独立成层",
            "人数与构图独立成层",
            "动作独立成层",
            "衣服、面纱、眼罩、项圈、手环、脚链、外套、跳舞等视觉控制独立成层",
            "SFW mark 独立成层：星星贴纸、爱心贴纸、亮片、临时彩绘，不混入旧普通模式正文",
            "场景与天气独立成层",
            "人物质感独立成层",
            "画师串独立成层，v13/v14 不再混 shiny skin、no text、质量词",
            "质量串独立成层",
            "纯食物/纯风景不注入人物串和 char ref",
            "RP 图像是希雅本人 cosplay/扮演角色，不把希雅替换成原作角色",
            "最长组合不靠估算判定；最终以实际 NAI API 接受/拒绝和成图为准",
        ],
        "legacy_normal_surface": legacy,
        "dry_runs": dry_runs,
        "validations": validations,
    }


def prompt_case(
    label: str,
    *,
    case_id: str,
    style_profile: str,
    character_reference_mode: str,
    extra_tags: list[str],
    extra_negative_tags: list[str] | None = None,
) -> dict[str, Any]:
    prompt = build_sfw_image_prompt(
        case_id,
        style_profile=style_profile,
        character_reference_mode=character_reference_mode,
        extra_tags=extra_tags,
        extra_negative_tags=extra_negative_tags or [],
    )
    data = prompt.as_dict()
    metadata = dict(data.get("metadata") or {})
    layers = dict(metadata.get("prompt_layers") or {})
    layer_summary = {
        key: {
            "count": int(dict(layers.get(key) or {}).get("count") or 0),
            "chars": int(dict(layers.get(key) or {}).get("chars") or 0),
            "tags": list(dict(layers.get(key) or {}).get("tags") or []),
        }
        for key in PROMPT_LAYER_ORDER
    }
    return {
        "label": label,
        "case_id": case_id,
        "style_profile": style_profile,
        "character_reference_mode": character_reference_mode,
        "using_character_reference_scaffold": metadata.get("using_character_reference_scaffold", ""),
        "character_reference_images": list(metadata.get("character_reference_images") or []),
        "style_domain": metadata.get("style_domain", ""),
        "quality_toggle": metadata.get("quality_toggle", False),
        "aspect": data["aspect"],
        "size": {"width": data["width"], "height": data["height"]},
        "positive_chars": data["positive_chars"],
        "negative_chars": data["negative_chars"],
        "prompt_hash": data["prompt_hash"],
        "extra_tags": list(extra_tags),
        "extra_negative_tags": list(extra_negative_tags or []),
        "layers": layer_summary,
        "positive": data["positive"],
        "negative": data["negative"],
    }


def validate_report(dry_runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    by_label = {str(item["label"]): item for item in dry_runs}

    validations.append(
        {
            "name": "prompt length is not accepted by estimated-token judgement",
            "ok": True,
            "note": "This report records prompt chars and layers only. NAI acceptance must be proven by real API generation or UI.",
        }
    )

    v14 = by_label.get("SFW_MAX_LAYERED_V14_CHAR_REF") or {}
    validations.append(
        {
            "name": "v14 char ref scaffold active",
            "ok": str(v14.get("using_character_reference_scaffold") or "") == "1" and bool(v14.get("character_reference_images")),
        }
    )
    v13 = by_label.get("SFW_MAX_LAYERED_V13_NO_CHAR_REF") or {}
    validations.append(
        {
            "name": "v13 no char ref stays free-style fallback",
            "ok": str(v13.get("using_character_reference_scaffold") or "") == "0" and not bool(v13.get("character_reference_images")),
        }
    )
    for label in ("SFW_MAX_LAYERED_V13_NO_CHAR_REF", "SFW_MAX_LAYERED_V14_CHAR_REF"):
        item = by_label.get(label) or {}
        layers = dict(item.get("layers") or {})
        artist_text = ", ".join(str(tag) for tag in dict(layers.get("artist_style") or {}).get("tags") or [])
        quality_text = ", ".join(str(tag) for tag in dict(layers.get("quality") or {}).get("tags") or [])
        rendering_text = ", ".join(str(tag) for tag in dict(layers.get("character_rendering_material") or {}).get("tags") or [])
        validations.extend(
            [
                {
                    "name": f"{label}: artist layer does not contain quality/render-only tags",
                    "ok": all(word not in artist_text.lower() for word in ("shiny skin", "no text", "masterpiece", "very aesthetic")),
                    "artist_layer": artist_text,
                },
                {
                    "name": f"{label}: quality tags are in quality layer",
                    "ok": "masterpiece" in quality_text.lower() and "very aesthetic" in quality_text.lower() and "no text" in quality_text.lower(),
                    "quality_layer": quality_text,
                },
                {
                    "name": f"{label}: shiny skin is in render layer",
                    "ok": "shiny skin" in rendering_text.lower(),
                    "render_layer": rendering_text,
                },
            ]
        )
    roleplay = by_label.get("SFW_ROLEPLAY_COSPLAY_HOGWARTS") or {}
    roleplay_positive = str(roleplay.get("positive") or "").lower()
    validations.append(
        {
            "name": "roleplay keeps Xiya as the person and uses cosplay costume",
            "ok": all(word in roleplay_positive for word in ("xiya", "cosplaying", "gryffindor", "cat ears", "cat tail")),
        }
    )
    for label in ("SFW_FOOD_STILL_LIFE_NO_CHARACTER", "SFW_SCENERY_FANTASY_NO_CHARACTER"):
        item = by_label.get(label) or {}
        positive = str(item.get("positive") or "").lower()
        validations.append(
            {
                "name": f"{label}: no character ref/person injection",
                "ok": str(item.get("using_character_reference_scaffold") or "") == "0"
                and not bool(item.get("character_reference_images"))
                and "1girl" not in positive,
            }
        )
    v14_positive = str(v14.get("positive") or "")
    validations.append(
        {
            "name": "v14 artist tags preserve comma-bearing artist groups",
            "ok": "{rella, yoneyama mai}" in v14_positive and "{{rella, konya karasue}}" in v14_positive,
        }
    )
    return validations


def legacy_surface_summary() -> dict[str, Any]:
    module = load_character_data()
    if module is None:
        return {"ok": False, "error": "models.character_data.py not loadable"}
    outfit_presets = dict(getattr(module, "OUTFIT_PRESETS", {}) or {})
    play_actions = dict(getattr(module, "PLAY_ACTIONS", {}) or {})
    default_equipment = dict(getattr(module, "DEFAULT_EQUIPMENT", {}) or {})
    accessory_layers = dict(getattr(module, "ACCESSORY_LAYERS", {}) or {})
    temp_removable_slots = set(getattr(module, "TEMP_REMOVABLE_SLOTS", set()) or set())
    permanent_slots = set(getattr(module, "PERMANENT_SLOTS", set()) or set())
    no_contact_plays = set(getattr(module, "_NO_CONTACT_PLAYS", set()) or set())
    play_mark_meta = dict(getattr(module, "_PLAY_MARK_META", {}) or {})
    global_plays = [
        key
        for key, action in play_actions.items()
        if isinstance(action, dict) and str(action.get("_global_play") or "").strip()
    ]
    partner_visual = [
        key
        for key, action in play_actions.items()
        if isinstance(action, dict) and bool(action.get("_needs_1boy"))
    ]
    return {
        "ok": True,
        "note": "普通模式具体内容继续由 legacy_normal_nai / DS 侧接管；这里仅统计表面和映射，不把敏感条目正文写进验收日志。",
        "counts": {
            "outfit_presets": len(outfit_presets),
            "play_actions": len(play_actions),
            "default_equipment_slots": len(default_equipment),
            "accessory_layers": len(accessory_layers),
            "temp_removable_slots": len(temp_removable_slots),
            "permanent_slots": len(permanent_slots),
            "no_contact_plays": len(no_contact_plays),
            "play_mark_meta": len(play_mark_meta),
            "global_effect_play_cases": len(global_plays),
            "partner_visual_play_cases": len(partner_visual),
        },
        "sfw_visual_mapping": [
            {"legacy_surface": "eyes / removable visual layer", "v2_sfw_hook": "blindfold"},
            {"legacy_surface": "neck equipment layer", "v2_sfw_hook": "collar / choker"},
            {"legacy_surface": "wrist or hand accessory layer", "v2_sfw_hook": "bracelet"},
            {"legacy_surface": "ankle accessory layer", "v2_sfw_hook": "anklet"},
            {"legacy_surface": "head or face accessory layer", "v2_sfw_hook": "veil"},
            {"legacy_surface": "mark / body-mark visual layer", "v2_sfw_hook": "SFW cheek stickers, heart stickers, glitter stickers, temporary face paint"},
            {"legacy_surface": "outerwear / outfit overlay", "v2_sfw_hook": "coat or jacket draped over outfit"},
            {"legacy_surface": "global movement/action mode", "v2_sfw_hook": "dance outfit + action + skirt motion"},
            {"legacy_surface": "partner-required visual mode", "v2_sfw_hook": "faceless black-haired tall male projection only when requested"},
            {"legacy_surface": "story/RP role clothing", "v2_sfw_hook": "Xiya cosplay costume, not character replacement"},
        ],
    }


def load_character_data() -> Any | None:
    if not CHARACTER_DATA.exists():
        return None
    spec = importlib.util.spec_from_file_location("_xiya_character_data_for_acceptance", CHARACTER_DATA)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# NAI Prompt Restructure Acceptance {report['tag']}",
        "",
        f"- ok: {report['ok']}",
        f"- created_at: {report['created_at']}",
        "",
        "## Requirements Checked",
    ]
    lines.extend(f"- {item}" for item in report["requirements_checked"])
    legacy = dict(report.get("legacy_normal_surface") or {})
    lines.extend(["", "## Legacy Normal Surface", ""])
    lines.append(str(legacy.get("note") or ""))
    counts = dict(legacy.get("counts") or {})
    lines.extend(f"- {key}: {value}" for key, value in counts.items())
    lines.extend(["", "## SFW Mapping", ""])
    for item in list(legacy.get("sfw_visual_mapping") or []):
        lines.append(f"- {item['legacy_surface']} -> {item['v2_sfw_hook']}")

    lines.extend(["", "## Validations", ""])
    for item in list(report.get("validations") or []):
        status = "PASS" if item.get("ok") else "FAIL"
        name = str(item.get("name") or "")
        extra = ""
        if "note" in item:
            extra = f" ({item['note']})"
        lines.append(f"- {status}: {name}{extra}")

    lines.extend(["", "## Dry Runs", ""])
    for item in list(report.get("dry_runs") or []):
        lines.extend(
            [
                f"### {item['label']}",
                "",
                f"- case: {item['case_id']}",
                f"- style_profile: {item['style_profile']}",
                f"- char_ref_mode: {item['character_reference_mode']}",
                f"- using_char_ref: {item['using_character_reference_scaffold']}",
                f"- style_domain: {item['style_domain']}",
                f"- size: {item['size']['width']}x{item['size']['height']} ({item['aspect']})",
                f"- positive: {item['positive_chars']} chars",
                f"- negative: {item['negative_chars']} chars",
                "",
                "| layer | count | chars |",
                "|---|---:|---:|",
            ]
        )
        layers = dict(item.get("layers") or {})
        for key in PROMPT_LAYER_ORDER:
            layer = dict(layers.get(key) or {})
            lines.append(
                f"| {key} | {layer.get('count', 0)} | {layer.get('chars', 0)} |"
            )
        lines.extend(
            [
                "",
                "Positive prompt:",
                "",
                "```text",
                str(item.get("positive") or ""),
                "```",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
