<div>
    <h2>Tareas en el Board HR</h2>
    <p id="error-message" style="color: red; display: none;">No se pudieron obtener los datos del tablero.</p>
    <ul id="monday-tasks">Cargando tareas...</ul>
</div>

<script>
    const API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ4NDExMTkyNCwiYWFpIjoxMSwidWlkIjo3MzMxMDUyOCwiaWFkIjoiMjAyNS0wMy0xMVQxNzo1NToyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg0ODc4MzgsInJnbiI6ImV1YzEifQ.Pp_UNPi-wRC1Y9yxFEQ_Rs9VC2J78QLjK58x7puQBAM";
    const BOARD_ID = "1863450371"; // ID del tablero HR
    const API_URL = "https://api.monday.com/v2";

    async function getMondayTasks() {
        const query = `{
            boards(ids: ${BOARD_ID}) {
                id
                name
                items_page {
                    items {
                        id
                        name
                    }
                }
            }
        }`;

        try {
            console.log("Enviando consulta a Monday.com...");

            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": API_KEY
                },
                body: JSON.stringify({ query })
            });

            const data = await response.json();
            console.log("Respuesta de Monday:", data);

            if (!data.data || !data.data.boards || data.data.boards.length === 0) {
                throw new Error("No se encontraron tableros con este ID.");
            }

            const board = data.data.boards[0];
            const tasks = board.items_page.items;

            const taskList = document.getElementById("monday-tasks");
            taskList.innerHTML = "";

            if (tasks.length === 0) {
                taskList.innerHTML = "<li>No hay tareas disponibles</li>";
                return;
            }

            tasks.forEach(task => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>${task.name}</strong>`;
                taskList.appendChild(li);
            });

        } catch (error) {
            console.error("Error al obtener tareas:", error);
            document.getElementById("error-message").style.display = "block";
            document.getElementById("monday-tasks").innerHTML = "<li>Error al cargar tareas</li>";
        }
    }

    getMondayTasks();
</script>
