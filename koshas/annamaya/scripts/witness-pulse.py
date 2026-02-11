import os
import re

VAULT_ROOT = os.getcwd()
DRIFT_PATTERNS = {
    r"WitnessOS": "Tryambakam Noesis",
    r"Witness OS": "Tryambakam Noesis",
}

def audit_drift():
    print("🎭 PHASE 1: WITNESS AUDIT (Aletheios)")
    print("-" * 40)
    
    drift_found = []
    
    # Check for root level entropy
    root_files = [f for f in os.listdir(VAULT_ROOT) if os.path.isfile(os.path.join(VAULT_ROOT, f))]
    if root_files:
        print(f"⚠️  ENTROPY DETECTED: {len(root_files)} files in vault root.")
        for f in root_files[:5]:
            print(f"   - {f}")
        if len(root_files) > 5:
            print(f"   ... and {len(root_files)-5} more.")
    
    # Check for naming drift in text files
    print("\n🔍 SCANNING FOR NAMING DRIFT...")
    for root, dirs, files in os.walk(VAULT_ROOT):
        if "_System" in root or "node_modules" in root or ".git" in root:
            continue
            
        for file in files:
            if file.endswith((".md", ".txt", ".json", ".yaml")):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for pattern, replacement in DRIFT_PATTERNS.items():
                            if re.search(pattern, content, re.IGNORECASE):
                                print(f"📍 DRIFT: '{pattern}' found in {os.path.relpath(path, VAULT_ROOT)}")
                                drift_found.append(path)
                except Exception:
                    pass
                    
    print("-" * 40)
    return drift_found

if __name__ == "__main__":
    audit_drift()
