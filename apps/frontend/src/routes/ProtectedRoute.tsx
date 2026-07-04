import { Navigate, Outlet } from 'react-router-dom';

interface ProtectedRouteProps {
  auth: boolean;
}

export default function ProtectedRoute({ auth }: ProtectedRouteProps) {
  return auth ? <Outlet /> : <Navigate to="/login" replace />;
}
