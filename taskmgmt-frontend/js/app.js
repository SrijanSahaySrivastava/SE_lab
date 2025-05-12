const API_BASE_URL = "http://127.0.0.1:8000/api";
let currentEditTaskTitle = null; // To store the title of the task being edited

// --- Token Management ---
function saveToken(token) {
  localStorage.setItem("accessToken", token);
}

function getToken() {
  return localStorage.getItem("accessToken");
}

function clearToken() {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken"); // If you store refresh tokens
}

function isLoggedIn() {
  return !!getToken();
}

// --- Navigation ---
function redirectToLogin() {
  if (
    window.location.pathname.endsWith("/login.html") ||
    window.location.pathname.endsWith("/register.html")
  ) {
    return; // Already on login/register page
  }
  window.location.href = "login.html";
}

function redirectToDashboard() {
  window.location.href = "dashboard.html";
}

// --- API Requests ---
async function makeApiRequest(
  endpoint,
  method = "GET",
  body = null,
  requiresAuth = true
) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();

  if (requiresAuth) {
    if (!token) {
      displayMessage("Authentication required. Please log in.", "error");
      redirectToLogin();
      return null;
    }
    headers["Authorization"] = `Bearer ${token}`;
  }

  const config = {
    method: method,
    headers: headers,
  };

  if (
    body &&
    (method === "POST" ||
      method === "PUT" ||
      method === "PATCH" ||
      method === "DELETE" ||
      (method === "GET" && body))
  ) {
    config.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    if (response.status === 204) {
      // No Content
      return {
        status: response.status,
        data: { message: "Operation successful (No Content)" },
      };
    }
    const responseData = await response.json();
    if (!response.ok) {
      console.error("API Error:", responseData);
      const errorMessage = responseData.detail || JSON.stringify(responseData);
      displayMessage(`Error: ${response.status} - ${errorMessage}`, "error");
      if (response.status === 401 && requiresAuth) {
        // Unauthorized
        clearToken();
        redirectToLogin();
      }
      return null;
    }
    return responseData;
  } catch (error) {
    console.error("Fetch Error:", error);
    displayMessage(`Network or fetch error: ${error.message}`, "error");
    return null;
  }
}

// --- UI Updates ---
function displayMessage(message, type = "success") {
  const messageArea = document.getElementById("messageArea");
  if (messageArea) {
    messageArea.textContent = message;
    messageArea.className =
      type === "success" ? "message-success" : "message-error";
    messageArea.classList.remove("hidden");
    setTimeout(() => {
      messageArea.classList.add("hidden");
      messageArea.textContent = "";
    }, 5000);
  } else {
    alert(message); // Fallback if no messageArea
  }
}

function getISODateTime(dateString) {
  if (!dateString) return null;
  try {
    // Input type datetime-local gives "YYYY-MM-DDTHH:MM"
    // Ensure it's converted to ISO 8601 with Z for UTC or timezone offset
    // For simplicity, assuming local time is intended and backend handles timezone conversion if necessary
    return new Date(dateString).toISOString();
  } catch (e) {
    console.warn("Could not parse date string to ISO: ", dateString);
    return dateString;
  }
}

function formatDateTimeForInput(isoString) {
  if (!isoString) return "";
  try {
    const date = new Date(isoString);
    // Format to YYYY-MM-DDTHH:MM for datetime-local input
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const day = date.getDate().toString().padStart(2, "0");
    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  } catch (e) {
    console.warn("Could not format ISO string for input: ", isoString);
    return "";
  }
}

// --- Logout ---
function logout() {
  clearToken();
  displayMessage("Logged out successfully.", "success");
  redirectToLogin();
}

// --- Common DOMContentLoaded check ---
document.addEventListener("DOMContentLoaded", () => {
  const logoutButton = document.getElementById("logoutButton");
  if (logoutButton) {
    logoutButton.addEventListener("click", logout);
  }

  // Protect non-auth pages
  const protectedPaths = ["/dashboard.html"];
  if (protectedPaths.some((path) => window.location.pathname.includes(path))) {
    if (!isLoggedIn()) {
      redirectToLogin();
    }
  }
  // Redirect if logged in and on auth pages
  const authPaths = ["/login.html", "/register.html"];
  if (authPaths.some((path) => window.location.pathname.includes(path))) {
    if (isLoggedIn()) {
      redirectToDashboard();
    }
  }
});
