"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {

  const pathname = usePathname();

  const links = [
    {
      name: "Home",
      href: "/",
      icon: "⌂",
    },
    {
      name: "Chat",
      href: "/chat",
      icon: "▢",
    },
    {
      name: "History",
      href: "/history",
      icon: "◷",
    },
  ];

  return (
    <aside className="w-64 min-h-screen border-r border-white/10 bg-[#0d111a] p-5">

      {/* Logo */}

      <div className="mb-10">

        <div className="mb-4 text-4xl">
          🤖
        </div>

        <h1 className="text-xl font-bold text-white">
          Multi PDF RAG
        </h1>

        <p className="mt-2 text-sm leading-6 text-gray-400">
          Ask anything from
          <br />
          your documents
        </p>

      </div>


      {/* Navigation */}

      <nav className="space-y-2">

        {links.map((link) => {

          const active =
            pathname === link.href;

          return (

            <Link
              key={link.href}
              href={link.href}
              className={`
                flex items-center gap-3
                rounded-xl
                px-4 py-3
                transition
                ${
                  active
                    ? "bg-purple-600/30 text-white"
                    : "text-gray-400 hover:bg-white/5 hover:text-white"
                }
              `}
            >

              <span className="text-xl">
                {link.icon}
              </span>

              <span>
                {link.name}
              </span>

            </Link>

          );

        })}

      </nav>


      {/* Upload */}

      <div className="mt-8">

        <Link
          href="/"
          className="
            flex items-center justify-center
            rounded-xl
            border border-purple-500/30
            bg-purple-500/10
            px-4 py-3
            text-purple-300
            transition
            hover:bg-purple-500/20
          "
        >
          + Upload PDF
        </Link>

      </div>


      {/* Tip */}

      <div className="
        mt-10
        rounded-xl
        border border-purple-500/20
        bg-purple-500/5
        p-4
      ">

        <p className="font-medium text-purple-300">
          💡 Tip
        </p>

        <p className="mt-2 text-xs leading-5 text-gray-400">
          Select multiple PDFs to get
          answers combining your documents.
        </p>

      </div>


      {/* Bottom */}

      <div className="
        absolute
        bottom-5
        text-xs
        text-gray-600
      ">
        © 2026 Multi PDF RAG
      </div>

    </aside>
  );
}