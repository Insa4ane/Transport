import { Routes, Route, Link } from "react-router-dom";
import Header from "./components/Header";
import ProtectedRoute from "./components/ProtectedRoute";
import RidesPage from "./pages/RidesPage";
import RideDetailPage from "./pages/RideDetailPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AddRidePage from "./pages/AddRidePage";
import MyBookingsPage from "./pages/MyBookingsPage";

function App() {
  return (
    <>
      <Header />
      <Routes>
        {/* publiczne */}
        <Route path="/" element={<RidesPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* tylko zalogowani */}
        <Route
          path="/rides/:id"
          element={
            <ProtectedRoute>
              <RideDetailPage />
            </ProtectedRoute>
          }
        />

        {/* tylko kierowcy */}
        <Route
          path="/rides/new"
          element={
            <ProtectedRoute driverOnly>
              <AddRidePage />
            </ProtectedRoute>
          }
        />

        {/* tylko pasażerowie */}
        <Route
          path="/bookings"
          element={
            <ProtectedRoute passengerOnly>
              <MyBookingsPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="*"
          element={
            <main>
              <h1>Nie znaleziono strony</h1>
              <Link to="/">← Wróć na stronę główną</Link>
            </main>
          }
        />
      </Routes>
    </>
  );
}

export default App;
