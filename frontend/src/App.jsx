import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [role, setRole] = useState(localStorage.getItem("role") || "");
  const [page, setPage] = useState(token ? "events" : "login");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [username, setUsername] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  const [registerRole, setRegisterRole] = useState("USER");

  const [events, setEvents] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [payments, setPayments] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [message, setMessage] = useState("");

  const api = axios.create({
    baseURL: API,
    headers: token
      ? {
          Authorization: `Bearer ${token}`,
        }
      : {},
  });

  const login = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post(`${API}/auth/login`, {
        email,
        password,
      });

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("role", res.data.role);

      setToken(res.data.access_token);
      setRole(res.data.role);
      setPage("events");
      setMessage("Login successful");
    } catch (error) {
      setMessage(error.response?.data?.detail || "Login failed");
    }
  };

  const register = async (e) => {
    e.preventDefault();

    try {
      await axios.post(`${API}/auth/register`, {
        username,
        email: registerEmail,
        password: registerPassword,
        role: registerRole,
      });

      setMessage("Registration successful. Please login.");
      setPage("login");
    } catch (error) {
      setMessage(error.response?.data?.detail || "Registration failed");
    }
  };

  const loadEvents = async () => {
    try {
      const res = await axios.get(`${API}/events`);
      setEvents(res.data);
    } catch {
      setMessage("Unable to load events");
    }
  };

  const loadBookings = async () => {
    try {
      const res = await api.get("/bookings/my");
      setBookings(res.data);
    } catch (error) {
      setMessage(error.response?.data?.detail || "Unable to load bookings");
    }
  };

  const loadPayments = async () => {
    try {
      const res = await api.get("/payments/my");
      setPayments(res.data);
    } catch (error) {
      setMessage(error.response?.data?.detail || "Unable to load payments");
    }
  };

  const loadNotifications = async () => {
    try {
      const res = await api.get("/notifications");
      setNotifications(res.data);
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Unable to load notifications"
      );
    }
  };

  const bookEvent = async (eventId) => {
    try {
      await api.post("/bookings", {
        event_id: eventId,
        ticket_quantity: 1,
      });

      setMessage("Event booked successfully");
      loadBookings();
    } catch (error) {
      setMessage(error.response?.data?.detail || "Booking failed");
    }
  };

  const markRead = async (id) => {
    try {
      await api.put(`/notifications/${id}/read`);
      loadNotifications();
    } catch {
      setMessage("Unable to update notification");
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");

    setToken("");
    setRole("");
    setPage("login");
    setMessage("Logged out");
  };

  useEffect(() => {
    if (page === "events") loadEvents();
    if (page === "bookings" && token) loadBookings();
    if (page === "payments" && token) loadPayments();
    if (page === "notifications" && token) loadNotifications();
  }, [page]);

  if (!token && page === "register") {
    return (
      <div className="auth-page">
        <div className="auth-card">
          <h1>SmartEvent</h1>
          <h2>Create Account</h2>

          {message && <p className="message">{message}</p>}

          <form onSubmit={register}>
            <input
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />

            <input
              type="email"
              placeholder="Email"
              value={registerEmail}
              onChange={(e) => setRegisterEmail(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={registerPassword}
              onChange={(e) => setRegisterPassword(e.target.value)}
              required
            />

            <select
              value={registerRole}
              onChange={(e) => setRegisterRole(e.target.value)}
            >
              <option value="USER">User</option>
              <option value="ORGANIZER">Organizer</option>
            </select>

            <button type="submit">Register</button>
          </form>

          <button
            className="link-button"
            onClick={() => setPage("login")}
          >
            Already have an account? Login
          </button>
        </div>
      </div>
    );
  }

  if (!token) {
    return (
      <div className="auth-page">
        <div className="auth-card">
          <h1>SmartEvent</h1>
          <h2>Login</h2>

          {message && <p className="message">{message}</p>}

          <form onSubmit={login}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <button type="submit">Login</button>
          </form>

          <button
            className="link-button"
            onClick={() => setPage("register")}
          >
            Create new account
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <header>
        <div>
          <h1>SmartEvent</h1>
          <span>{role}</span>
        </div>

        <nav>
          <button onClick={() => setPage("events")}>Events</button>

          {role === "USER" && (
            <>
              <button onClick={() => setPage("bookings")}>
                My Bookings
              </button>

              <button onClick={() => setPage("payments")}>
                Payments
              </button>
            </>
          )}

          <button onClick={() => setPage("notifications")}>
            Notifications
          </button>

          <button onClick={logout}>Logout</button>
        </nav>
      </header>

      <main>
        {message && <p className="message">{message}</p>}

        {page === "events" && (
          <>
            <h2>Available Events</h2>

            <div className="grid">
              {events.map((event) => (
                <div className="card" key={event.id}>
                  <h3>{event.title}</h3>

                  <p>{event.description}</p>

                  <p>
                    <strong>Category:</strong> {event.category}
                  </p>

                  <p>
                    <strong>Location:</strong> {event.location}
                  </p>

                  <p>
                    <strong>Price:</strong> ₹{event.ticket_price}
                  </p>

                  <p>
                    <strong>Date:</strong>{" "}
                    {new Date(event.event_date).toLocaleString()}
                  </p>

                  {role === "USER" && (
                    <button onClick={() => bookEvent(event.id)}>
                      Book Ticket
                    </button>
                  )}
                </div>
              ))}
            </div>
          </>
        )}

        {page === "bookings" && (
          <>
            <h2>My Bookings</h2>

            <div className="grid">
              {bookings.map((booking) => (
                <div className="card" key={booking.id}>
                  <h3>Booking #{booking.id}</h3>

                  <p>Event ID: {booking.event_id}</p>
                  <p>Tickets: {booking.ticket_quantity}</p>
                  <p>Total: ₹{booking.total_price}</p>
                  <p>Status: {booking.booking_status}</p>
                </div>
              ))}
            </div>
          </>
        )}

        {page === "payments" && (
          <>
            <h2>Payment History</h2>

            <div className="grid">
              {payments.map((payment) => (
                <div className="card" key={payment.id}>
                  <h3>Payment #{payment.id}</h3>
                  <p>Booking: {payment.booking_id}</p>
                  <p>Amount: ₹{payment.amount}</p>
                  <p>Method: {payment.payment_method}</p>
                  <p>Status: {payment.payment_status}</p>
                </div>
              ))}
            </div>
          </>
        )}

        {page === "notifications" && (
          <>
            <h2>Notifications</h2>

            <div className="grid">
              {notifications.map((notification) => (
                <div className="card" key={notification.id}>
                  <h3>{notification.title}</h3>

                  <p>{notification.message}</p>
                  <p>Type: {notification.type}</p>

                  <p>
                    Status: {notification.is_read ? "Read" : "Unread"}
                  </p>

                  {!notification.is_read && (
                    <button
                      onClick={() => markRead(notification.id)}
                    >
                      Mark as Read
                    </button>
                  )}
                </div>
              ))}
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;