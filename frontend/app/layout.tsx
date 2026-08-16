import Sidebar from "@/components/Sidebar";
import "./globals.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-[#050814]">
        <div className="flex h-screen overflow-hidden">

          <Sidebar />

          <div className="min-w-0 flex-1">
            {children}
          </div>

        </div>
      </body>
    </html>
  );
}