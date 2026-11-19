const vscode = require('vscode');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

function activate(context) {
    let disposable = vscode.commands.registerCommand('imageToVector.openDropzone', function () {
        const panel = vscode.window.createWebviewPanel(
            'imageToVectorDropzone',
            'Image to Vector (Drag & Drop)',
            vscode.ViewColumn.Beside,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        panel.webview.html = getWebviewContent();

        panel.webview.onDidReceiveMessage(
            message => {
                if (message.command === 'vectorize') {
                    const filePath = message.filePath;
                    vscode.window.showInformationMessage('Đang vector hóa ảnh bằng Antigravity quota: ' + path.basename(filePath));
                    
                    // Script path in workspace or skill repo
                    const scriptPath = 'd:\\ComfyUI\\svg\\image-to-vector-skill-repo\\scripts\\auto_vectorizer.py';
                    const outputSvg = 'd:\\ComfyUI\\svg\\output_vector.svg';

                    const cmd = `python "${scriptPath}" "${filePath}" "${outputSvg}"`;
                    exec(cmd, (err, stdout, stderr) => {
                        if (err) {
                            vscode.window.showErrorMessage('Lỗi xử lý: ' + err.message);
                            return;
                        }
                        const svgData = fs.readFileSync(outputSvg, 'utf-8');
                        const previewPath = outputSvg.replace('.svg', '_preview.png');
                        const previewUri = panel.webview.asWebviewUri(vscode.Uri.file(previewPath)).toString();

                        panel.webview.postMessage({
                            command: 'rendered',
                            svg: svgData,
                            svgPath: outputSvg,
                            folderPath: path.dirname(outputSvg),
                            previewUri: previewUri
                        });
                        vscode.window.showInformationMessage('Vector hóa thành công! Đã tạo file SVG.');
                    });
                } else if (message.command === 'openExternalFile') {
                    exec(`Start-Process "${message.filePath}"`, { shell: 'powershell.exe' });
                } else if (message.command === 'openExternalFolder') {
                    exec(`explorer.exe "${message.folderPath}"`);
                }
            },
            undefined,
            context.subscriptions
        );
    });

    context.subscriptions.push(disposable);
}

function getWebviewContent() {
    return `<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        padding: 20px;
        background-color: var(--vscode-editor-background);
        color: var(--vscode-editor-foreground);
    }
    .header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    .dropzone {
        border: 2px dashed #3b82f6;
        border-radius: 16px;
        padding: 40px 20px;
        text-align: center;
        background: rgba(59, 130, 246, 0.05);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .dropzone:hover, .dropzone.dragover {
        background: rgba(59, 130, 246, 0.15);
        border-color: #2563eb;
    }
    .btn {
        background: #2563eb;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        margin: 5px;
    }
    .btn-secondary {
        background: #4b5563;
    }
    .btn:hover {
        opacity: 0.9;
    }
    .preview-box {
        margin-top: 25px;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid var(--vscode-widget-border);
        display: none;
    }
    .svg-container {
        background: #fff;
        padding: 10px;
        border-radius: 8px;
        margin: 15px 0;
        text-align: center;
    }
    .svg-container svg {
        max-width: 100%;
        height: auto;
    }
</style>
</head>
<body>
    <div class="header">
        <h2>🎯 Chuyển Đổi Ảnh Thành Vector (Antigravity Quota)</h2>
    </div>

    <div class="dropzone" id="dropArea">
        <p style="font-size: 28px; margin: 0 0 10px;">📥</p>
        <p style="font-size: 16px; font-weight: 600; margin: 0 0 8px;">Kéo & thả ảnh vào đây</p>
        <p style="font-size: 13px; opacity: 0.7; margin: 0 0 15px;">Hỗ trợ định dạng JPG, PNG, WEBP, BMP</p>
        <input type="file" id="fileInput" accept="image/*" style="display: none;" />
        <button class="btn" onclick="document.getElementById('fileInput').click()">Hoặc chọn file từ máy tính</button>
    </div>

    <div class="preview-box" id="previewBox">
        <h3>✨ Kết Quả Vector Hóa</h3>
        <div class="svg-container" id="svgContainer"></div>
        <div>
            <button class="btn" id="btnOpenFile">📄 Mở file SVG ngoài Windows</button>
            <button class="btn btn-secondary" id="btnOpenFolder">📂 Mở thư mục ngoài Windows</button>
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        const dropArea = document.getElementById('dropArea');
        const fileInput = document.getElementById('fileInput');
        const previewBox = document.getElementById('previewBox');
        const svgContainer = document.getElementById('svgContainer');
        let currentSvgPath = '';
        let currentFolderPath = '';

        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropArea.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropArea.classList.remove('dragover');
            }, false);
        });

        dropArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });

        function handleFile(file) {
            // Note: in VS Code Webview, file.path contains full local path
            const path = file.path || file.name;
            vscode.postMessage({
                command: 'vectorize',
                filePath: path
            });
        }

        window.addEventListener('message', event => {
            const message = event.data;
            if (message.command === 'rendered') {
                currentSvgPath = message.svgPath;
                currentFolderPath = message.folderPath;
                svgContainer.innerHTML = message.svg;
                previewBox.style.display = 'block';
            }
        });

        document.getElementById('btnOpenFile').addEventListener('click', () => {
            vscode.postMessage({ command: 'openExternalFile', filePath: currentSvgPath });
        });
        document.getElementById('btnOpenFolder').addEventListener('click', () => {
            vscode.postMessage({ command: 'openExternalFolder', folderPath: currentFolderPath });
        });
    </script>
</body>
</html>`;
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
