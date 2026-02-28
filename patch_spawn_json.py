import os
import json

# Configuration
TEXTURE_DIR = "assets/bookofdragons/textures/entity/dragons/nightfury"
SPAWN_JSON_PATH = "config/incontrol/spawn.json" # Adjust to your actual path

def calculate_weights():
    # 1. Count the variants
    files = [f for f in os.listdir(TEXTURE_DIR) if f.endswith('.png')]
    # Extract numbers from nightfury_#.png
    variant_ids = []
    for f in files:
        try:
            num = int(f.split('_')[1].split('.')[0])
            variant_ids.append(num)
        except:
            continue
    
    variant_ids.sort()
    total_variants = len(variant_ids)
    
    # 2. Perform the math
    new_spawn_entries = []
    
    # Common pool (0-3)
    common_ids = [i for i in variant_ids if i <= 3]
    # Rare pool (4+)
    rare_ids = [i for i in variant_ids if i > 3]
    
    # Weight calculation
    common_weight = 10.0 # Fixed 10% each
    rare_total_pool = 60.0
    rare_weight = rare_total_pool / len(rare_ids) if rare_ids else 0
    
    # 3. Build the JSON objects
    for v_id in variant_ids:
        weight = common_weight if v_id <= 3 else rare_weight
        
        entry = {
            "mob": "dragon_mod:nightfury",
            "result": "allow",
            "onjoin": True,
            "nbt": {
                "Variant": v_id
            },
            "weight": round(weight, 2)
        }
        new_spawn_entries.append(entry)
        
    # 4. Write to file
    with open(SPAWN_JSON_PATH, 'w') as f:
        json.dump(new_spawn_entries, f, indent=2)
    
    print(f"Successfully patched {total_variants} variants.")
    print(f"Common: {len(common_ids)} | Rare: {len(rare_ids)} (Weight: {round(rare_weight, 2)} each)")

if __name__ == "__main__":
    calculate_weights()
