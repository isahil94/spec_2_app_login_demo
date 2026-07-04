import { Navigate, Route, Routes } from 'react-router-dom';
import { useAppSelector } from './state/hooks';
import ProtectedRoute from './routes/ProtectedRoute';
import AuthLayout from './layouts/AuthLayout';
import MainLayout from './layouts/MainLayout';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import ForgotPasswordPage from './pages/ForgotPassword';
import ResetPasswordPage from './pages/ResetPassword';
import DashboardPage from './pages/Dashboard';
import TaskListPage from './pages/TaskList';
import TaskDetailsPage from './pages/TaskDetails';
import CreateTaskPage from './pages/CreateTask';
import EditTaskPage from './pages/EditTask';
import ReportsPage from './pages/Reports';
import TeamsPage from './pages/Teams';
import ProfilePage from './pages/Profile';
import SettingsPage from './pages/Settings';

export default function App() {
  const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated);

  return (
    <Routes>
      <Route
        path="/login"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <AuthLayout><LoginPage /></AuthLayout>
          )
        }
      />
      <Route
        path="/register"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <AuthLayout><RegisterPage /></AuthLayout>
          )
        }
      />
      <Route path="/forgot-password" element={<AuthLayout><ForgotPasswordPage /></AuthLayout>} />
      <Route path="/reset-password" element={<AuthLayout><ResetPasswordPage /></AuthLayout>} />
      <Route
        path="/"
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />}
      />
      <Route element={<ProtectedRoute auth={isAuthenticated} />}>
        <Route path="/dashboard" element={<MainLayout><DashboardPage /></MainLayout>} />
        <Route path="/tasks" element={<MainLayout><TaskListPage /></MainLayout>} />
        <Route path="/tasks/create" element={<MainLayout><CreateTaskPage /></MainLayout>} />
        <Route path="/tasks/:id" element={<MainLayout><TaskDetailsPage /></MainLayout>} />
        <Route path="/tasks/:id/edit" element={<MainLayout><EditTaskPage /></MainLayout>} />
        <Route path="/reports" element={<MainLayout><ReportsPage /></MainLayout>} />
        <Route path="/teams" element={<MainLayout><TeamsPage /></MainLayout>} />
        <Route path="/profile" element={<MainLayout><ProfilePage /></MainLayout>} />
        <Route path="/settings" element={<MainLayout><SettingsPage /></MainLayout>} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
