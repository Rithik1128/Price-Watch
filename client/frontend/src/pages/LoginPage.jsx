import React from 'react';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-300">
      <div className="bg-white shadow-2xl rounded-2xl p-10 w-full max-w-md">
        <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">Login to PriceWatch</h2>

        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-600">Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              className="w-full mt-1 px-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600">Password</label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full mt-1 px-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-xl transition duration-300"
          >
            Login
          </button>
        </form>

        <div className="my-4 text-center text-gray-500 text-sm">or</div>

        <button className="w-full border flex items-center justify-center gap-2 py-2 rounded-xl hover:bg-gray-100 transition">
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/4/4f/Icon-Google.svg"
            alt="Google"
            className="h-5 w-5"
          />
          <span className="text-sm font-medium text-gray-700">Continue with Google</span>
        </button>

        <p className="text-sm text-gray-500 text-center mt-6">
          Don't have an account?{' '}
          <a href="/register" className="text-blue-500 hover:underline">
            Sign up
          </a>
        </p>
      </div>
    </div>
  );
}
