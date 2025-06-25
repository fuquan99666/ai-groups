// 打字机效果展示
function displayStream(containerId) {
    const container = document.getElementById(containerId);
    const eventSource = new EventSource('/chat');
    
    eventSource.onmessage = (e) => {
        container.innerHTML += JSON.parse(e.data).content;
        container.scrollTop = container.scrollHeight;
    };
}

// 参数对比UI
function renderComparison() {
    // 同时发起两个不同参数的请求并展示对比
    const params1 = {temperature: 0.7, top_p: 0.9};
    const params2 = {temperature: 1.2, top_p: 0.5};
    
}
