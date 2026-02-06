import { Routes, Route } from "react-router-dom";
import AdminLogin from "../pages/admin/Login";


const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/admin/login" element={<AdminLogin />} />
        {/* Future routes will go here */}
    </Routes>
  );
};

export default AppRoutes;
