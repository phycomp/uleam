"""Skill Viewer：列出技能來源、Usage、作者、備註；支援指定上層級列出下層級。"""

import os, sys, argparse

SKILL_DIRS = [
    "/home/sam/代理人/.agents/skills",
    "/home/sam/.opencode/skills",
    "/home/sam/.agents/skills",
]

# 層級架構：上層級 → 下層級
HIERARCHY = {
    "generic-qcable": [
        "quantum-cryogenic-cable",
        "mantaro",
        "polar",
        "component-integration",
        "connector",
        "crosstalk-calc",
        "three-view",
        "material-db",
        "thermal-load-measurement",
        "thermal-load-simulation",
        "thermal-load-units",
        "thermal-load-sop",
        "electrical-spec",
        "electrical-test-sop",
        "llm-parser",
        "measurement-unit-link",
    ],
    "quantum-cryogenic-cable": [
        "mantaro",
        "polar",
        "nbtii-small-batch",
        "component-integration",
    ],
    "component-integration": ["connector"],
    "nbtii-small-batch": ["nbtii-pcb-fab", "nbtii-test-sop"],
    "nbtii-pcb-fab": ["nbtii-medium-batch"],
    "nbtii-medium-batch": ["nbtii-r2r-mass"],
    "thermal-load-measurement": ["thermal-load-simulation", "thermal-load-sop"],
    "thermal-load-simulation": ["thermal-load-units"],
    "engineering-delivery": [
        "kpi-delivery-valid",
        "cloud-deploy",
        "skill-generator",
        "refactor",
    ],
    "kpi-delivery-valid": ["llm-parser", "measurement-unit-link"],
    "qcable-index": [
        "generic-qcable",
        "quantum-cryogenic-cable",
        "thermal-load-measurement",
        "thermal-load-simulation",
        "thermal-load-units",
        "thermal-load-sop",
        "component-integration",
        "connector",
        "crosstalk-calc",
        "electrical-spec",
        "electrical-test-sop",
        "nbtii-small-batch",
        "nbtii-pcb-fab",
        "nbtii-medium-batch",
        "nbtii-r2r-mass",
        "nbtii-test-sop",
        "mantaro",
        "polar",
        "llm-parser",
        "measurement-unit-link",
        "skill-generator",
        "refactor",
        "cloud-deploy",
        "material-db",
        "three-view",
        "oloid-3d-product",
        "txt-proc",
        "txt-genoffice",
        "engineering-delivery",
        "kpi-delivery-valid",
    ],
}


def parse_frontmatter(path):
    info = {
        "name": os.path.basename(os.path.dirname(path)),
        "desc": "",
        "author": "",
        "version": "",
        "usage": "",
        "notes": "",
    }
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return info
    if not content.startswith("---"):
        return info
    parts = content.split("---", 2)
    if len(parts) < 3:
        return info
    fm = parts[1]
    for line in fm.splitlines():
        line = line.strip()
        if line.startswith("name:"):
            info["name"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("description:"):
            info["desc"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("author:"):
            info["author"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("version:"):
            info["version"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("allowed-tools:"):
            info["usage"] = line.split(":", 1)[1].strip()
    body = parts[2].strip()
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            info["notes"] = line[:80]
            break
    return info


def load_skills():
    all_skills = []
    seen = set()
    for base in SKILL_DIRS:
        if not os.path.isdir(base):
            continue
        for d in sorted(os.listdir(base)):
            p = os.path.join(base, d, "SKILL.md")
            if os.path.isfile(p):
                info = parse_frontmatter(p)
                key = info["name"]
                if key in seen:
                    continue
                seen.add(key)
                info["source"] = base
                all_skills.append(info)
    return all_skills


def print_skill(info):
    print(f"\n[{info['name']}]")
    print(f"  來源: {info['source']}")
    print(f"  Usage: {info['desc'][:100]}")
    print(f"  作者: {info['author'] or '(未指定)'}")
    print(f"  版本: {info['version'] or '(未指定)'}")
    print(f"  工具: {info['usage'] or '(未指定)'}")
    print(f"  備註: {info['notes'] or '(無)'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parent", help="指定上層級技能名稱，列出其下層級")
    ap.add_argument("--tree", action="store_true", help="印出完整層級樹")
    ap.add_argument("--json", action="store_true", help="以 JSON 格式輸出")
    args = ap.parse_args()

    skills = load_skills()
    skill_map = {s["name"]: s for s in skills}

    if args.parent:
        children = HIERARCHY.get(args.parent, [])
        if args.json:
            import json

            out = {"parent": args.parent, "children": []}
            for c in children:
                if c in skill_map:
                    info = dict(skill_map[c])
                    info["installed"] = True
                    out["children"].append(info)
                else:
                    out["children"].append({"name": c, "installed": False})
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return
        print(f"上層級: {args.parent}")
        print(f"下層級 ({len(children)}):")
        for c in children:
            if c in skill_map:
                print_skill(skill_map[c])
            else:
                print(f"\n[{c}] (未安裝)")
        return

    if args.tree:

        def print_tree(node, prefix="", visited=None):
            if visited is None:
                visited = set()
            if node in visited:
                print(f"{prefix}{node} (循環)")
                return
            visited = visited | {node}
            print(f"{prefix}{node}")
            for c in HIERARCHY.get(node, []):
                print_tree(c, prefix + "  ", visited)

        for root in ["qcable-index", "engineering-delivery", "generic-qcable"]:
            print_tree(root)
            print()
        return

    print(f"Total unique skills: {len(skills)}")
    print("=" * 100)
    for info in sorted(skills, key=lambda x: x["name"]):
        print_skill(info)


if __name__ == "__main__":
    main()
