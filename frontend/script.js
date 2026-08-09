const API_URL = "http://127.0.0.1:8000";

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




function saveTasksToCache() {

    localStorage.setItem(
        "taskflow_tasks",
        JSON.stringify(tasks)
    );
}


function loadCachedTasks() {

    const cachedTasks =
        localStorage.getItem(
            "taskflow_tasks"
        );

    if (cachedTasks) {

        tasks = JSON.parse(cachedTasks);

        renderTasks(tasks);

        updateStatistics(tasks);
    }
}




async function loadTasks() {

    loadingMessage.textContent =
        "Loading latest tasks...";

    try {

        const response =
            await fetch(
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


        const newTask = {

            title: title,

            status: "pending",

            priority:
                priorityInput.value,

            due_date:
                dueDateInput.value.trim()
                || null,

            project_id:
                Number(
                    projectIdInput.value
                )
        };


        try {

            const response =
                await fetch(
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

            projectIdInput.value =
                "1";


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
            await fetch(
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
            await fetch(
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




loadCachedTasks();

loadTasks();