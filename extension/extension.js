const vscode = require('vscode');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

let outputConfigPath = '';
let statusBarItem = null;

function getEffectiveOutputDir() {
    try {
        if (fs.existsSync(outputConfigPath)) {
            const data = JSON.parse(fs.readFileSync(outputConfigPath, 'utf-8'));
            if (data && data.outputDir && fs.existsSync(data.outputDir)) {
                return data.outputDir;
            }
        }
    } catch (e) {}
    return 'd:\\ComfyUI\\svg';
}

function saveOutputDir(newDir) {
    try {
        const data = { outputDir: newDir, updatedAt: new Date().toISOString() };
        fs.writeFileSync(outputConfigPath, JSON.stringify(data, null, 2), 'utf-8');
    } catch (e) {}
    if (statusBarItem) {
        statusBarItem.text = `$(folder-opened) Output: ${path.basename(newDir)}`;
        statusBarItem.tooltip = `Thư mục lưu ảnh vector: ${newDir} (Nhấp để đổi)`;
    }
}

function activate(context) {
    const wsFolders = vscode.workspace.workspaceFolders;
    const rootDir = wsFolders && wsFolders.length > 0 ? wsFolders[0].uri.fsPath : 'd:\\ComfyUI\\svg';
    outputConfigPath = path.join(rootDir, 'output_config.json');

    // Create Status Bar Button (Always visible on the status bar for instant 1-click access)
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'imageToVector.selectOutputDir';
    const initialDir = getEffectiveOutputDir();
    statusBarItem.text = `$(folder-opened) Output: ${path.basename(initialDir)}`;
    statusBarItem.tooltip = `Thư mục lưu ảnh vector: ${initialDir} (Nhấp để chọn thư mục khác)`;
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Command to select output directory (via Windows Folder Browser)
    let selectDirCmd = vscode.commands.registerCommand('imageToVector.selectOutputDir', async function () {
        const currentDir = getEffectiveOutputDir();
        const options = {
            canSelectFiles: false,
            canSelectFolders: true,
            canSelectMany: false,
            openLabel: 'Chọn thư mục này làm nơi xuất ảnh vector',
            title: 'Chọn thư mục xuất ảnh vector đầu ra'
        };
        if (fs.existsSync(currentDir)) {
            options.defaultUri = vscode.Uri.file(currentDir);
        }

        const folderUri = await vscode.window.showOpenDialog(options);
        if (folderUri && folderUri[0]) {
            const selectedPath = folderUri[0].fsPath;
            saveOutputDir(selectedPath);
            vscode.window.showInformationMessage(
                `✅ Đã đặt thư mục ảnh đầu ra: ${selectedPath}`,
                'Mở thư mục trên máy'
            ).then(sel => {
                if (sel === 'Mở thư mục trên máy') {
                    exec(`explorer.exe "${selectedPath}"`);
                }
            });
        }
    });

    // Command to open drag & drop webview
    let dropzoneCmd = vscode.commands.registerCommand('imageToVector.openDropzone', function () {
        const panel = vscode.window.createWebviewPanel(
            'imageToVectorDropzone',
            'Image to Vector (Drag & Drop)',
            vscode.ViewColumn.Beside,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        const currentOutDir = getEffectiveOutputDir();
        panel.webview.html = getWebviewContent(currentOutDir);

        panel.webview.onDidReceiveMessage(
            message => {
                if (message.command === 'vectorize') {
                    const filePath = message.filePath;
                    const outDir = getEffectiveOutputDir();
                    if (!fs.existsSync(outDir)) {
                        fs.mkdirSync(outDir, { recursive: true });
                    }
                    const outputSvg = path.join(outDir, 'output_vector.svg');
                    const scriptPath = path.join(rootDir, 'image-to-vector-skill-repo', 'scripts', 'auto_vectorizer.py');

                    vscode.window.showInformationMessage(`Đang vector hóa vào: ${outDir}`);

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
                            folderPath: outDir,
                            previewUri: previewUri
                        });
                        vscode.window.showInformationMessage('Vector hóa thành công!');
                    });
                } else if (message.command === 'selectFolder') {
                    vscode.commands.executeCommand('imageToVector.selectOutputDir');
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

    context.subscriptions.push(selectDirCmd, dropzoneCmd);
}

function getWebviewContent(currentDir) {
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
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .dir-badge {
        font-size: 12px;
        background: rgba(255,255,255,0.08);
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid var(--vscode-widget-border);
        cursor: pointer;
    }
    .dropzone {
        border: 2px dashed #3b82f6;
        border-radius: 16px;
        padding: 35px 20px;
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
        margin-top: 20px;
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
        <h3 style="margin:0;">🎯 Xưởng Tạo Ảnh Vector</h3>
        <span class="dir-badge" onclick="selectFolder()">📂 Thư mục: <span id="lblDir">${currentDir}</span> ✏️</span>
    </div>

    <div class="dropzone" id="dropArea">
        <p style="font-size: 28px; margin: 0 0 10px;">📥</p>
        <p style="font-size: 15px; font-weight: 600; margin: 0 0 6px;">Kéo & thả ảnh vào đây</p>
        <p style="font-size: 12px; opacity: 0.7; margin: 0 0 12px;">Hỗ trợ JPG, PNG, WEBP, BMP</p>
        <input type="file" id="fileInput" accept="image/*" style="display: none;" />
        <button class="btn" onclick="document.getElementById('fileInput').click()">Chọn file từ máy</button>
    </div>

    <div class="preview-box" id="previewBox">
        <h4 style="margin:0;">✨ Kết Quả Vector Hóa</h4>
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

        function selectFolder() {
            vscode.postMessage({ command: 'selectFolder' });
        }

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
