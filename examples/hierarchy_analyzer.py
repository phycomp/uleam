"""Hierarchy Analyzer：分析技能上下層級與 repo 代碼依賴。"""

import os, sys, re, argparse, json

sys.path.insert(0, "/home/sam/代理人")
from examples.skill_viewer import HIERARCHY, load_skills


def analyze_skills():
    skills = load_skills()
    smap = {s["name"]: s for s in skills}
    tree_lines = []

    def render(node, prefix="", visited=None):
        if visited is None:
            visited = set()
        if node in visited:
            tree_lines.append(f"{prefix}{node} (循環)")
            return
        visited = visited | {node}
        tree_lines.append(f"{prefix}{node}")
        for c in HIERARCHY.get(node, []):
            render(c, prefix + "  ", visited)

    for root in ["qcable-index", "engineering-delivery", "generic-qcable"]:
        render(root)
        tree_lines.append("")
    return "\n".join(tree_lines)


def analyze_repo(repo_path):
    # build import graph
    imports = {}
    for root, _, files in os.walk(repo_path):
        if any(x in root for x in [".git", "__pycache__", "node_modules", ".venv"]):
            continue
        for f in files:
            if not f.endswith(".py"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, repo_path)
            mod = rel.replace(os.sep, ".").replace(".py", "")
            try:
                with open(path, encoding="utf-8") as fh:
                    src = fh.read()
            except Exception:
                continue
            # find imports
            deps = set()
            for m in re.finditer(r"^(?:from|import)\s+([\w\.]+)", src, re.M):
                dep = m.group(1).split(".")[0]
                if dep and dep != mod.split(".")[0]:
                    deps.add(dep)
            imports[mod] = sorted(deps)
    return imports


def to_mermaid_skill():
    lines = ["graph TD"]
    for parent, children in HIERARCHY.items():
        for c in children:
            lines.append(f"  {parent} --> {c}")
    return "\n".join(lines)


def to_mermaid_repo(imports):
    lines = ["graph TD"]
    for mod, deps in imports.items():
        for d in deps:
            lines.append(f"  {mod} --> {d}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="/home/sam/代理人", help="repo path to analyze")
    ap.add_argument("--output", default=None, help="output file")
    ap.add_argument("--format", default="text", choices=["text", "mermaid", "json"])
    args = ap.parse_args()

    skill_tree = analyze_skills()
    repo_imports = analyze_repo(args.repo)

    if args.format == "text":
        out = (
            "=== Skill Hierarchy ===\n" + skill_tree + "\n\n=== Repo Import Graph ===\n"
        )
        for mod, deps in sorted(repo_imports.items()):
            if deps:
                out += f"{mod} -> {', '.join(deps)}\n"
    elif args.format == "mermaid":
        out = (
            "## Skill Hierarchy\n```mermaid\n"
            + to_mermaid_skill()
            + "\n```\n\n## Repo Import Graph\n```mermaid\n"
            + to_mermaid_repo(repo_imports)
            + "\n```"
        )
    elif args.format == "json":
        out = json.dumps(
            {"skills": HIERARCHY, "repo_imports": repo_imports},
            ensure_ascii=False,
            indent=2,
        )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Written to {args.output}")
    else:
        print(out[:3000])


if __name__ == "__main__":
    main()
