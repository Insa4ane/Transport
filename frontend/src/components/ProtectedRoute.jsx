import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function ProtectedRoute({ children, driverOnly = false, passengerOnly = false }) {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  }
  if (driverOnly && !user.is_driver) {
    return <Navigate to="/" replace />;
  }
  if (passengerOnly && user.is_driver) {
    return <Navigate to="/" replace />;
  }
  return children;
}
