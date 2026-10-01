import { Navigate, RouterProvider, createBrowserRouter } from "react-router-dom";
import CampingPage from "../pages/CampingPage.tsx";

const router = createBrowserRouter([
  { path: "/", element: <Navigate to="/camping" replace /> },
  { path: "/camping", element: <CampingPage /> },
]);

export default function App() {
  return <RouterProvider router={router} />;
}
