"""SFW NovelAI prompt builder for V2 image tests."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..lorebook.schema import estimate_tokens
from ..runtime_assets import load_nai_character_assets


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
XIYA_CHAR_REF_V1 = PLUGIN_ROOT / "runtime_data" / "nai_references" / "xiya_char_ref_v1.png"

ASPECTS = {
    "portrait": (832, 1216),
    "landscape": (1216, 832),
    "square": (1024, 1024),
}

CHARACTER_RENDER_TAGS = [
    "shiny skin",
]

CHARACTER_FALLBACK_QUALITY_TAGS = [
    "2::very aesthetic::",
    "4::masterpiece::",
]

PROMPT_LAYER_ORDER = (
    "character_core_and_reference",
    "count_and_composition",
    "action",
    "clothes_accessories_props",
    "scene_weather",
    "character_rendering_material",
    "quality",
    "artist_style",
)

FOOD_STYLE_TAGS = [
    "premium food illustration",
    "high-end cookbook still life",
    "appetizing texture focus",
    "detailed tableware and plating",
    "warm natural side lighting",
    "soft edible highlights",
    "rich food surface detail",
]

SCENERY_STYLE_TAGS = [
    "painterly environment illustration",
    "wide atmospheric composition",
    "cinematic lighting",
    "rich environmental detail",
    "background art",
]

SCENERY_STYLE_HINTS = {
    "cyber": [
        "cyberpunk environment art",
        "neon city lighting",
        "wet reflective pavement",
        "high contrast night atmosphere",
    ],
    "ink": [
        "chinese ink wash influence",
        "xianxia landscape painting",
        "misty mountains",
        "elegant brushwork",
    ],
    "fantasy_oil": [
        "grand fantasy oil painting",
        "vast scale",
        "dramatic atmospheric perspective",
        "epic landscape",
    ],
    "dream": [
        "dreamlike background art",
        "soft surreal atmosphere",
        "luminous mist",
        "quiet magical realism",
    ],
}

SFW_ACCESSORY_TAGS = {
    "veil": ["1.4::translucent white veil draped behind cat ears::", "veil fabric visible around hair"],
    "blindfold": ["2.0::soft black blindfold covering both eyes::", "eyes hidden by blindfold"],
    "collar": ["1.4::simple black choker collar::"],
    "bracelet": ["1.3::delicate wrist bracelet::"],
    "anklet": ["1.3::delicate ankle anklet::"],
}

SFW_DAILY_OUTFIT = [
    "fully clothed",
    "consistent SFW daily outfit",
    "oversized light blue hoodie",
    "modest loose hoodie",
    "hoodie covers torso",
    "hoodie hem at hips",
    "denim hot pants",
    "visible short shorts under hoodie",
    "visible legs",
    "elegant low-heel sandals or mary jane shoes",
    "visible elegant footwear",
    "no sneakers",
    "footwear changes do not change hosiery color, coverage, or material",
    "keep the same stockings or pantyhose across the same scene if hosiery is present",
    "long sleeves",
    "sleeves covering wrists",
    "same outfit as previous report image unless owner requests an outfit change",
]

SFW_SELFIE_OUTFIT = [
    "fully clothed",
    "upper-body SFW selfie outfit",
    "oversized light blue hoodie",
    "hood down",
    "hoodie hood behind neck",
    "real cat ears visible above hair",
    "hoodie covers torso",
    "long sleeves",
    "sleeves covering wrists",
    "same hair and face as Xiya",
]

SFW_BEACH_OUTFIT = [
    "safe SFW beach outfit",
    "tasteful SFW beachwear",
    "tasteful beachwear",
    "bikini or rash guard appropriate for beach",
    "casual beach shorts",
    "bare legs",
    "same hair and face as Xiya",
]

SFW_COLD_OUTFIT = [
    "fully clothed winter outfit",
    "warm light blue hoodie layered under coat",
    "winter coat",
    "warm leggings or dark winter pants",
    "scarf",
    "same hair and face as Xiya",
]

SFW_DANCE_OUTFIT = [
    "safe SFW dance outfit",
    "tasteful skirt or dress",
    "flowing skirt",
    "skirt hem visible",
    "dance outfit",
    "elegant low heels or delicate dance shoes",
    "same hair and face as Xiya",
]

SFW_ROLEPLAY_COSPLAY_OUTFIT = [
    "fully clothed",
    "safe SFW roleplay cosplay outfit",
    "Xiya cosplaying the requested role",
    "costume matches the story setting",
    "role outfit is the visible costume",
    "same hair and face as Xiya",
    "cat ears and cat tail remain visible",
    "story-accurate clothing silhouette",
    "school robe or cloak if school setting is requested",
    "period-appropriate outfit if period setting is requested",
    "role props visible if requested",
]


@dataclass(slots=True)
class ImagePrompt:
    case_id: str
    positive: str
    negative: str
    aspect: str
    width: int
    height: int
    required_tags: list[str] = field(default_factory=list)
    forbidden_tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "positive": self.positive,
            "negative": self.negative,
            "aspect": self.aspect,
            "width": self.width,
            "height": self.height,
            "required_tags": list(self.required_tags),
            "forbidden_tags": list(self.forbidden_tags),
            "positive_chars": len(self.positive),
            "negative_chars": len(self.negative),
            "positive_estimated_tokens": estimate_tokens(self.positive),
            "negative_estimated_tokens": estimate_tokens(self.negative),
            "prompt_hash": hashlib.sha1(self.positive.encode("utf-8", errors="ignore")).hexdigest()[:12],
            "metadata": dict(self.metadata),
        }


SFW_CASES: dict[str, dict[str, Any]] = {
    "study_selfie": {
        "aspect": "square",
        "tags": ["selfie", "clear selfie framing", "holding phone", "front camera perspective", "desk", "open book", "soft smile", "cute expression", "indoors"],
        "required": ["selfie", "clear selfie framing", "holding phone", "open book"],
        "forbidden": ["full body", "from behind"],
    },
    "status_selfie": {
        "aspect": "portrait",
        "outfit_profile": "selfie",
        "tags": ["1.8::vertical phone selfie::", "1.8::upper-body selfie crop::", "1.6::shoulders and face in frame::", "1.5::cropped above waist::", "clear selfie framing", "selfie", "holding phone", "front camera perspective", "Xiya's face visible", "cute expression", "small cute hand gesture", "soft smile", "indoors", "cozy room background", "visible room details", "bedroom background", "curtains", "warm wall", "small furniture visible", "current status photo", "upper body"],
        "required": ["vertical phone selfie", "clear selfie framing", "holding phone", "Xiya's face visible", "upper body", "cozy room background", "visible room details"],
        "forbidden": ["full body", "from behind", "open book", "book stack", "desk study", "food-only close-up", "object-only photo", "isolated hand", "simple background", "white background", "plain white background", "empty background", "blank background", "cutout"],
    },
    "dongtian_return": {
        "aspect": "portrait",
        "tags": [
            "vertical composition",
            "cozy fantasy home interior",
            "doorway",
            "threshold",
            "welcoming pose",
            "soft lamp",
            "warm room",
            "small everyday objects",
            "faint projection glow at doorway",
            "over-the-shoulder view from behind the owner",
            "back of black-haired faceless owner projection in foreground",
            "owner shoulder silhouette at the doorway edge",
            "male face hidden",
            "only back of head and shoulder silhouette visible",
            "Xiya welcoming the projection",
        ],
        "required": ["vertical composition", "cozy fantasy home interior", "doorway", "welcoming pose", "faint projection glow", "back of black-haired faceless owner projection", "male face hidden"],
        "forbidden": ["outdoors", "skyscraper", "rainforest", "simple background", "selfie", "realistic man", "full male body", "front-facing male face", "detailed male face"],
        "allow_male_owner_projection": True,
    },
    "dongtian_care": {
        "aspect": "portrait",
        "tags": [
            "vertical composition",
            "cozy fantasy home interior",
            "warm room",
            "soft lamp",
            "gentle caring expression",
            "quiet rest mood",
            "medium shot",
            "holding a folded blanket",
            "arranging blanket on a resting couch",
            "blanket visible",
            "bed or resting couch visible",
            "resting couch in foreground",
            "rest corner",
            "hoodie covers torso",
            "owner implied offscreen",
        ],
        "required": ["vertical composition", "cozy fantasy home interior", "warm room", "gentle caring expression", "holding a folded blanket", "blanket visible", "bed or resting couch visible", "resting couch"],
        "forbidden": ["projection glow", "re-entry portal", "selfie", "realistic man", "full male body", "simple background", "shirt lift", "clothes lift", "bare midriff", "exposed stomach", "close-up face portrait", "headshot"],
    },
    "dongtian_status": {
        "aspect": "portrait",
        "tags": [
            "vertical composition",
            "cozy fantasy home interior",
            "visible room background",
            "warm room",
            "soft lamp",
            "calm status report",
            "Xiya standing in room",
            "neutral gentle expression",
            "third-person scene",
        ],
        "required": ["vertical composition", "cozy fantasy home interior", "visible room background", "Xiya standing in room"],
        "forbidden": ["projection glow", "re-entry portal", "selfie", "realistic man", "full male body", "simple background", "white background", "empty background", "open book", "desk study", "cooking"],
    },
    "dongtian_hug": {
        "aspect": "portrait",
        "tags": [
            "cozy fantasy home interior",
            "warm room",
            "soft lamp",
            "vertical composition",
            "upper body two-person portrait",
            "1boy",
            "tall strong faceless adult man",
            "black hair",
            "broad shoulders",
            "fully clothed man",
            "male face hidden",
            "man seen from behind",
            "Xiya facing viewer over his shoulder",
            "subtle owner projection glow",
            "gentle hug",
            "embracing",
            "tender safe affection",
            "hoodie girl being hugged",
        ],
        "required": ["1girl", "1boy", "tall strong faceless adult man", "black hair", "male face hidden", "gentle hug", "portrait"],
        "forbidden": ["outdoors", "skyscraper", "rainforest", "simple background", "selfie", "front-facing male face", "detailed male face", "nsfw", "nude"],
        "allow_male_owner_projection": True,
    },
    "dongtian_sitting_together": {
        "aspect": "portrait",
        "tags": [
            "cozy fantasy home interior",
            "warm room",
            "visible room background",
            "warm lamp",
            "indoor seat",
            "floor visible",
            "two people sitting side by side",
            "quiet companionship",
            "calm close distance",
            "1boy",
            "tall strong faceless adult man",
            "black hair",
            "broad shoulders",
            "fully clothed man",
            "male face hidden",
            "man seen from side or behind",
            "Xiya sitting beside him",
            "relaxed safe posture",
            "portrait shared scene",
        ],
        "required": ["1girl", "1boy", "sitting side by side", "visible room background", "tall strong faceless adult man", "black hair", "male face hidden", "portrait"],
        "forbidden": ["hugging", "embrace", "kissing", "selfie", "front-facing male face", "detailed male face", "outdoors", "skyscraper", "rainforest", "simple background", "white background", "empty background", "blank background", "nsfw", "nude"],
        "allow_male_owner_projection": True,
    },
    "mirror_outfit": {
        "aspect": "portrait",
        "tags": ["mirror selfie", "visible mirror frame", "phone visible in mirror", "standing", "full body", "neat outfit", "bedroom", "cute pose"],
        "required": ["mirror selfie", "visible mirror frame", "phone visible in mirror", "full body", "standing"],
        "forbidden": ["close-up", "upper body only"],
    },
    "cooking_apron": {
        "aspect": "portrait",
        "tags": ["kitchen", "apron", "cooking", "holding spatula", "steam", "warm lighting"],
        "required": ["kitchen", "apron", "cooking"],
        "forbidden": ["outdoors", "simple background"],
    },
    "chinese_cooking": {
        "aspect": "portrait",
        "tags": ["kitchen", "apron", "wok", "rice bowl", "chopsticks", "steam", "cooking"],
        "required": ["kitchen", "apron", "wok", "rice bowl"],
        "forbidden": ["outdoors", "simple background"],
    },
    "western_cooking": {
        "aspect": "portrait",
        "tags": ["kitchen", "apron", "oven tray", "pasta pot", "plate", "bread", "warm lighting"],
        "required": ["kitchen", "apron", "oven tray", "plate"],
        "forbidden": ["outdoors", "simple background"],
    },
    "rainy_skyscraper_window": {
        "aspect": "landscape",
        "tags": ["floor-to-ceiling window", "rain", "night city", "skyscraper", "neon reflection", "looking outside"],
        "required": ["floor-to-ceiling window", "rain", "night city", "skyscraper"],
        "forbidden": ["sunny", "grassland", "simple background"],
    },
    "standing_full_body": {
        "aspect": "portrait",
        "tags": ["standing", "full body", "head to toe", "head to toe visible", "both legs visible", "feet visible", "clear normal face", "well-drawn eyes", "visible room background", "clear floor", "full body action pose", "dynamic pose", "background supports the character"],
        "required": ["standing", "full body", "head to toe", "both legs visible", "feet visible", "clear normal face", "visible room background"],
        "forbidden": ["close-up", "lower body only", "cropped legs", "missing legs", "hidden feet", "deformed face", "distorted face", "white background", "empty background", "blank background", "isolated character cutout"],
    },
    "hand_closeup": {
        "aspect": "square",
        "tags": ["hand focus", "close-up", "holding pen", "notebook", "desk"],
        "required": ["hand focus", "close-up", "holding pen"],
        "forbidden": ["full body", "distant view"],
    },
    "outdoor_walk_rain": {
        "aspect": "landscape",
        "tags": ["outdoors", "rain", "wet pavement", "umbrella", "city walkway", "overcast"],
        "required": ["outdoors", "rain", "umbrella"],
        "forbidden": ["sunny", "bedroom"],
    },
    "rainforest_walk": {
        "aspect": "landscape",
        "tags": ["rainforest", "dense plants", "wet leaves", "humid air", "filtered green light", "walking path"],
        "required": ["rainforest", "dense plants", "wet leaves"],
        "forbidden": ["grassland", "skyscraper", "simple background"],
    },
    "sunny_rainforest": {
        "aspect": "landscape",
        "tags": ["rainforest", "sunlight", "clear sky glimpsed through leaves", "bright green plants", "walking path"],
        "required": ["rainforest", "sunlight", "bright green plants"],
        "forbidden": ["wet pavement", "night city", "simple background"],
    },
    "meal_table": {
        "aspect": "portrait",
        "tags": ["Xiya sitting at table", "sitting at table", "visible table surface", "table edge visible", "tableware", "plate on table", "food visible on plate", "eating food", "eating a bite", "food near mouth", "fork or small spoon", "home interior", "cafe interior", "warm indoor background", "upper body or waist-up"],
        "required": ["1girl", "Xiya sitting at table", "sitting at table", "visible table surface", "tableware", "food visible", "plate", "eating a bite", "warm indoor background"],
        "forbidden": ["floor", "food-only close-up", "object-only photo", "isolated hand", "no character", "whole untouched food only", "simple background", "solid color background", "empty background", "no table", "no plate"],
    },
    "food_closeup": {
        "aspect": "square",
        "allow_no_character": True,
        "tags": ["pure food close-up", "detailed anime food illustration", "painterly still life", "food is the main subject", "close-up composition", "tableware visible", "tableware", "plate", "steam", "appetizing food", "clear object focus", "rich lighting", "clean tabletop"],
        "required": ["food is the main subject", "close-up composition", "tableware visible"],
        "forbidden": ["person", "portrait", "face", "hand", "disembodied hand", "simple background"],
    },
    "floor_cleanup": {
        "aspect": "landscape",
        "tags": ["kneeling", "cleaning cloth", "small box", "tidying room", "floor visible", "housework"],
        "required": ["kneeling", "cleaning cloth", "floor visible"],
        "forbidden": ["bed", "mirror selfie", "simple background"],
    },
    "library_table": {
        "aspect": "landscape",
        "tags": ["library", "reading table", "bookshelves", "open book", "quiet study", "warm lamp"],
        "required": ["library", "bookshelves", "open book"],
        "forbidden": ["kitchen", "outdoors", "simple background"],
    },
    "bookstore_aisle": {
        "aspect": "landscape",
        "tags": ["bookstore", "narrow aisle", "bookshelves", "holding book", "cozy shop lighting"],
        "required": ["bookstore", "bookshelves", "holding book"],
        "forbidden": ["kitchen", "rainforest", "simple background"],
    },
    "cafe_corner": {
        "aspect": "landscape",
        "tags": ["cafe", "corner seat", "coffee cup", "window table", "notebook", "soft indoor light"],
        "required": ["cafe", "coffee cup", "window table"],
        "forbidden": ["kitchen", "bedroom", "simple background"],
    },
    "tram_window": {
        "aspect": "landscape",
        "tags": ["tram interior", "window seat", "city passing outside", "handrail", "hanging strap", "overhead hand strap", "soft motion blur"],
        "required": ["tram interior", "window seat", "city passing outside", "handrail"],
        "forbidden": ["bedroom", "forest", "simple background"],
    },
    "train_platform": {
        "aspect": "landscape",
        "tags": ["train platform", "station lights", "waiting pose", "railway tracks", "travel bag"],
        "required": ["train platform", "station lights", "railway tracks"],
        "forbidden": ["bedroom", "kitchen", "simple background"],
    },
    "balcony_night": {
        "aspect": "landscape",
        "tags": ["apartment balcony", "night city lights", "railing", "potted plant", "quiet evening"],
        "required": ["apartment balcony", "night city lights", "railing"],
        "forbidden": ["rainforest", "kitchen", "simple background"],
    },
    "seaside_walk": {
        "aspect": "landscape",
        "tags": ["seaside promenade", "ocean", "sea breeze", "distant waves", "walking path"],
        "required": ["seaside promenade", "ocean", "walking path"],
        "forbidden": ["rainforest", "skyscraper", "simple background"],
    },
    "beach_walk": {
        "aspect": "landscape",
        "outfit_profile": "beach",
        "allow_sfw_swimwear": True,
        "tags": ["sunny beach", "shoreline", "ocean waves", "sand", "summer light", "walking by the water"],
        "required": ["beach", "ocean waves", "sand", "tasteful SFW beachwear"],
        "forbidden": ["lingerie", "nudity", "explicit focus", "simple background"],
    },
    "garden_courtyard": {
        "aspect": "landscape",
        "tags": ["garden courtyard", "stone path", "flowers", "bench", "soft sunlight", "greenery"],
        "required": ["garden courtyard", "stone path", "flowers"],
        "forbidden": ["skyscraper", "kitchen", "simple background"],
    },
    "greenhouse_path": {
        "aspect": "landscape",
        "tags": ["greenhouse", "glass roof", "potted plants", "hanging vines", "narrow plant path"],
        "required": ["greenhouse", "glass roof", "potted plants"],
        "forbidden": ["snow", "skyscraper", "simple background"],
    },
    "greenhouse_sitting_together": {
        "aspect": "portrait",
        "tags": [
            "glass greenhouse interior",
            "glass roof",
            "potted plants",
            "hanging vines",
            "narrow plant path",
            "wooden bench beside plant path",
            "1.35::both people seated on wooden bench::",
            "1.3::sitting side by side on bench::",
            "seated pose",
            "knees bent",
            "seated legs",
            "bench under both people",
            "1boy",
            "tall strong faceless adult man",
            "black hair",
            "broad shoulders",
            "fully clothed man",
            "male face hidden",
            "man seen from side or behind",
            "Xiya and owner projection sitting together",
            "quiet rest mood",
        ],
        "required": ["glass greenhouse interior", "glass roof", "potted plants", "wooden bench", "both people seated on wooden bench", "sitting side by side on bench", "1boy", "male face hidden"],
        "forbidden": ["extra boys", "multiple men", "crowd", "lab coat", "scientist", "standing pose", "standing", "standing together", "walking", "walking away", "full standing figure", "snow", "skyscraper", "simple background"],
        "allow_male_owner_projection": True,
    },
    "bedroom_reading": {
        "aspect": "landscape",
        "tags": ["bedroom", "bedside lamp", "open book", "blanket", "quiet room", "soft pillow"],
        "required": ["bedroom", "bedside lamp", "open book"],
        "forbidden": ["kitchen", "outdoors", "simple background"],
    },
    "snowy_street": {
        "aspect": "landscape",
        "outfit_profile": "cold",
        "tags": ["snowy street", "falling snow", "street lamp", "winter coat", "visible breath"],
        "required": ["snowy street", "falling snow", "street lamp"],
        "forbidden": ["summer beach", "rainforest", "simple background"],
    },
    "foggy_alley": {
        "aspect": "landscape",
        "tags": ["foggy alley", "street lamps", "soft fog", "wet stone path", "quiet city"],
        "required": ["foggy alley", "street lamps", "soft fog"],
        "forbidden": ["sunny", "beach", "simple background"],
    },
    "music_room": {
        "aspect": "landscape",
        "tags": ["music room", "sheet music", "wooden floor", "music stand", "soft stage light"],
        "required": ["music room", "sheet music", "music stand"],
        "forbidden": ["kitchen", "outdoors", "simple background"],
    },
    "quiet_shape_room": {
        "aspect": "landscape",
        "tags": ["small quiet room", "gold round lamp", "green square window", "wooden cabinet", "warm dark interior", "simple cozy furniture", "night outside window"],
        "required": ["small quiet room", "gold round lamp", "green square window"],
        "forbidden": ["music stand", "sheet music", "piano", "organ pipes", "simple background", "barefoot", "bare feet"],
    },
    "pipe_organ_hall": {
        "aspect": "landscape",
        "tags": ["pipe organ hall", "large organ pipes", "keyboard console", "arched hall", "stained glass"],
        "required": ["pipe organ hall", "large organ pipes", "keyboard console"],
        "forbidden": ["piano room", "upright piano", "simple background"],
    },
    "piano_room": {
        "aspect": "landscape",
        "tags": ["piano room", "grand piano", "piano bench", "sitting on piano bench", "hands near piano keys", "playing piano pose", "sheet music", "sunlit room"],
        "required": ["piano room", "grand piano", "piano bench", "hands near piano keys"],
        "forbidden": ["organ pipes", "cathedral nave", "simple background", "kneeling", "sitting on floor", "floor sitting"],
    },
    "dream_lantern_path": {
        "aspect": "landscape",
        "tags": ["dreamlike path", "floating lanterns", "soft glow", "misty blue light", "surreal garden"],
        "required": ["dreamlike path", "floating lanterns", "soft glow"],
        "forbidden": ["kitchen", "office", "simple background"],
    },
    "starry_rooftop": {
        "aspect": "landscape",
        "tags": ["rooftop", "starry sky", "city horizon", "night breeze", "telescope"],
        "required": ["rooftop", "starry sky", "city horizon"],
        "forbidden": ["rainforest", "kitchen", "simple background"],
    },
    "aquarium_walk": {
        "aspect": "landscape",
        "tags": ["aquarium tunnel", "blue water light", "large fish silhouettes", "glass tunnel", "walking"],
        "required": ["aquarium tunnel", "blue water light", "glass tunnel"],
        "forbidden": ["bedroom", "kitchen", "simple background"],
    },
    "museum_gallery": {
        "aspect": "landscape",
        "tags": ["museum gallery", "framed paintings", "polished floor", "quiet exhibit", "soft spotlights"],
        "required": ["museum gallery", "framed paintings", "soft spotlights"],
        "forbidden": ["kitchen", "bedroom", "simple background"],
    },
    "observatory_dome": {
        "aspect": "landscape",
        "tags": ["observatory dome", "large telescope", "open star slit", "night sky", "control desk"],
        "required": ["observatory dome", "large telescope", "night sky"],
        "forbidden": ["kitchen", "beach", "simple background"],
    },
    "moonlit_bridge": {
        "aspect": "landscape",
        "tags": ["moonlit bridge", "river reflection", "night walkway", "soft moonlight", "distant lamps"],
        "required": ["moonlit bridge", "river reflection", "soft moonlight"],
        "forbidden": ["kitchen", "bedroom", "simple background"],
    },
    "festival_street": {
        "aspect": "landscape",
        "tags": ["festival street", "paper lanterns", "food stalls", "evening crowd", "warm lights"],
        "required": ["festival street", "paper lanterns", "food stalls"],
        "forbidden": ["empty room", "simple background"],
    },
    "scenery_view": {
        "aspect": "landscape",
        "allow_no_character": True,
        "tags": ["pure scenery view", "detailed anime background art", "painterly environment illustration", "scenery is the main subject", "wide environmental composition", "wide landscape", "environment focus", "clear background details", "atmospheric lighting", "rich lighting"],
        "required": ["scenery is the main subject", "wide environmental composition"],
        "forbidden": ["person", "portrait", "face", "selfie"],
    },
    "story_scene": {
        "aspect": "landscape",
        "outfit_profile": "roleplay_cosplay",
        "tags": ["storybook illustration", "narrative scene", "story environment", "Xiya acting as the story heroine", "key story prop visible", "fantasy background supports the story"],
        "required": ["storybook illustration", "narrative scene", "Xiya acting as the story heroine", "key story prop visible"],
        "forbidden": ["selfie", "phone", "simple background", "modern hoodie", "daily hoodie", "denim hot pants", "modern casual outfit"],
    },
    "roleplay_scene": {
        "aspect": "landscape",
        "outfit_profile": "roleplay_cosplay",
        "tags": ["cinematic scene", "interactive staging", "Xiya cosplaying the role", "fantasy interior", "dramatic lighting"],
        "required": ["cinematic scene", "Xiya cosplaying the role", "fantasy interior", "dramatic lighting"],
        "forbidden": ["selfie", "simple background", "modern hoodie", "daily hoodie", "denim hot pants", "modern casual outfit"],
    },
}


def sfw_image_cases() -> list[str]:
    return sorted(SFW_CASES)


def build_sfw_image_prompt(
    case_id: str,
    *,
    extra_tags: list[str] | None = None,
    extra_negative_tags: list[str] | None = None,
    style_profile: str = "v13",
    character_reference_mode: str = "auto",
) -> ImagePrompt:
    case = dict(SFW_CASES.get(case_id) or {})
    if not case:
        raise KeyError(f"Unknown SFW image case: {case_id}")
    normalized_ref_mode = _normalize_character_reference_mode(character_reference_mode)
    requested_style = str(style_profile or "v13").strip().lower()
    if requested_style.isdigit():
        requested_style = f"v{requested_style}"
    use_character_reference_scaffold = (
        normalized_ref_mode in {"auto", "required"}
        and requested_style == "v14"
        and XIYA_CHAR_REF_V1.exists()
        and not bool(case.get("allow_no_character"))
    )
    assets = load_nai_character_assets(
        style_profile=style_profile,
        use_character_reference=use_character_reference_scaffold,
        safe_sfw=True,
    )
    base_aspect = str(case.get("aspect") or "portrait")
    aspect = _aspect_for_focus(case_id, case, extra_tags=extra_tags, base_aspect=base_aspect)
    width, height = ASPECTS.get(aspect, ASPECTS["portrait"])
    roleplay_cosplay_scene = str(case.get("outfit_profile") or "").strip().lower() == "roleplay_cosplay"
    allow_male_owner = bool(case.get("allow_male_owner_projection")) or _extra_tags_request_male_owner(extra_tags)
    allow_no_character = bool(case.get("allow_no_character"))
    raw_extra = " ".join(str(tag or "") for tag in list(extra_tags or [])).lower()
    tiny_figure_scenery = bool(allow_no_character and _raw_requests_tiny_figure(raw_extra))
    dance_requested = _raw_requests_dance(raw_extra)
    hosiery_requested = _raw_requests_hosiery(raw_extra)
    stirrup_requested = _raw_requests_stirrup(raw_extra)
    shoe_removed_requested = _raw_requests_shoes_removed(raw_extra)
    compact_footwear_prompt = bool(shoe_removed_requested and stirrup_requested and not allow_no_character and not allow_male_owner)
    style_domain = _style_domain_for_case(case_id, case, extra_tags)
    quality_toggle = _quality_toggle_for_domain(style_domain)
    style_parts = _style_parts_for_domain(style_domain, raw_extra=raw_extra, assets=assets)
    render_parts = _render_parts_for_domain(style_domain)
    quality_parts = _quality_parts_for_domain(style_domain, quality_toggle=quality_toggle)
    reference_images = _character_reference_images_for(style_domain, assets)
    outfit_parts = _sfw_outfit_parts(case, extra_tags=extra_tags, allow_no_character=allow_no_character)
    accessory_parts = _sfw_accessory_parts(raw_extra, lower_body_only=compact_footwear_prompt) if not allow_no_character else []
    if compact_footwear_prompt:
        outfit_parts = [
            "fully clothed",
            "oversized light blue hoodie",
            "denim hot pants",
            "visible short shorts under hoodie",
            "white stirrup pantyhose",
            "open toe and open heel stirrup pantyhose",
            "white stirrup strap under each foot arch",
            "2.2::white stirrup strap under foot arch::",
            "toes and heels visible outside the pantyhose",
            "same white stirrup pantyhose remains unchanged",
            "not cotton socks",
            "2.5::knees-to-feet seated close-up focused on legwear and feet::",
            "2.3::open toes and open heels visible with white stirrup fabric::",
            "2.4::seated on a low cushion knees bent feet forward::",
            "face and head out of frame",
            "upper body mostly cropped out",
            "both feet are not touching footwear",
        ]
        style_parts = _drop_style_items(style_parts, {"wlop", "fuzichoco", "konya karasue"})
    if allow_no_character:
        if tiny_figure_scenery:
            character_parts = [
                    "tiny distant human silhouette for scale",
                    "scenery remains the main subject",
                    "no close character portrait",
            ]
        else:
            character_parts = [
                    "no humans",
                    "no character",
            ]
        clothes_parts: list[str] = []
        render_parts = ["detailed illustration", "rich lighting", *render_parts]
    else:
        if compact_footwear_prompt:
            character_parts = [
                    "1girl",
                    "Xiya lower-body clothing detail",
                    "knees-to-feet close-up of seated anime girl",
                    "pale blue cat tail partly visible",
            ]
            clothes_parts = [
                    "light blue hoodie hem visible at top of frame",
                    "denim hot pants visible at top of frame",
                    "safe SFW outfit",
                    *outfit_parts,
                    *accessory_parts,
            ]
            render_parts = ["clean flat-color anime illustration", *render_parts]
        else:
            if str(assets.get("using_character_reference_scaffold") or "") == "1":
                character_parts = [
                        "1girl",
                        *([] if str(assets.get("character_base", "")).strip().lower() == "1girl" else [assets.get("character_base", "")]),
                        assets.get("character_tags", ""),
                ]
            else:
                character_parts = [
                        "1girl",
                        assets.get("character_tags", "") or assets.get("character_base", ""),
                ]
            clothes_parts = [
                    "safe SFW outfit",
                    *outfit_parts,
                    *accessory_parts,
            ]
            if roleplay_cosplay_scene:
                clothes_parts.extend(
                    [
                        "role costume is dominant and clearly visible",
                        "role costume, scene props, and background carry the roleplay setting",
                    ]
                )
    composition_parts = [*_subject_focus_tags(case_id, case, extra_tags)]
    action_parts = _action_parts_for_case(case_id, case, raw_extra)
    scene_parts: list[str] = []
    blindfold_requested = _raw_requests_blindfold(raw_extra)
    for tag in list(case.get("tags") or []):
        clean_case_tag = str(tag or "").strip()
        if shoe_removed_requested and _shoe_removed_scene_tag_conflict(clean_case_tag):
            continue
        if blindfold_requested and _blindfold_scene_tag_conflict(clean_case_tag):
            continue
        scene_parts.append(clean_case_tag)
    if extra_tags:
        for tag in extra_tags:
            clean = str(tag or "").strip()
            if not clean:
                continue
            if allow_no_character and _no_character_extra_tag_should_skip(clean):
                continue
            if _raw_requests_hosiery(raw_extra) and clean.lower() in {"barefoot", "bare feet", "bare toes", "光脚", "赤脚", "裸足"}:
                continue
            if shoe_removed_requested and "pair of sandals placed on the floor beside both feet" in clean.lower():
                continue
            if compact_footwear_prompt and _compact_footwear_extra_tag_should_skip(clean):
                continue
            if _tail_diagnostic_extra_tag_should_skip(clean):
                continue
            if not allow_no_character and _visual_control_extra_tag_should_skip(clean):
                continue
            scene_parts.append(clean)
    positive_mode = "sfw_positive_beach" if bool(case.get("allow_sfw_swimwear")) else "sfw_positive"
    prompt_layers = {
        "character_core_and_reference": character_parts,
        "count_and_composition": composition_parts,
        "action": action_parts,
        "clothes_accessories_props": clothes_parts,
        "scene_weather": scene_parts,
        "character_rendering_material": render_parts,
        "artist_style": style_parts,
        "quality": quality_parts,
    }
    tail_diagnostic_parts = _tail_diagnostic_parts(extra_tags)
    positive = _join_tags([*_flatten_prompt_layers(prompt_layers), *tail_diagnostic_parts], mode=positive_mode)
    negative_parts = [
        *(str(tag) for tag in list(extra_negative_tags or []) if str(tag).strip()),
        *(str(tag) for tag in list(case.get("forbidden") or []) if str(tag).strip()),
        *([] if compact_footwear_prompt else [_case_negative_sfw(assets.get("negative_sfw", ""), allow_male=allow_male_owner)]),
        "nsfw",
        "explicit",
        "nude",
        "uncensored",
        "explicit sexual focus",
        "sexualized composition",
        "cleavage focus",
        "lingerie",
        "underwear",
        *([] if bool(case.get("allow_sfw_swimwear")) else ["swimsuit", "bikini"]),
        "sneakers",
        "athletic shoes",
        "running shoes",
        "cotton socks",
        "weird multicolor socks",
        "red and blue stockings",
        "mismatched stockings",
        "random hosiery color change",
        "stockings changing color between shots",
        "stockings changing type between shots",
        "pantyhose changing color when shoes are removed",
        "pantyhose changing type when shoes are removed",
        *_hosiery_negative_parts(raw_extra),
        "see-through clothes",
        "bare chest",
        "exposed genitals",
        "cameltoe",
        "nipples",
        "thong",
        "micro bikini",
        "simple background",
        "bad anatomy",
        "bad hands",
        "missing legs",
        "cropped legs",
        "2girls",
        "multiple girls",
        "duplicate girl",
        "cloned girl",
        "bad feet",
        "deformed feet",
        "distorted face",
        "deformed face",
        "text",
        "watermark",
        "low quality",
    ]
    if "red cube" in raw_extra:
        negative_parts.extend(["standing on red cube", "red cube pedestal", "large red cube platform", "cube under both feet"])
    outfit_profile = str(case.get("outfit_profile") or "daily").strip().lower()
    if outfit_profile == "daily" and not dance_requested:
        daily_negatives = ["jeans", "long pants", "pants only", "leggings"]
        if not hosiery_requested:
            daily_negatives.append("tights")
        if shoe_removed_requested:
            if stirrup_requested:
                daily_negatives.extend(["feet without pantyhose", "no hosiery"])
            else:
                daily_negatives.extend(["one shoe on foot", "shoes on feet"])
        else:
            daily_negatives.extend(["barefoot", "bare feet", "no shoes"])
        negative_parts.extend(daily_negatives)
    elif dance_requested:
        dance_negatives = ["jeans", "long pants", "pants only", "hoodie and jeans only"]
        if not _raw_requests_barefoot(raw_extra):
            dance_negatives.extend(["barefoot", "bare feet", "no shoes"])
        negative_parts.extend(dance_negatives)
    elif outfit_profile == "roleplay_cosplay":
        negative_parts.extend(
            [
                "modern hoodie",
                "oversized hoodie",
                "daily hoodie",
                "denim hot pants",
                "daily shorts",
                "modern casual outfit",
                "streetwear",
            ]
        )
    if allow_no_character and not tiny_figure_scenery:
        negative_parts.extend(["1girl", "girl", "person", "human", "face", "portrait", "hands", "body"])
    elif tiny_figure_scenery:
        negative_parts.extend(["portrait", "close-up face", "large character", "character close-up", "selfie"])
    elif not allow_male_owner:
        negative_parts.extend(["1boy", "male", "male focus", "hetero"])
    if case_id == "status_selfie" and _raw_requests_food(" ".join(str(tag or "") for tag in list(extra_tags or []))):
        negative_parts.extend(
            [
                "food printed on phone",
                "food phone case",
                "phone case food",
                "food fused with phone",
                "phone covering mouth",
                "food-only close-up",
                "object-only photo",
                "isolated hand",
            ]
        )
    if str(case_id or "").endswith("_selfie") or "selfie" in raw_extra:
        negative_parts.extend(
            [
                "full body",
                "full-length portrait",
                "head to toe",
                "standing full body",
                "lower body",
                "legs in frame",
                "feet in frame",
                "visible feet",
                "visible sandals",
                "shoes in frame",
                "mirror selfie",
                "hood up",
                "cat ear hood",
                "animal hood",
                "fake cat ears on hood",
                "hat ears",
                "camera app interface",
                "smartphone camera UI",
                "phone screen UI",
                "visible UI icons",
                "on-screen text",
                "japanese text",
                "camera mode labels",
                "green hair",
                "mint hair",
                "teal hair",
                "turquoise hair",
                "blue-green hair",
            ]
        )
    required_tags = []
    for tag in list(case.get("required") or []):
        clean_required = str(tag or "").strip()
        if shoe_removed_requested and _shoe_removed_scene_tag_conflict(clean_required):
            continue
        if blindfold_requested and _blindfold_scene_tag_conflict(clean_required):
            continue
        required_tags.append(clean_required)
    negative = _join_tags(negative_parts, mode="negative")
    return ImagePrompt(
        case_id=case_id,
        positive=positive,
        negative=negative,
        aspect=aspect,
        width=width,
        height=height,
        required_tags=required_tags,
        forbidden_tags=list(case.get("forbidden") or []),
        metadata={
            "builder": "v2_sfw",
            "style_source": "models.character_data",
            "style_profile_requested": assets.get("style_profile_requested", ""),
            "style_profile_resolved": assets.get("style_profile_resolved", ""),
            "available_style_profiles": assets.get("available_style_profiles", ""),
            "character_reference_mode": normalized_ref_mode,
            "style_supports_character_reference": assets.get("style_supports_character_reference", ""),
            "using_character_reference_scaffold": assets.get("using_character_reference_scaffold", ""),
            "sfw_sanitized_character": assets.get("sfw_sanitized_character", ""),
            "extra_tags": list(extra_tags or []),
            "extra_negative_tags": list(extra_negative_tags or []),
            "base_aspect": base_aspect,
            "aspect_source": "focus_override" if aspect != base_aspect else "case_default",
            "allow_male_owner_projection": allow_male_owner,
            "allow_no_character": allow_no_character,
            "xiya_roleplay_cosplay_scene": roleplay_cosplay_scene,
            "compact_footwear_prompt": compact_footwear_prompt,
            "style_domain": style_domain,
            "quality_toggle": quality_toggle,
            "prompt_layer_order": list(PROMPT_LAYER_ORDER),
            "prompt_layers": _prompt_layers_metadata(prompt_layers),
            "tail_diagnostic_tags": tail_diagnostic_parts,
            "character_reference_images": reference_images,
            "character_reference_type": "character" if reference_images else "",
            "character_reference_strength": 0.68 if reference_images else 0,
            "character_reference_fidelity": 0.55 if reference_images else 0,
        },
    )


def _style_domain_for_case(case_id: str, case: dict[str, Any], extra_tags: list[str] | None) -> str:
    raw = " ".join([case_id, *[str(tag or "") for tag in list(case.get("tags") or [])], *[str(tag or "") for tag in list(extra_tags or [])]]).lower()
    if bool(case.get("allow_no_character")):
        if case_id == "food_closeup" or _raw_requests_food(raw):
            return "food"
        return "scenery"
    return "character"


def _quality_toggle_for_domain(style_domain: str) -> bool:
    # NAI quality tags currently help character images; food/scenery get lean domain quality strings.
    return str(style_domain or "") == "character"


def _style_parts_for_domain(style_domain: str, *, raw_extra: str, assets: dict[str, str]) -> list[str]:
    domain = str(style_domain or "character")
    if domain == "food":
        return [*FOOD_STYLE_TAGS]
    if domain == "scenery":
        parts = [*SCENERY_STYLE_TAGS]
        if any(marker in raw_extra for marker in ("梦", "梦幻", "dream", "surreal", "lantern", "tram", "电车")):
            parts.extend(SCENERY_STYLE_HINTS["dream"])
            return parts
        if any(marker in raw_extra for marker in ("水墨", "山水", "中式", "仙侠", "shanshui")):
            parts.extend(SCENERY_STYLE_HINTS["ink"])
            return parts
        if any(marker in raw_extra for marker in ("cyber", "neon", "skyscraper", "night city")):
            parts.extend(SCENERY_STYLE_HINTS["cyber"])
        elif any(marker in raw_extra for marker in ("ink", "chinese", "xianxia", "shan shui", "山水", "水墨")):
            parts.extend(SCENERY_STYLE_HINTS["ink"])
        elif any(marker in raw_extra for marker in ("fantasy", "epic", "vast", "castle", "mountain")):
            parts.extend(SCENERY_STYLE_HINTS["fantasy_oil"])
        return parts
    parts = [assets.get("style_tags", "")]
    if any(marker in raw_extra for marker in ("knees-to-feet", "lower-body", "shoes removed", "shoes off")):
        return _drop_style_items(parts, {"wlop", "fuzichoco"})
    return parts


def _quality_parts_for_domain(style_domain: str, *, quality_toggle: bool) -> list[str]:
    domain = str(style_domain or "character")
    if domain == "character":
        return [*CHARACTER_FALLBACK_QUALITY_TAGS, "no text"]
    if domain == "food":
        return ["best quality", "masterpiece", "clear object focus"]
    return ["best quality", "masterpiece", "atmospheric perspective"]


def _render_parts_for_domain(style_domain: str) -> list[str]:
    if str(style_domain or "character") == "character":
        return [*CHARACTER_RENDER_TAGS]
    return []


def _action_parts_for_case(case_id: str, case: dict[str, Any], raw_extra: str) -> list[str]:
    raw = " ".join([str(case_id or ""), *[str(tag or "") for tag in list(case.get("tags") or [])], raw_extra]).lower()
    parts: list[str] = []
    if any(marker in raw for marker in ("hug", "hugging", "embrace", "抱住", "拥抱")):
        parts.extend(["gentle safe embrace", "clear hugging action"])
    if any(marker in raw for marker in ("selfie", "phone photo", "自拍")):
        parts.extend(["holding phone", "front camera perspective"])
    if _raw_requests_food(raw):
        parts.extend(["food visible as requested", "natural eating or presenting pose"])
    if _raw_requests_dance(raw):
        parts.extend(["graceful dancing pose", "skirt motion follows dance"])
    if any(marker in raw for marker in ("cooking", "kitchen", "做饭", "烹饪")):
        parts.extend(["cooking action", "utensil or cookware used naturally"])
    if _raw_requests_shoes_removed(raw):
        parts.extend(["shoes removed action state", "feet separated from footwear"])
    return parts[:12]


def _character_reference_images_for(style_domain: str, assets: dict[str, str]) -> list[str]:
    if str(style_domain or "") != "character":
        return []
    if str(assets.get("using_character_reference_scaffold") or "") != "1":
        return []
    if str(assets.get("style_profile_resolved") or "").strip().lower() != "v14":
        return []
    if not XIYA_CHAR_REF_V1.exists():
        return []
    return [str(XIYA_CHAR_REF_V1)]


def _normalize_character_reference_mode(value: str) -> str:
    raw = str(value or "auto").strip().lower()
    if raw in {"0", "false", "no", "off", "disable", "disabled", "legacy", "long", "old"}:
        return "off"
    if raw in {"required", "require", "force", "on", "true", "yes"}:
        return "required"
    return "auto"


def _flatten_prompt_layers(layers: dict[str, list[str]]) -> list[str]:
    parts: list[str] = []
    for key in PROMPT_LAYER_ORDER:
        parts.extend(layers.get(key) or [])
    return parts


def _prompt_layers_metadata(layers: dict[str, list[str]]) -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}
    for key in PROMPT_LAYER_ORDER:
        values = [str(part).strip() for part in list(layers.get(key) or []) if str(part).strip()]
        text = ", ".join(values)
        metadata[key] = {
            "count": len(values),
            "chars": len(text),
            "estimated_tokens": estimate_tokens(text),
            "tags": values,
        }
    return metadata


def _drop_style_items(parts: list[str], banned_words: set[str]) -> list[str]:
    kept: list[str] = []
    for part in parts:
        tags: list[str] = []
        for tag in _split_nai_tags(str(part or "")):
            if not tag:
                continue
            if any(word in tag.lower() for word in banned_words):
                continue
            tags.append(tag)
        if tags:
            kept.append(", ".join(tags))
    return kept


def _split_nai_tags(value: str) -> list[str]:
    tags: list[str] = []
    current: list[str] = []
    curly = 0
    square = 0
    weighted = False
    text = str(value or "")
    i = 0
    while i < len(text):
        if text.startswith("::", i):
            if weighted:
                current.append("::")
                weighted = False
                i += 2
                continue
            prefix = "".join(current).strip().lstrip(":")
            try:
                float(prefix)
            except ValueError:
                pass
            else:
                current.append("::")
                weighted = True
                i += 2
                continue
        char = text[i]
        if char == "," and curly <= 0 and square <= 0:
            if not weighted:
                tag = "".join(current).strip()
                if tag:
                    tags.append(tag)
                current = []
                i += 1
                continue
        current.append(char)
        if char == "{":
            curly += 1
        elif char == "}":
            curly = max(0, curly - 1)
        elif char == "[":
            square += 1
        elif char == "]":
            square = max(0, square - 1)
        i += 1
    tag = "".join(current).strip()
    if tag:
        tags.append(tag)
    return tags


def _sfw_accessory_parts(raw: str, *, lower_body_only: bool = False) -> list[str]:
    parts: list[str] = []
    markers = {
        "veil": ("veil", "face veil", "bridal veil", "面纱", "头纱", "轻纱"),
        "blindfold": ("blindfold", "eye mask", "眼罩", "蒙眼", "蒙住眼睛"),
        "collar": ("collar", "choker", "项圈", "颈圈", "颈环"),
        "bracelet": ("bracelet", "wristband", "wrist cuff", "手环", "手镯", "腕带", "腕环"),
        "anklet": ("anklet", "ankle bracelet", "ankle cuff", "脚链", "脚环", "脚镯"),
    }
    for key, keys in markers.items():
        if lower_body_only and key not in {"anklet"}:
            continue
        if any(marker in raw for marker in keys):
            parts.extend(SFW_ACCESSORY_TAGS[key])
    return parts[:8]


def _sfw_outfit_parts(case: dict[str, Any], *, extra_tags: list[str] | None, allow_no_character: bool) -> list[str]:
    if allow_no_character:
        return []
    profile = str(case.get("outfit_profile") or "daily").strip().lower()
    raw = " ".join(str(tag or "") for tag in list(extra_tags or [])).lower()
    if profile == "beach":
        return [*SFW_BEACH_OUTFIT]
    if profile == "cold":
        return [*SFW_COLD_OUTFIT]
    if profile == "selfie":
        return [*SFW_SELFIE_OUTFIT]
    if profile == "roleplay_cosplay":
        parts = [*SFW_ROLEPLAY_COSPLAY_OUTFIT]
        if any(
            marker in raw
            for marker in (
                "hogwarts",
                "gryffindor",
                "slytherin",
                "ravenclaw",
                "hufflepuff",
                "wizard school",
                "magic school",
                "霍格沃茨",
                "格兰芬多",
                "斯莱特林",
                "拉文克劳",
                "赫奇帕奇",
                "魔法学校",
            )
        ):
            parts.extend(
                [
                    "Hogwarts-style school robe",
                    "wizard school uniform",
                    "school cloak",
                    "white shirt",
                    "pleated skirt",
                    "house-color tie if requested",
                    "wand or book if requested",
                ]
            )
        if any(marker in raw for marker in ("dance", "dancing", "ballroom", "waltz", "skirt hem", "dress", "跳舞", "舞蹈", "舞步", "华尔兹", "裙摆", "裙子", "连衣裙")):
            parts.extend(["tasteful role costume dress", "flowing skirt", "skirt hem visible"])
        if _raw_requests_coat_drape(raw):
            parts.extend(["front-open outer cloak over the role costume", "outer layer visible but not replacing the costume"])
        return parts
    coat_requested = _raw_requests_coat_drape(raw)
    dance_requested = _raw_requests_dance(raw)
    if coat_requested and dance_requested:
        if _raw_requests_hosiery(raw):
            return [
                "fully clothed",
                "safe SFW flowing dance dress",
                "visible skirt hem",
                *_hosiery_positive_parts(raw),
                "front-open dark cropped jacket over the dance outfit",
                "jacket does not hide the skirt hem",
                "same hair and face as Xiya",
            ]
        return [
            *SFW_DANCE_OUTFIT,
            "front-open dark cropped jacket over the dance outfit",
            "dress and skirt remain visible under the jacket",
            "jacket sleeves hanging naturally at sides",
            "outer layer does not hide skirt hem",
        ]
    if coat_requested:
        return [
            "fully clothed",
            "consistent SFW daily outfit",
            "oversized light blue hoodie",
            "front-open dark cropped jacket over her light blue hoodie",
            "light blue hoodie remains visible under the jacket",
            "jacket sleeves hanging naturally at sides",
            "denim hot pants",
            "visible short shorts under hoodie",
            "visible legs",
            "elegant low-heel sandals or mary jane shoes",
            "visible elegant footwear",
            "same hair and face as Xiya",
        ]
    if dance_requested:
        if _raw_requests_hosiery(raw):
            return [
                "fully clothed",
                "safe SFW flowing dance dress",
                "visible skirt hem",
                *_hosiery_positive_parts(raw),
                "same hair and face as Xiya",
            ]
        return [*SFW_DANCE_OUTFIT]
    if _raw_requests_hosiery(raw):
        hosiery_parts = _hosiery_positive_parts(raw)
        return [
            "fully clothed",
            "consistent SFW daily outfit",
            "oversized light blue hoodie",
            "denim hot pants",
            "visible short shorts under hoodie",
            *hosiery_parts,
            "no cotton socks",
            "same hair and face as Xiya",
        ]
    return [*SFW_DAILY_OUTFIT]


def _raw_requests_dance(raw: str) -> bool:
    return any(marker in raw for marker in ("dance", "dancing", "solo xiya dance", "flowing skirt", "skirt hem", "dress", "跳舞", "舞蹈", "舞步", "华尔兹", "裙摆", "裙子", "连衣裙"))


def _raw_requests_coat_drape(raw: str) -> bool:
    return any(
        marker in raw
        for marker in (
            "coat draped over xiya",
            "coat over her light blue hoodie",
            "coat over xiya",
            "jacket draped over xiya",
            "jacket over her light blue hoodie",
            "jacket sleeves hanging",
            "outerwear",
            "coat",
            "jacket",
            "披肩",
            "披到你肩上",
            "披在肩上",
            "披上",
            "外套",
            "外套披",
            "夹克",
            "披外套",
        )
    )


def _raw_requests_hosiery(raw: str) -> bool:
    return any(
        marker in raw
        for marker in (
            "stirrup stockings",
            "stirrup pantyhose",
            "white stirrup pantyhose",
            "black stirrup pantyhose",
            "stockings",
            "pantyhose",
            "thighhighs",
            "thigh highs",
            "garter stockings",
            "white stockings",
            "black stockings",
            "hosiery",
            "踩脚",
            "白丝",
            "黑丝",
            "丝袜",
            "连裤袜",
            "长筒袜",
            "吊带袜",
            "全包",
            "包脚",
        )
    )


def _raw_requests_stirrup(raw: str) -> bool:
    return any(marker in raw for marker in ("stirrup", "踩脚", "open toe and open heel"))


def _raw_requests_blindfold(raw: str) -> bool:
    return any(marker in raw for marker in ("blindfold", "eye mask"))


def _raw_requests_tiny_figure(raw: str) -> bool:
    return any(
        marker in str(raw or "")
        for marker in (
            "tiny figure",
            "tiny human",
            "tiny silhouette",
            "small figure",
            "distant figure",
            "figure for scale",
            "人物极小",
            "小小的人影",
            "远处人影",
            "用人物衬托",
            "衬托宏大",
        )
    )


def _raw_requests_shoes_removed(raw: str) -> bool:
    return any(
        marker in raw
        for marker in (
            "shoes removed",
            "shoes off",
            "both feet out of shoes",
            "out of shoes",
            "pair of sandals placed",
            "sandals placed on the floor",
            "remove shoes",
            "takes off shoes",
            "脱鞋",
            "把鞋脱",
        )
    )


def _raw_requests_barefoot(raw: str) -> bool:
    return any(marker in raw for marker in ("barefoot", "bare feet", "bare toes", "without shoes", "no shoes", "赤脚", "光脚", "裸足", "没穿鞋", "不穿鞋"))


def _shoe_removed_scene_tag_conflict(tag: str) -> bool:
    value = str(tag or "").strip().lower()
    if not value:
        return False
    return any(
        marker in value
        for marker in (
            "standing",
            "standing in room",
            "full body",
            "head to toe",
            "clear normal face",
            "full body action",
            "dynamic pose",
            "visible elegant footwear",
            "shoes worn",
            "wearing shoes",
            "wearing sandals",
            "well-drawn eyes",
            "clear floor",
            "background supports the character",
        )
    )


def _blindfold_scene_tag_conflict(tag: str) -> bool:
    value = str(tag or "").strip().lower()
    if not value:
        return False
    return any(
        marker in value
        for marker in (
            "clear normal face",
            "well-drawn eyes",
            "clear eyes",
            "expressive eyes",
            "looking at viewer",
        )
    )


def _hosiery_positive_parts(raw: str) -> list[str]:
    wants_black = any(marker in raw for marker in ("black stockings", "black pantyhose", "black stirrup pantyhose", "black hosiery", "黑丝", "黑色丝袜", "黑色连裤袜"))
    wants_white = any(marker in raw for marker in ("white stockings", "white pantyhose", "white stirrup pantyhose", "white hosiery", "白丝", "白色丝袜", "白色连裤袜"))
    wants_full_foot = any(marker in raw for marker in ("full-foot", "full foot", "covered feet", "全包", "包脚"))
    wants_stirrup = _raw_requests_stirrup(raw)
    shoes_removed = _raw_requests_shoes_removed(raw)

    color = "black" if wants_black and not wants_white else "white"
    coverage = "full-foot" if wants_full_foot and not wants_stirrup else "stirrup"
    hosiery = f"{color} {coverage} pantyhose"
    if coverage == "stirrup":
        hosiery = f"{color} stirrup pantyhose, open heel/toe stirrup design"
    elif coverage == "full-foot":
        hosiery = f"{color} full-foot pantyhose, feet fully covered"

    parts = [
        hosiery,
        f"same {color} pantyhose remains unchanged",
        "not cotton socks",
    ]
    if coverage == "stirrup":
        parts.extend(
            [
                f"2.0::{color} stirrup pantyhose strap under foot arch::",
                "open toes and open heels visible",
                "not bare legs",
            ]
        )
    if shoes_removed:
        parts.extend(
            [
                "2.4::both feet are completely out of shoes::",
                "2.4::one matching pair of empty low-heel sandals beside her feet::",
                "2.3::exactly two sandals total::",
            ]
        )
    else:
        parts.extend(
            [
                "elegant low-heel sandals worn over the same pantyhose",
            ]
        )
    return parts


def _hosiery_negative_parts(raw: str) -> list[str]:
    negatives: list[str] = []
    wants_black = any(marker in raw for marker in ("black stockings", "black pantyhose", "black stirrup pantyhose", "black hosiery", "黑丝", "黑色丝袜", "黑色连裤袜"))
    wants_white = any(marker in raw for marker in ("white stockings", "white pantyhose", "white stirrup pantyhose", "white hosiery", "白丝", "白色丝袜", "白色连裤袜", "踩脚白"))
    wants_full_foot = any(marker in raw for marker in ("full-foot", "full foot", "covered feet", "全包", "包脚"))
    wants_stirrup = _raw_requests_stirrup(raw)
    if wants_white and not wants_black:
        negatives.extend(["black stockings", "black pantyhose", "black hosiery"])
    if wants_black and not wants_white:
        negatives.extend(["white stockings", "white pantyhose", "white hosiery"])
    if wants_stirrup and not wants_full_foot:
        negatives.extend(["full-foot pantyhose", "fully covered feet", "covered toes", "ankle socks", "stockings ending at ankle", "footless tights ending at ankle", "leggings ending at ankle", "white ankle cuff", "ankle cuff", "ankle band only", "bare feet with ankle cuffs", "bare foot without stirrup strap", "bare legs", "naked legs", "no legwear"])
    if wants_full_foot and not wants_stirrup:
        negatives.extend(["stirrup pantyhose", "open heel stockings", "open toe stockings"])
    if _raw_requests_shoes_removed(raw):
        shoe_state_negatives = ["different stockings after shoes removed", "shoe still worn on one foot", "wearing sandals", "one shoe on foot", "shoes on feet", "sandals on feet", "feet inside shoes", "toes inside sandals", "feet resting on sandals", "sandals directly under feet", "visible shoes", "visible sandals", "footwear in frame", "extra pair of shoes", "duplicate shoes", "multiple pairs of shoes", "two pairs of sandals", "second pair of sandals", "second pair of shoes", "extra sandals at edge of frame", "shoe in foreground and shoe in background", "three shoes", "four shoes", "shoe pile", "plain white background", "blank background", "isolated character"]
        if wants_stirrup:
            negatives.extend(["bare feet without pantyhose", "no hosiery", *shoe_state_negatives, "standing", "standing pose", "full standing body", "full body portrait", "face close-up", "head close-up", "high heels", "stiletto heels", "pump shoes"])
        elif wants_full_foot or wants_white or wants_black:
            negatives.extend(["bare feet", "bare toes", *shoe_state_negatives, "standing", "standing pose", "full standing body", "full body portrait", "face close-up", "head close-up", "high heels", "stiletto heels", "pump shoes"])
        else:
            negatives.extend(shoe_state_negatives)
    return negatives


def _compact_footwear_extra_tag_should_skip(tag: str) -> bool:
    value = str(tag or "").strip().lower()
    if not value:
        return True
    return any(
        marker in value
        for marker in (
            "stirrup pantyhose",
            "white stirrup",
            "pantyhose unchanged",
            "open toe",
            "open heel",
            "open toes",
            "open heels",
            "strap under foot",
            "feet out of shoes",
            "shoes removed",
            "footwear",
            "sandal",
            "sandals",
            "portrait composition",
            "people-first",
            "visible room background",
            "warm lamp",
            "indoor seat",
            "third-person",
            "third_person",
            "standing",
            "standing pose",
            "full body",
            "head to toe",
            "full-body",
            "full standing body",
            "exactly two shoes",
            "sfw",
            "dongtian",
            "veil",
            "blindfold",
            "collar",
            "bracelet",
            "coat draped",
            "dance",
            "clear room background",
            "visible room background",
        )
    )


def _visual_control_extra_tag_should_skip(tag: str) -> bool:
    value = str(tag or "").strip().lower()
    if not value:
        return True
    return any(
        marker in value
        for marker in (
            "veil",
            "face veil",
            "bridal veil",
            "面纱",
            "头纱",
            "blindfold",
            "eye mask",
            "眼罩",
            "蒙眼",
            "collar",
            "choker",
            "项圈",
            "颈圈",
            "bracelet",
            "wristband",
            "手环",
            "手镯",
            "anklet",
            "ankle bracelet",
            "脚链",
            "脚环",
            "coat draped",
            "jacket draped",
            "coat over",
            "jacket over",
            "外套披",
            "披外套",
            "披在肩上",
            "dance",
            "dancing",
            "skirt hem",
            "跳舞",
            "舞蹈",
            "舞步",
            "裙摆",
            "white stirrup pantyhose",
            "black stirrup pantyhose",
            "stirrup stockings",
            "踩脚",
            "白丝",
            "黑丝",
            "丝袜",
            "连裤袜",
        )
    )


def _tail_diagnostic_extra_tag_should_skip(tag: str) -> bool:
    return "red cube" in str(tag or "").strip().lower()


def _tail_diagnostic_parts(extra_tags: list[str] | None) -> list[str]:
    raw = " ".join(str(tag or "") for tag in list(extra_tags or [])).lower()
    if "red cube" not in raw:
        return []
    return [
        "not a pedestal",
        "2.2::small bright red cube floor prop beside Xiya's left foot::",
        "2.0::red cube clearly visible on floor::",
    ]


def _no_character_extra_tag_should_skip(tag: str) -> bool:
    raw = str(tag or "").strip().lower()
    if not raw:
        return True
    return any(
        marker in raw
        for marker in (
            "person",
            "people",
            "human",
            "character",
            "portrait",
            "face",
            "selfie",
            "1girl",
            "1boy",
            "male",
            "female",
            "xiya",
            "owner",
            "shared scene",
            "third-person",
            "third_person",
        )
    )


def _subject_focus_tags(case_id: str, case: dict[str, Any], extra_tags: list[str] | None) -> list[str]:
    raw = " ".join([case_id, *[str(tag or "") for tag in list(case.get("tags") or [])], *[str(tag or "") for tag in list(extra_tags or [])]]).lower()
    if bool(case.get("allow_no_character")):
        if case_id == "food_closeup":
            return ["object-focused composition", "food is the main subject", "no character in frame"]
        tags = ["environment-focused composition", "scenery is the main subject", "no character in frame"]
        if any(marker in raw for marker in ("window", "窗外", "窗框", "窗边")):
            tags.extend(
                [
                    "view through a window",
                    "dark window frame visible",
                    "window frame borders the scenery",
                    "interior window edge framing the outside view",
                ]
            )
        return tags
    if "selfie" in raw or "phone photo" in raw:
        tags = [
            "face-focused selfie composition",
            "clear selfie perspective",
            "phone camera framing",
            "Xiya close to camera",
            "Xiya's face remains visible when showing props",
            "prop visible near Xiya if requested",
            "cute expressive face",
            "cute hand gesture if natural",
        ]
        if _raw_requests_food(raw):
            tags.extend(
                [
                    "mirror selfie with food",
                    "one hand holding phone",
                    "other hand holding food",
                    "apple pie slice near mouth if requested",
                    "bitten food slice if eating is requested",
                    "phone and food are separate objects",
                    "small plate of food visible",
                ]
            )
        return tags
    if _raw_requests_food(raw):
        if case_id == "meal_table":
            return [
                "people-first meal composition",
                "Xiya is the main subject",
                "visible table surface in the foreground",
                "plate on the table",
                "apple pie slice on a plate if apple pie is requested",
                "fork or small spoon visible",
                "food and plate are visible near Xiya",
                "eating a bite pose if eating is requested",
                "food near mouth if eating is requested",
                "clear face",
                "natural hands",
                "warm indoor room background",
                "background supports the meal scene",
            ]
        return [
            "people-first composition",
            "Xiya is the main subject",
            "food is a visible prop in the scene",
            "food and plate are visible near Xiya",
            "eating a bite pose if eating is requested",
            "food near mouth if eating is requested",
            "clear face",
            "natural hands",
            "background supports the character",
        ]
    if _raw_requests_hosiery(raw) or _raw_requests_shoes_removed(raw):
        composition = "single Xiya knees-to-feet seated detail composition" if _raw_requests_shoes_removed(raw) else "single Xiya full-body composition"
        tags = [
            composition,
            "Xiya is the only character",
            "legs and elegant footwear visible",
            "clear room background",
        ]
        if "rain outside window" in raw or "rainy window" in raw:
            tags.append("2.0::rainy window background behind Xiya::")
        if "cozy fantasy room" in raw or "warm lamp" in raw:
            tags.append("2.0::cozy fantasy room with warm lamp::")
        if _raw_requests_shoes_removed(raw):
            tags.extend(
                [
                    "lower-body footwear detail focus",
                    "knees-to-feet crop",
                    "face and head out of frame",
                    "2.4::seated on low cushion knees bent feet forward::",
                    "2.2::cozy fantasy room background with wood floor window curtain warm lamp::",
                ]
            )
        if _raw_requests_stirrup(raw):
            tags.append("stirrup pantyhose straps and open toes visible")
        return tags
    if "mirror" in raw:
        return ["clear mirror selfie composition", "visible mirror reflection", "Xiya is main subject", "cute pose"]
    if case_id == "story_scene":
        tags = [
            "story-scene composition",
            "Xiya remains the visible main character",
            "Xiya is acting as the story heroine",
            "Xiya identity remains visible through face, cat ears, cat tail, and purple eyes",
            "role costume matches the story",
            "key story prop visible",
            "character action and key object are both clear",
            "background supports the story",
        ]
        if "star bridge" in raw:
            tags.extend(["luminous star bridge visible underfoot", "bridge across the night sky"])
        if "talking star" in raw or ("会说话" in raw and "星" in raw):
            tags.extend(
                [
                    "2.0::glowing golden talking star orb visible::",
                    "2.0::small luminous star in the girl's hands::",
                    "1.6::character holding a glowing star orb::",
                    "expressive magical star with tiny face",
                    "the star is the key story prop",
                ]
            )
        return tags
    if case_id == "roleplay_scene":
        return [
            "roleplay scene composition",
            "Xiya remains the visible main character",
            "Xiya is cosplaying and embodying the requested role",
            "Xiya identity remains visible through face, cat ears, cat tail, and purple eyes",
            "role costume matches the roleplay setting",
            "interactive staging between the roleplay characters",
            "clear action relationship",
            "background supports the roleplay scene",
            "not a status photo",
        ]
    if any(word in raw for word in ("dance", "dancing", "跳舞", "舞蹈")):
        return [
            "solo Xiya dance performance",
            "Xiya is the main subject",
            "full body action pose",
            "head to toe visible",
            "both legs visible",
            "feet visible",
            "clear normal face",
            "well-drawn eyes",
            "dynamic dancing pose",
            "arms extended gracefully",
            "graceful step",
            "visible room background",
            "clear floor",
            "background supports the action",
        ]
    if any(word in raw for word in ("hugging", "embrace", "靠肩", "shoulder", "双人舞", "1boy", "owner projection", "adult male owner", "two-person")):
        tags = [
            "people-first composition",
            "Xiya and owner are both main subjects",
            "two-person interaction focus",
            "clear action relationship",
            "background supports the characters",
        ]
        if "lean" in raw or "shoulder" in raw or "靠" in raw:
            tags.extend(
                [
                    "2.0::Xiya leaning her head against owner's shoulder::",
                    "2.0::shoulders touching::",
                    "close shoulder contact visible",
                ]
            )
        if "tram" in raw or "train" in raw:
            tags.extend(
                [
                    "both characters seated together on the tram bench",
                    "owner seated beside Xiya on the same bench",
                    "sitting shoulder to shoulder",
                    "no empty seat gap between them",
                    "close two-person crop",
                    "no standing passenger focus",
                    "no extra passengers",
                    "exactly one girl and one man",
                ]
            )
        if "coat" in raw or "jacket" in raw:
            tags.extend(
                [
                    "dark jacket visibly draped over Xiya's shoulders",
                    "coat wrapped around Xiya's shoulders like a shawl",
                    "black jacket over her light blue hoodie",
                    "jacket sleeves hanging down in front of Xiya",
                    "owner wearing dark shirt and trousers",
                    "owner in plain black shirt and trousers",
                ]
            )
        return tags
    return [
        "people-first composition",
        "Xiya is the main subject",
        "clear face",
        "expressive pose",
        "background supports the character",
    ]


def _aspect_for_focus(
    case_id: str,
    case: dict[str, Any],
    *,
    extra_tags: list[str] | None,
    base_aspect: str,
) -> str:
    aspect = str(base_aspect or "portrait").strip().lower()
    if bool(case.get("allow_no_character")):
        return aspect
    raw = " ".join(
        [
            case_id,
            *[str(tag or "") for tag in list(case.get("tags") or [])],
            *[str(tag or "") for tag in list(extra_tags or [])],
        ]
    ).lower()
    people_focus_markers = (
        "selfie",
        "mirror selfie",
        "hugging",
        "embrace",
        "shoulder",
        "leaning",
        "holding hands",
        "couple dance",
        "two-person",
        "1boy",
        "owner projection",
        "adult male owner",
        "fully clothed man",
        "dance",
        "dancing",
        "full body action",
        "performing",
        "kneeling",
        "eating",
        "food near mouth",
        "holding food",
        "portrait composition",
        "blue cat girl",
        "talking star",
        "glowing star",
        "star orb",
    )
    if aspect == "landscape" and any(marker in raw for marker in people_focus_markers):
        return "portrait"
    return aspect


def _raw_requests_food(raw: str) -> bool:
    return any(word in str(raw or "") for word in ("food", "apple pie", "meal", "eating", "pie", "plate"))


def _extra_tags_request_male_owner(extra_tags: list[str] | None) -> bool:
    text = " ".join(str(tag or "").strip().lower() for tag in list(extra_tags or []))
    if not text:
        return False
    return any(
        marker in text
        for marker in (
            "1boy",
            "owner projection",
            "adult male owner",
            "adult man",
            "fully clothed man",
            "tall strong adult male",
            "black-haired man",
        )
    )


def _case_negative_sfw(value: str, *, allow_male: bool = False) -> str:
    if not allow_male:
        return str(value or "")
    blocked = {"1boy", "male", "male focus", "hetero"}
    kept: list[str] = []
    for raw_tag in str(value or "").replace("\n", ",").split(","):
        tag = raw_tag.strip()
        if not tag:
            continue
        if _strip_nai_weight(tag).lower() in blocked:
            continue
        kept.append(tag)
    return ", ".join(kept)


def _strip_nai_weight(tag: str) -> str:
    value = str(tag or "").strip()
    while "::" in value:
        prefix, rest = value.split("::", 1)
        try:
            float(prefix.strip())
        except ValueError:
            break
        value = rest.strip()
    while value.endswith("::"):
        value = value[:-2].strip()
    return value


def _join_tags(parts: list[str], *, mode: str = "positive") -> str:
    seen: set[str] = set()
    out: list[str] = []
    banned_positive = {
        "nsfw",
        "uncensored",
        "nude",
        "explicit",
        "sex",
        "nipples",
        "pussy",
        "penis",
        "medium breasts",
        "large breasts",
        "cleavage",
        "lingerie",
        "underwear",
        *([] if mode == "sfw_positive_beach" else ["swimsuit"]),
        "bikini",
        "see-through clothes",
    } if mode in {"sfw_positive", "sfw_positive_beach"} else set()
    for part in parts:
        for raw_tag in _split_nai_tags(str(part or "").replace("\n", ",")):
            tag = raw_tag.strip()
            if not tag:
                continue
            key = tag.lower()
            if key in banned_positive:
                continue
            if key in seen:
                continue
            seen.add(key)
            out.append(tag)
    return ", ".join(out)
