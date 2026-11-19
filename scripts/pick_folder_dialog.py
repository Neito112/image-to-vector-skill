import os
import subprocess
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output_config.json')
FALLBACK_WORKSPACE_CONFIG = r'd:\ComfyUI\svg\output_config.json'

def open_folder_dialog():
    ps_cmd = """
Add-Type -AssemblyName System.Windows.Forms
$form = New-Object System.Windows.Forms.Form
$form.TopMost = $true
$dialog = New-Object System.Windows.Forms.FolderBrowserDialog
$dialog.Description = 'Chon thu muc luu anh vector dau ra'
$dialog.ShowNewFolderButton = $true
$dialog.SelectedPath = 'd:\\ComfyUI\\svg'
$result = $dialog.ShowDialog($form)
if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    Write-Output $dialog.SelectedPath
}
$form.Dispose()
"""
    res = subprocess.run(['powershell', '-NoProfile', '-Command', ps_cmd], capture_output=True, text=True)
    selected_path = res.stdout.strip()
    if selected_path and os.path.exists(selected_path):
        payload = {'outputDir': selected_path}
        for p in [CONFIG_PATH, FALLBACK_WORKSPACE_CONFIG]:
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump(payload, f, indent=2)
            except Exception:
                pass
        print(f"[+] Successfully selected and saved output directory: {selected_path}")
        return selected_path
    else:
        print("[-] Selection cancelled or invalid.")
        return None

if __name__ == '__main__':
    open_folder_dialog()
