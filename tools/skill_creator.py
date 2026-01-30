"""
Nexus Tool: Skill Creator
=========================
Usage: python tools/skill_creator.py [--instincts]

Analyzes git history to generate a SKILL.md describing project patterns.
"""

import os
import subprocess
import argparse
import re
from collections import Counter

def run_git(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError:
        return ""

def analyze_repo():
    print("Nexus: Analyzing Neural Pathways (Git History)...")
    
    # 1. Commit Conventions
    raw_commits = run_git('git log --oneline -n 200 | cut -d" " -f2-')
    conventions = Counter()
    for line in raw_commits.split('\n'):
        match = re.match(r'^([a-z]+)(\(.*\))?:', line)
        if match:
            conventions[match.group(1)] += 1
            
    # 2. File Architecture (Top Directories)
    # Simple heuristic: list top level dirs
    architecture = []
    for item in os.listdir("."):
        if os.path.isdir(item) and not item.startswith("."):
            architecture.append(item)
            
    return {
        "conventions": conventions,
        "architecture": architecture,
        "commit_count": len(raw_commits.split('\n'))
    }

def generate_skill(data, output_file="skills/generated_project_patterns.md"):
    content = f"""---
name: project-patterns
description: Auto-generated patterns from git history
source: skill-creator
---

# Project Patterns

## Commit Conventions
Detected types in last {data['commit_count']} commits:
"""
    for conv, count in data['conventions'].most_common(5):
        content += f"- **{conv}**: {count} uses\n"
        
    content += "\n## Architecture\nTop-level structure:\n"
    for folder in data['architecture']:
        content += f"- `{folder}/`\n"
        
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"[OK] Skill generated: {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instincts", action="store_true", help="Generate instincts")
    args = parser.parse_args()
    
    data = analyze_repo()
    generate_skill(data)
    
    if args.instincts:
        # Generate a dummy instinct based on conventions
        print("Nexus: Generating Instincts...")
        import yaml
        instinct = {
            "id": "git-convention",
            "trigger": "when writing commit message",
            "confidence": 0.9,
            "domain": "git",
            "response": f"Use one of: {', '.join(data['conventions'].keys())}"
        }
        os.makedirs("skills/instincts", exist_ok=True)
        with open("skills/instincts/git-convention.yaml", "w") as f:
            yaml.dump(instinct, f)
        print("[OK] Instinct generated: skills/instincts/git-convention.yaml")

if __name__ == "__main__":
    main()
