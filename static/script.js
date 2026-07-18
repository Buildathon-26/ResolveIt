async function submitComplaint() {
    const title = document.getElementById("title").value;
    const category = document.getElementById("category").value;
    const photo = document.getElementById("photo").files[0];

    if (title === "") {
        alert("Enter complaint");
        return;
    }

    const formData = new FormData();
    formData.append("title", title);
    formData.append("category", category);
    if (photo) formData.append("photo", photo);

    await fetch("/add_complaints", {
        method: "POST",
        body: formData
    });

    document.getElementById("title").value = "";
    document.getElementById("photo").value = "";
    loadComplaints();
}

async function loadComplaints() {
    const response = await fetch("/get_complaints");
    let data = await response.json();

    const search = document.getElementById("search").value.toLowerCase();
    if (search) {
        data = data.filter(item =>
            item.title.toLowerCase().includes(search) ||
            item.category.toLowerCase().includes(search)
        );
    }

    let html = "";
    data.forEach(item => {
        html += `
        <div class="card">
            <div>
                <h3>${item.title}
                    ${item.trending ? '<span class="badge">🔥 Trending</span>' : ''}
                </h3>
                <div class="category">${item.category}</div>
                ${item.photo ? `<img src="${item.photo}" width="200">` : ""}
                <div class="urgency">
                    Urgency: <progress value="${item.urgency}" max="10"></progress> ${item.urgency}
                </div>
                ${item.resolved ? '<div class="resolved">✅ Resolved</div>' : ''}
                <div>By: ${item.author}</div>
            </div>
            <div>
                <p>👍 ${item.votes}</p>
                <div class="actions">
                    <button class="vote" onclick="vote(${item.id})">Upvote</button>
                    ${!item.resolved ? `<button class="resolve" onclick="resolveComplaint(${item.id})">Resolve</button>` : ''}
                </div>
            </div>
        </div>`;
    });

    document.getElementById("complaints").innerHTML = html;

    const stats = await fetch("/analytics");
    const analytics = await stats.json();
    document.getElementById("analytics").innerHTML = `
        <p>Total: ${analytics.total} | Open: ${analytics.open} | Resolved: ${analytics.resolved}</p>
        <p>Categories: ${Object.entries(analytics.categories).map(([k, v]) => k + ': ' + v).join(', ')}</p>
    `;
}

async function vote(id) {
    await fetch(`/vote/${id}`, { method: "POST" });
    loadComplaints();
}

async function resolveComplaint(id) {
    await fetch(`/resolve/${id}`, { method: "POST" });
    confetti({ particleCount: 150, spread: 100, origin: { y: 0.6 } });
    loadComplaints();
}

loadComplaints();
setInterval