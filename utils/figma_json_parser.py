import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent

FIGMA_EXPORT_FILE = PROJECT_ROOT / "figma" / "figma_export.json"
COMPONENT_MAP_FILE = PROJECT_ROOT / "data" / "figma_component_map.json"
EXPECTED_OUTPUT_FILE = PROJECT_ROOT / "expected" / "upload_modal.json"

EXPECTED_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def figma_color_to_rgb(fill: dict | None) -> str | None:
    if not fill:
        return None

    color = fill.get("color")

    if isinstance(color, str):
        return color

    if not isinstance(color, dict):
        return None

    red = round(color.get("r", 0) * 255)
    green = round(color.get("g", 0) * 255)
    blue = round(color.get("b", 0) * 255)
    alpha = fill.get("opacity", 1)

    if alpha < 1:
        return f"rgba({red}, {green}, {blue}, {alpha})"

    return f"rgb({red}, {green}, {blue})"


def first_visible_fill(node: dict) -> str | None:
    for fill in node.get("fills", []):
        if fill.get("visible", True):
            result = figma_color_to_rgb(fill)
            if result:
                return result

    return None


def first_stroke(node: dict) -> str | None:
    strokes = node.get("strokes", [])

    if not strokes:
        return None

    return figma_color_to_rgb(strokes[0])


def font_weight_from_style(style: str | None) -> str | None:
    if not style:
        return None

    normalized = style.lower()

    weights = {
        "thin": "100",
        "extra light": "200",
        "extralight": "200",
        "light": "300",
        "regular": "400",
        "normal": "400",
        "medium": "500",
        "semi bold": "600",
        "semibold": "600",
        "bold": "700",
        "extra bold": "800",
        "extrabold": "800",
        "black": "900"
    }

    return weights.get(normalized)


def format_px(value: Any) -> str | None:
    if value is None:
        return None

    number = float(value)

    if number.is_integer():
        return f"{int(number)}px"

    return f"{number}px"


def flatten_nodes(
    nodes: list[dict],
    parent: dict | None = None,
    absolute_parent_x: float = 0,
    absolute_parent_y: float = 0
) -> list[dict]:
    flattened = []

    for node in nodes:
        local_x = node.get("x", 0)
        local_y = node.get("y", 0)

        if parent is None:
            absolute_x = local_x
            absolute_y = local_y
        else:
            absolute_x = absolute_parent_x + local_x
            absolute_y = absolute_parent_y + local_y

        flattened_node = {
            "node": node,
            "parent": parent,
            "absolute_x": absolute_x,
            "absolute_y": absolute_y
        }

        flattened.append(flattened_node)

        children = node.get("children", [])

        if children:
            flattened.extend(
                flatten_nodes(
                    children,
                    parent=node,
                    absolute_parent_x=absolute_x,
                    absolute_parent_y=absolute_y
                )
            )

    return flattened


def matches(node: dict, rules: dict) -> bool:
    for key, expected_value in rules.items():
        if node.get(key) != expected_value:
            return False

    return True


def find_node(flattened: list[dict], rules: dict) -> dict | None:
    for item in flattened:
        if matches(item["node"], rules):
            return item

    return None


def get_frame_node(item: dict) -> dict:
    node = item["node"]
    parent = item.get("parent")

    if node.get("type") == "TEXT" and parent and parent.get("type") == "FRAME":
        return parent

    return node


def extract_component(item: dict) -> dict:
    node = item["node"]
    frame_node = get_frame_node(item)

    font_name = node.get("fontName", {})

    result = {
        "text": node.get("characters"),
        "visible": True,
        "width": frame_node.get("width", node.get("width")),
        "height": frame_node.get("height", node.get("height")),
        "x": item.get("absolute_x"),
        "y": item.get("absolute_y"),
        "fontFamily": font_name.get("family"),
        "fontSize": format_px(node.get("fontSize")),
        "fontWeight": font_weight_from_style(font_name.get("style")),
        "color": first_visible_fill(node),
        "backgroundColor": first_visible_fill(frame_node),
        "borderColor": first_stroke(frame_node),
        "borderRadius": format_px(frame_node.get("cornerRadius")),
        "paddingTop": format_px(frame_node.get("paddingTop")),
        "paddingRight": format_px(frame_node.get("paddingRight")),
        "paddingBottom": format_px(frame_node.get("paddingBottom")),
        "paddingLeft": format_px(frame_node.get("paddingLeft"))
    }

    return {
        key: value
        for key, value in result.items()
        if value is not None
    }


def generate_expected_rules() -> Path:
    figma_data = load_json(FIGMA_EXPORT_FILE)
    mapping = load_json(COMPONENT_MAP_FILE)

    root_nodes = figma_data if isinstance(figma_data, list) else [figma_data]
    flattened = flatten_nodes(root_nodes)

    expected_rules = {}
    missing_components = []

    for component_name, config in mapping.items():
        item = find_node(flattened, config["match"])

        if item is None:
            missing_components.append(component_name)
            continue

        expected_rules[component_name] = extract_component(item)

    with EXPECTED_OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(expected_rules, file, indent=4)

    print(f"Expected Figma rules saved: {EXPECTED_OUTPUT_FILE}")

    if missing_components:
        print("Figma mappings not found:")
        for component_name in missing_components:
            print(f"  - {component_name}")

    return EXPECTED_OUTPUT_FILE