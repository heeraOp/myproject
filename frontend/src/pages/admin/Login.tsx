import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const AdminLogin = () => {
  const navigate = useNavigate();

  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/login/`, {
        phone,
        password,
      });

      const { access, refresh, user } = response.data;

      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      localStorage.setItem("admin_user", JSON.stringify(user));

      navigate("/admin/dashboard");
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          err?.response?.data?.non_field_errors?.[0] ||
          "Invalid phone or password"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#020617] via-[#020617] to-black px-6">
      <div className="w-full max-w-5xl grid grid-cols-1 md:grid-cols-2 gap-14 items-center">

        {/* LEFT : BRANDING */}
        <div className="space-y-6 text-center md:text-left">
          <div className="flex items-center justify-center md:justify-start gap-4">
            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-indigo-500 to-pink-500 flex items-center justify-center text-2xl shadow-xl">
              🎱
            </div>
            <h1 className="text-5xl font-extrabold text-white">
              Housie <span className="text-indigo-400">Admin</span>
            </h1>
          </div>

          <p className="text-gray-300 text-lg">
            Control games · payouts · winners
          </p>

          <p className="text-gray-400 text-sm max-w-md">
            Secure administration panel for real-time Housie games with automated
            claims and live number calling.
          </p>

          <p className="text-gray-600 text-xs">
            © {new Date().getFullYear()} Housie Admin™
          </p>
        </div>

        {/* RIGHT : LOGIN CARD */}
        <div className="flex justify-center">
          <div className="relative w-full max-w-md">

            {/* Glow */}
            <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 opacity-25 blur-xl" />

            {/* Card */}
            <form
              onSubmit={handleSubmit}
              className="relative bg-black/70 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl px-8 py-6"
            >
              <h2 className="text-xl font-semibold text-white text-center mb-4">
                Sign in to continue
              </h2>

              {error && (
                <div className="mb-4 rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-xs text-red-400 text-center">
                  {error}
                </div>
              )}

              {/* Phone */}
              <div className="mb-3">
                <label className="block text-xs text-gray-400 mb-1">
                  Phone Number
                </label>
                <input
                  type="text"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  required
                  className="w-full rounded-md bg-gray-900 border border-gray-700 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              {/* Password */}
              <div className="mb-4">
                <label className="block text-xs text-gray-400 mb-1">
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full rounded-md bg-gray-900 border border-gray-700 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              {/* Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-md bg-gradient-to-r from-indigo-500 to-pink-500 py-2.5 text-sm font-semibold text-white shadow-md hover:opacity-90 transition disabled:opacity-60"
              >
                {loading ? "Signing in..." : "Sign In"}
              </button>

              {/* Forgot password */}
              <div className="mt-3 text-center">
                <a
                  href="/admin/forgot-password"
                  className="text-xs text-indigo-400 hover:text-indigo-300"
                >
                  Forgot password?
                </a>
              </div>
            </form>
          </div>
        </div>

      </div>
    </div>
  );
};

export default AdminLogin;
