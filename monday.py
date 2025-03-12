<div class="task-container">
    <h2>📋 Tareas en <span id="board-name">Cargando...</span></h2>
    <div id="tasks-list">Cargando tareas...</div>
</div>

<script>
    const API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ4NDExMTkyNCwiYWFpIjoxMSwidWlkIjo3MzMxMDUyOCwiaWFkIjoiMjAyNS0wMy0xMVQxNzo1NToyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg0ODc4MzgsInJnbiI6ImV1YzEifQ.Pp_UNPi-wRC1Y9yxFEQ_Rs9VC2J78QLjK58x7puQBAM";
    const BOARD_ID = "1863450371"; // ID del board "HR"
    const API_URL = "https://api.monday.com/v2";

    async function getTasks() {
        const query = `{
            boards(ids: ${BOARD_ID}) {
                name
                items_page {
                    items {
                        id
                        name
                        column_values {
                            id
                            value
                        }
                    }
                }
            }
        }`;

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": API_KEY
                },
                body: JSON.stringify({ query })
            });

            const data = await response.json();
            const board = data.data.boards[0];
            document.getElementById("board-name").textContent = board.name;

            const tasks = board.items_page.items;
            const tasksList = document.getElementById("tasks-list");
            tasksList.innerHTML = "";

            if (tasks.length === 0) {
                tasksList.innerHTML = "<div class='task-item'>No hay tareas disponibles 📌</div>";
                return;
            }

            tasks.forEach(task => {
                let startDate = "No definido";
                let dueDate = "No definido";
                let status = "No definido";
                let priority = "No definido";
                let notes = "No definido";

                task.column_values.forEach(col => {
                    if (col.id === "project_timeline" && col.value) {
                        const timeline = JSON.parse(col.value);
                        startDate = timeline.from || "No definido";
                        dueDate = timeline.to || "No definido";
                    }
                    if (col.id === "project_status" && col.value) {
                        status = JSON.parse(col.value).index || "No definido";
                    }
                    if (col.id === "priority_1" && col.value) {
                        priority = JSON.parse(col.value).index || "No definido";
                    }
                    if (col.id === "text9" && col.value) {
                        notes = col.value.replace(/"/g, "") || "No definido";
                    }
                });

                const taskElement = `
                    <div class="task-item">
                        <h3>${task.name}</h3>
                        <p>📅 <strong>Inicio:</strong> ${startDate} | ⏳ <strong>Vencimiento:</strong> ${dueDate}</p>
                        <p>🔴 <strong>Estado:</strong> ${status} | ⭐ <strong>Prioridad:</strong> ${priority}</p>
                        <p>📄 <strong>Notas:</strong> ${notes}</p>
                    </div>
                `;
                tasksList.innerHTML += taskElement;
            });

        } catch (error) {
            console.error("Error obteniendo tareas:", error);
            document.getElementById("tasks-list").innerHTML = "<div class='task-item error'>Error al cargar tareas ❌</div>";
        }
    }

    getTasks();
</script>

<style>
    .task-container {
        background: #2B6CB0; /* Azul intenso */
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        max-width: 90%;
        margin: auto;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }

    h2 {
        font-size: 22px;
        margin-bottom: 15px;
        font-weight: bold;
    }

    .task-item {
        background: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: left;
    }

    .task-item h3 {
        margin: 0;
        font-size: 18px;
        font-weight: bold;
    }

    .task-item p {
        margin: 5px 0;
        font-size: 14px;
    }

    .task-item.error {
        background: #ff4d4d;
        color: white;
        font-weight: bold;
    }

    @media (max-width: 768px) {
        .task-container {
            max-width: 100%;
        }
    }
</style>
