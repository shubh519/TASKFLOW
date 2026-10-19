const API_URL = "http://127.0.0.1:8000";
let accessToken = sessionStorage.getItem("taskflow_access_token");

function authFetch(url, options = {}) {
    const headers = new Headers(options.headers || {});
    if (accessToken) headers.set("Authorization", `Bearer ${accessToken}`);
    return fetch(url, { ...options, headers });
}


function getCurrentUserIdFromToken() {
    if (!accessToken) throw new Error("Please log in first.");
    try {
        const payloadPart = accessToken.split(".")[1]
            .replace(/-/g, "+").replace(/_/g, "/");
        const payload = JSON.parse(atob(payloadPart));
        const userId = Number(payload.sub);
        if (!Number.isInteger(userId) || userId <= 0) throw new Error();
        return userId;
    } catch {
        throw new Error("Your login session is invalid. Please log in again.");
    }
}

async function apiJson(url, options = {}) {
    const response = await authFetch(url, options);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        const detail = Array.isArray(data.detail)
            ? data.detail.map(item => item.msg || "Invalid input").join(", ")
            : (data.detail || `Request failed (${response.status})`);
        throw new Error(detail);
    }
    return data;
}

async function loadProjects() {
    if (!accessToken) return;
    const projectSelect = document.getElementById("projectId");
    projectSelect.innerHTML = '<option value="">Loading projects...</option>';
    try {
        let projects = await apiJson(`${API_URL}/projects`);

        // New accounts may not have a project yet. Create one for the logged-in user.
        if (projects.length === 0) {
            const ownerId = getCurrentUserIdFromToken();
            await apiJson(`${API_URL}/projects`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Accept": "application/json" },
                body: JSON.stringify({
                    name: "My TaskFlow Project",
                    description: "Default project for personal tasks",
                    owner_id: ownerId
                })
            });
            projects = await apiJson(`${API_URL}/projects`);
        }

        projectSelect.innerHTML = "";
        for (const project of projects) {
            const option = document.createElement("option");
            option.value = String(project.id);
            option.textContent = `${project.name} (ID: ${project.id})`;
            projectSelect.appendChild(option);
        }
        if (projects.length === 0) {
            projectSelect.innerHTML = '<option value="">No projects available</option>';
            throw new Error("No project is available for this account.");
        }
    } catch (error) {
        projectSelect.innerHTML = '<option value="">Unable to load projects</option>';
        const message = `Project loading failed: ${error.message}`;
        const authMessage = document.getElementById("authMessage");
        if (authMessage) authMessage.textContent = message;
        console.error(message, error);
        throw error;
    }
}



function updateAuthUI(message = "") {
    const loggedIn = Boolean(accessToken);
    const status = document.getElementById("authStatus");
    const logoutButton = document.getElementById("logoutButton");
    const authMessage = document.getElementById("authMessage");
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const authGrid = document.querySelector("#authSection .auth-grid");

    if (status) {
        status.textContent = loggedIn
            ? "You are logged in. Your tasks are scoped to your account."
            : "Log in or create an account to manage your own tasks.";
    }

    // Hide the whole forms container while logged in, not just each form.
    if (authGrid) {
        authGrid.hidden = loggedIn;
        authGrid.style.setProperty("display", loggedIn ? "none" : "", "important");
    }
    [loginForm, registerForm].forEach((form) => {
        if (!form) return;
        form.hidden = loggedIn;
        if (loggedIn) form.style.setProperty("display", "none", "important");
        else form.style.removeProperty("display");
    });

    if (logoutButton) {
        logoutButton.hidden = !loggedIn;
        if (loggedIn) logoutButton.style.removeProperty("display");
        else logoutButton.style.setProperty("display", "none", "important");
    }
    if (authMessage) authMessage.textContent = message;
}


async function authenticate(path, payload) {
    const response = await authFetch(`${API_URL}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload)
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        const detail = Array.isArray(data.detail)
            ? data.detail.map(item => item.msg || "Invalid input").join(", ")
            : (data.detail || "Authentication failed");
        throw new Error(detail);
    }
    return data;
}


const taskForm =
    document.getElementById("taskForm");

const taskTitle =
    document.getElementById("taskTitle");

const priorityInput =
    document.getElementById("priority");

const dueDateInput =
    document.getElementById("dueDate");

const projectIdInput =
    document.getElementById("projectId");

const titleError =
    document.getElementById("titleError");

const taskList =
    document.getElementById("taskList");

const loadingMessage =
    document.getElementById("loadingMessage");

const refreshButton =
    document.getElementById("refreshButton");

const totalTasks =
    document.getElementById("totalTasks");

const pendingTasks =
    document.getElementById("pendingTasks");

const completedTasks =
    document.getElementById("completedTasks");


let tasks = [];




function getTaskCacheKey() {
    if (!accessToken) return null;
    try {
        const payloadPart = accessToken.split(".")[1]
            .replace(/-/g, "+").replace(/_/g, "/");
        const payload = JSON.parse(atob(payloadPart));
        return `taskflow_tasks_user_${payload.sub}`;
    } catch {
        return null;
    }
}

function saveTasksToCache() {
    const cacheKey = getTaskCacheKey();
    if (!cacheKey) return;
    localStorage.setItem(cacheKey, JSON.stringify(tasks));
}

function loadCachedTasks() {
    const cacheKey = getTaskCacheKey();
    if (!cacheKey) return;
    const cachedTasks = localStorage.getItem(cacheKey);

    if (cachedTasks) {

        tasks = JSON.parse(cachedTasks);

        renderTasks(tasks);

        updateStatistics(tasks);
    }
}




async function loadTasks() {
    if (!accessToken) {
        tasks = [];
        renderTasks([]);
        updateStatistics([]);
        loadingMessage.textContent = "Log in to load your tasks.";
        return;
    }

    loadingMessage.textContent = "Loading latest tasks...";

    try {

        const response =
            await authFetch(
                `${API_URL}/tasks`
            );

        if (!response.ok) {
            throw new Error(
                "Unable to load tasks"
            );
        }

        tasks =
            await response.json();

        saveTasksToCache();

        renderTasks(tasks);

        updateStatistics(tasks);

        loadingMessage.textContent = "";

    } catch (error) {

        loadingMessage.textContent =
            "Backend unavailable. Showing cached tasks.";

        console.error(error);
    }
}




function renderTasks(taskData) {

    taskList.textContent = "";

    if (taskData.length === 0) {

        const emptyMessage =
            document.createElement("p");

        emptyMessage.className =
            "empty-message";

        emptyMessage.textContent =
            "No tasks available. Add your first task.";

        taskList.appendChild(
            emptyMessage
        );

        return;
    }


    taskData.forEach((task) => {

        const taskItem =
            document.createElement("article");

        taskItem.className =
            `task-item ${task.priority}`;


        const taskInfo =
            document.createElement("div");


        const title =
            document.createElement("h3");

        title.className =
            "task-title";

        title.textContent =
            task.title;


        const meta =
            document.createElement("div");

        meta.className =
            "task-meta";


        const status =
            document.createElement("span");

        status.textContent =
            `Status: ${task.status}`;


        const priority =
            document.createElement("span");

        priority.textContent =
            `Priority: ${task.priority}`;


        const dueDate =
            document.createElement("span");

        dueDate.textContent =
            `Due: ${task.due_date || "Not set"}`;


        const project =
            document.createElement("span");

        project.textContent =
            `Project: ${task.project_id}`;


        meta.appendChild(status);
        meta.appendChild(priority);
        meta.appendChild(dueDate);
        meta.appendChild(project);


        taskInfo.appendChild(title);
        taskInfo.appendChild(meta);


        const actions =
            document.createElement("div");

        actions.className =
            "task-actions";


        const editButton =
            document.createElement("button");

        editButton.className =
            "edit-button";

        editButton.textContent =
            "Edit";


        editButton.addEventListener(
            "click",
            function () {
                editTask(task);
            }
        );


        const deleteButton =
            document.createElement("button");

        deleteButton.className =
            "delete-button";

        deleteButton.textContent =
            "Delete";


        deleteButton.addEventListener(
            "click",
            function () {
                deleteTask(task.id);
            }
        );


        actions.appendChild(editButton);
        actions.appendChild(deleteButton);


        taskItem.appendChild(taskInfo);
        taskItem.appendChild(actions);


        taskList.appendChild(taskItem);
    });
}




taskForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const title =
            taskTitle.value.trim();


        if (!title) {

            titleError.textContent =
                "Task title is required.";

            return;
        }


        titleError.textContent = "";


        const selectedProjectId = Number(projectIdInput.value);
        if (!Number.isInteger(selectedProjectId) || selectedProjectId <= 0) {
            alert("Please select one of your projects first.");
            return;
        }

        const newTask = {
            title,
            status: "pending",
            priority: priorityInput.value,
            due_date: dueDateInput.value.trim() || null,
            project_id: selectedProjectId
        };


        try {

            const response =
                await authFetch(
                    `${API_URL}/tasks`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                newTask
                            )
                    }
                );


            if (!response.ok) {

                const errorData =
                    await response.json();

                throw new Error(
                    errorData.detail
                    || "Unable to create task"
                );
            }


            const createdTask =
                await response.json();


            tasks.push(createdTask);

            saveTasksToCache();

            renderTasks(tasks);

            updateStatistics(tasks);


            taskForm.reset();

            priorityInput.value =
                "medium";



        } catch (error) {

            alert(
                `Error: ${error.message}`
            );
        }
    }
);




taskTitle.addEventListener(
    "input",
    function () {

        if (taskTitle.value.trim()) {

            titleError.textContent = "";
        }
    }
);




async function editTask(task) {

    const newTitle =
        prompt(
            "Edit task title:",
            task.title
        );


    if (newTitle === null) {
        return;
    }


    if (!newTitle.trim()) {

        alert(
            "Task title cannot be empty."
        );

        return;
    }


    const newStatus =
        prompt(
            "Status: pending or completed",
            task.status
        );


    if (newStatus === null) {
        return;
    }


    const updatedTask = {

        title:
            newTitle.trim(),

        status:
            newStatus.trim(),

        priority:
            task.priority,

        due_date:
            task.due_date,

        project_id:
            task.project_id
    };


    try {

        const response =
            await authFetch(
                `${API_URL}/tasks/${task.id}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            updatedTask
                        )
                }
            );


        if (!response.ok) {

            throw new Error(
                "Unable to update task"
            );
        }


        const savedTask =
            await response.json();


        tasks =
            tasks.map((item) => {

                if (
                    item.id ===
                    savedTask.id
                ) {
                    return savedTask;
                }

                return item;
            });


        saveTasksToCache();

        renderTasks(tasks);

        updateStatistics(tasks);


    } catch (error) {

        alert(error.message);
    }
}




async function deleteTask(taskId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this task?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await authFetch(
                `${API_URL}/tasks/${taskId}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Unable to delete task"
            );
        }


        tasks =
            tasks.filter(
                (task) =>
                    task.id !== taskId
            );


        saveTasksToCache();

        renderTasks(tasks);

        updateStatistics(tasks);


    } catch (error) {

        alert(error.message);
    }
}




function updateStatistics(taskData) {

    totalTasks.textContent =
        taskData.length;


    const pending =
        taskData.filter(
            task =>
                task.status === "pending"
        ).length;


    const completed =
        taskData.filter(
            task =>
                task.status === "completed"
        ).length;


    pendingTasks.textContent =
        pending;

    completedTasks.textContent =
        completed;
}




refreshButton.addEventListener(
    "click",
    loadTasks
);





const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const logoutButton = document.getElementById("logoutButton");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
        const data = await authenticate("/auth/login", {
            email: document.getElementById("loginEmail").value.trim(),
            password: document.getElementById("loginPassword").value
        });
        accessToken = data.access_token;
        sessionStorage.setItem("taskflow_access_token", accessToken);
        updateAuthUI("Login successful.");
        await loadProjects();
        await loadTasks();
    } catch (error) {
        updateAuthUI(error.message);
    }
});

registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
        const name = document.getElementById("registerName").value.trim();
        const email = document.getElementById("registerEmail").value.trim();
        const password = document.getElementById("registerPassword").value;
        await authenticate("/auth/register", { name, email, password });
        const data = await authenticate("/auth/login", { email, password });
        accessToken = data.access_token;
        sessionStorage.setItem("taskflow_access_token", accessToken);
        registerForm.reset();
        updateAuthUI("Account created and logged in.");
        await loadProjects();
        await loadTasks();
    } catch (error) {
        updateAuthUI(error.message);
    }
});

logoutButton.addEventListener("click", () => {
    accessToken = null;
    sessionStorage.removeItem("taskflow_access_token");
    tasks = [];
    saveTasksToCache();
    renderTasks(tasks);
    updateStatistics(tasks);
    const projectSelect = document.getElementById("projectId");
    projectSelect.innerHTML = '<option value="">Log in to load projects</option>';
    updateAuthUI("You have logged out.");
    loadTasks();
});

updateAuthUI();

if (accessToken) {
    loadCachedTasks();
    loadProjects().then(loadTasks).catch(() => {
        loadingMessage.textContent = "Could not load your projects. Check the backend and log in again if needed.";
    });
} else {
    renderTasks([]);
    updateStatistics([]);
    loadingMessage.textContent = "Log in to load your tasks.";
}
