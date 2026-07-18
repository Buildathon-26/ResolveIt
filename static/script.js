javascript
async function loadComplaints() {

    const response =
        await fetch("/get_complaints");

    const data =
        await response.json();

    let html = "";

    data.forEach(item => {

        html += `

        <div class="card">

            <div>

                <h3>
                    ${item.title}

                    ${item.trending
                ? '<span class="badge">🔥 Trending</span>'
                : ''}
                </h3>

                <div class="category">
                    ${item.category}
                </div>

                <div class="urgency">
                    Urgency Score:
                    ${item.urgency}
                </div>

                ${item.resolved
                ?
                '<div class="resolved">✅ Resolved</div>'
                :
                ''
            }

            </div>

            <div>

                <p>👍 ${item.votes}</p>

                <div class="actions">

                    <button
                    class="vote"
                    onclick="vote(${item.id})">
                    Upvote
                    </button>

                    <button
                    class="share"
                    onclick="shareComplaint(${item.id},
                    '${item.title}')">
                    WhatsApp
                    </button>

                    ${!item.resolved
                ?
                `<button
                    class="resolve"
                    onclick="resolveComplaint(${item.id})">
                    Resolve
                    </button>`
                :
                ''
            }

                </div>

            </div>

        </div>
        `;
    });

    document.getElementById(
        "complaints"
    ).innerHTML = html;
}


async function submitComplaint() {

    const title =
        document.getElementById(
            "title"
        ).value;

    const category =
        document.getElementById(
            "category"
        ).value;

    if (title === "") {
        alert("Enter complaint");
        return;
    }

    await fetch(
        "/add_complaint",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                title,
                category
            })
        }
    );

    document.getElementById(
        "title"
    ).value = "";

    loadComplaints();
}


async function vote(id) {

    await fetch(
        `/vote/${id}`,
        {
            method: "POST"
        }
    );

    loadComplaints();
}


function shareComplaint(id, title) {

    const link =
        window.location.origin +
        "/#complaint-" + id;

    const message =
        `Support this complaint:\n\n${title}\n\n${link}`;

    const whatsapp =
        `https://wa.me/?text=${encodeURIComponent(message)}`;

    window.open(
        whatsapp,
        "_blank"
    );
}


async function resolveComplaint(id) {

    await fetch(
        `/resolve/${id}`,
        {
            method: "POST"
        }
    );

    confetti({
        particleCount: 150,
        spread: 100,
        origin: { y: 0.6 }
    });

    loadComplaints();
}


loadComplaints();

setInterval(() => {
    loadComplaints();
}, 15000);