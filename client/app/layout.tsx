'use client';

import React from 'react';
import '@/styles/globals.css';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { useAuthStore } from '@/lib/store';
import { Toaster } from 'react-hot-toast';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { fetchUser } = useAuthStore();

  React.useEffect(() => {
    fetchUser();
  }, []);

  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-gray-50">
        <Toaster position="top-right" />
        <Navbar />
        <main className="flex-1">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
