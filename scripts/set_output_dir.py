import os
import sys
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output_config.json')
FALLBACK_WORKSPACE_CONFIG = r'd:\ComfyUI\svg\output_config.json'

def get_output_dir():
    for p in [CONFIG_PATH, FALLBACK_WORKSPACE_CONFIG]:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('outputDir') and os.path.exists(data['outputDir']):
                        return data['outputDir']
            except Exception:
                pass
    return r'd:\ComfyUI\svg'

def set_output_dir(new_dir):
    new_dir = os.path.abspath(new_dir)
    os.makedirs(new_dir, exist_ok=True)
    payload = {'outputDir': new_dir}
    for p in [CONFIG_PATH, FALLBACK_WORKSPACE_CONFIG]:
        try:
            with open(p, 'w', encoding='utf-8') as f:
                json.dump(payload, f, indent=2)
        except Exception:
            pass
    print(f"[+] Successfully updated vector output directory to: {new_dir}")
    return new_dir

if __name__ == '__main__':
    if len(sys.argv) > 1:
        set_output_dir(sys.argv[1])
    else:
        print(f"Current output directory: {get_output_dir()}")
