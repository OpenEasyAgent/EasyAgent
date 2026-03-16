// EasyAgent Dashboard JavaScript

let currentAgentId = null;
let autoRefreshInterval = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initApp();
});

function initApp() {
    loadSystemMetrics();
    loadAgents();
    loadTools();
    loadModelConfig();
    
    // Set up auto-refresh
    autoRefreshInterval = setInterval(() => {
        loadSystemMetrics();
    }, 5000);
    
    // Set up chat input
    const chatInput = document.getElementById('chat-input');
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// System Metrics
async function loadSystemMetrics() {
    try {
        const response = await fetch('/api/system/metrics');
        const data = await response.json();
        
        const cpuPercent = data.cpu?.percent || 0;
        const memoryPercent = data.memory?.percent || 0;
        
        document.getElementById('cpu-progress').style.width = cpuPercent + '%';
        document.getElementById('cpu-value').textContent = cpuPercent.toFixed(1) + '%';
        
        document.getElementById('memory-progress').style.width = memoryPercent + '%';
        document.getElementById('memory-value').textContent = memoryPercent.toFixed(1) + '%';
        
        // Update progress bar colors based on usage
        updateProgressColor('cpu-progress', cpuPercent);
        updateProgressColor('memory-progress', memoryPercent);
    } catch (error) {
        console.error('Failed to load system metrics:', error);
    }
}

function updateProgressColor(elementId, percent) {
    const element = document.getElementById(elementId);
    element.classList.remove('bg-success', 'bg-warning', 'bg-danger');
    
    if (percent < 50) {
        element.classList.add('bg-success');
    } else if (percent < 80) {
        element.classList.add('bg-warning');
    } else {
        element.classList.add('bg-danger');
    }
}

// Agents
async function loadAgents() {
    try {
        const response = await fetch('/api/agent/status');
        const agents = await response.json();
        
        const tbody = document.getElementById('agent-tbody');
        
        if (agents.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">暂无 Agent</td></tr>';
            return;
        }
        
        tbody.innerHTML = agents.map(agent => `
            <tr>
                <td><code>${agent.id}</code></td>
                <td>${agent.type || 'ChatAgent'}</td>
                <td>${agent.model_name || 'gpt-4'}</td>
                <td>
                    <span class="badge ${agent.status === 'active' ? 'bg-success' : 'bg-secondary'}">
                        ${agent.status === 'active' ? '运行中' : '已停止'}
                    </span>
                </td>
                <td>${formatDate(agent.created_at)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="selectAgent('${agent.id}')">
                        <i class="bi bi-chat"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteAgent('${agent.id}')">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load agents:', error);
        showToast('加载 Agent 失败', 'error');
    }
}

async function createAgent() {
    const agentId = document.getElementById('new-agent-id').value || 'agent_' + Date.now();
    const agentType = document.getElementById('new-agent-type').value;
    const modelName = document.getElementById('new-agent-model').value;
    
    try {
        const response = await fetch('/api/agent/create', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                agent_id: agentId,
                type: agentType,
                model_name: modelName
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Agent 创建成功', 'success');
            bootstrap.Modal.getInstance(document.getElementById('createAgentModal')).hide();
            loadAgents();
            document.getElementById('new-agent-id').value = '';
        } else {
            showToast(data.error || '创建失败', 'error');
        }
    } catch (error) {
        console.error('Failed to create agent:', error);
        showToast('创建 Agent 失败', 'error');
    }
}

async function deleteAgent(agentId) {
    if (!confirm(`确定要删除 Agent "${agentId}" 吗？`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/agent/${agentId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Agent 已删除', 'success');
            if (currentAgentId === agentId) {
                currentAgentId = null;
                disableChat();
            }
            loadAgents();
        } else {
            showToast(data.error || '删除失败', 'error');
        }
    } catch (error) {
        console.error('Failed to delete agent:', error);
        showToast('删除 Agent 失败', 'error');
    }
}

function selectAgent(agentId) {
    currentAgentId = agentId;
    document.getElementById('chat-input').disabled = false;
    document.getElementById('send-btn').disabled = false;
    document.getElementById('chat-container').innerHTML = `
        <div class="text-muted text-center py-4">
            已选择 Agent: <code>${agentId}</code>，开始对话吧
        </div>
    `;
    showToast('已选择 Agent: ' + agentId, 'success');
}

function disableChat() {
    document.getElementById('chat-input').disabled = true;
    document.getElementById('send-btn').disabled = true;
}

// Chat
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message || !currentAgentId) {
        return;
    }
    
    // Add user message
    addChatMessage('user', message);
    input.value = '';
    
    // Show loading
    const loadingHtml = `
        <div class="chat-message assistant" id="loading-message">
            <div class="message-bubble">
                <div class="spinner-border spinner-border-sm" role="status"></div>
                <span class="ms-2">处理中...</span>
            </div>
        </div>
    `;
    document.getElementById('chat-container').insertAdjacentHTML('beforeend', loadingHtml);
    scrollToBottom();
    
    try {
        const response = await fetch(`/api/agent/${currentAgentId}/chat`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        
        const data = await response.json();
        
        // Remove loading
        document.getElementById('loading-message').remove();
        
        if (data.success) {
            addChatMessage('assistant', data.response || data.message);
        } else {
            addChatMessage('assistant', '错误: ' + (data.error || '未知错误'));
        }
    } catch (error) {
        console.error('Failed to send message:', error);
        document.getElementById('loading-message').remove();
        addChatMessage('assistant', '发送消息失败，请稍后重试');
    }
}

function addChatMessage(role, content) {
    const container = document.getElementById('chat-container');
    const time = new Date().toLocaleTimeString();
    
    // Remove placeholder if exists
    if (container.querySelector('.text-muted.text-center')) {
        container.innerHTML = '';
    }
    
    const html = `
        <div class="chat-message ${role}">
            <div class="message-bubble">${escapeHtml(content)}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', html);
    scrollToBottom();
}

function scrollToBottom() {
    const container = document.getElementById('chat-container');
    container.scrollTop = container.scrollHeight;
}

// Tools
async function loadTools() {
    try {
        const response = await fetch('/api/tool/list');
        const tools = await response.json();
        
        const list = document.getElementById('tools-list');
        
        if (tools.length === 0) {
            list.innerHTML = '<li class="list-group-item text-muted">暂无工具</li>';
            return;
        }
        
        list.innerHTML = tools.map(tool => `
            <li class="list-group-item">
                <i class="bi bi-tools"></i> ${tool.name}
                <small class="text-muted d-block">${tool.description || '无描述'}</small>
            </li>
        `).join('');
    } catch (error) {
        console.error('Failed to load tools:', error);
    }
}

// Model Config
async function loadModelConfig() {
    try {
        const response = await fetch('/api/model/info');
        const config = await response.json();
        
        document.getElementById('model-select').value = config.model_name || 'gpt-4';
        document.getElementById('temperature-input').value = config.temperature || 0.7;
        document.getElementById('max-tokens-input').value = config.max_tokens || 150;
    } catch (error) {
        console.error('Failed to load model config:', error);
    }
}

async function updateModelConfig() {
    const modelName = document.getElementById('model-select').value;
    const temperature = parseFloat(document.getElementById('temperature-input').value);
    const maxTokens = parseInt(document.getElementById('max-tokens-input').value);
    
    try {
        const response = await fetch('/api/model/update', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                model_name: modelName,
                temperature: temperature,
                max_tokens: maxTokens
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('模型配置已更新', 'success');
        } else {
            showToast('更新失败', 'error');
        }
    } catch (error) {
        console.error('Failed to update model config:', error);
        showToast('更新失败', 'error');
    }
}

// Utility Functions
function refreshAll() {
    loadSystemMetrics();
    loadAgents();
    loadTools();
    loadModelConfig();
    showToast('已刷新', 'success');
}

async function clearAllData() {
    if (!confirm('确定要清空所有数据吗？这不会删除已创建的 Agent。')) {
        return;
    }
    
    // Clear chat
    document.getElementById('chat-container').innerHTML = `
        <div class="text-muted text-center py-4">
            数据已清空
        </div>
    `;
    currentAgentId = null;
    disableChat();
    showToast('已清空', 'success');
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    const toastTitle = document.getElementById('toast-title');
    
    toastMessage.textContent = message;
    
    const header = toast.querySelector('.toast-header');
    header.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'text-white');
    
    switch (type) {
        case 'success':
            header.classList.add('bg-success', 'text-white');
            toastTitle.textContent = '成功';
            break;
        case 'error':
            header.classList.add('bg-danger', 'text-white');
            toastTitle.textContent = '错误';
            break;
        case 'warning':
            header.classList.add('bg-warning');
            toastTitle.textContent = '警告';
            break;
        default:
            header.classList.add('bg-info', 'text-white');
            toastTitle.textContent = '通知';
    }
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}
