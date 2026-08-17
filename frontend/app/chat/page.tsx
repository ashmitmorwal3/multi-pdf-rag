"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { getSessionId } from "@/lib/session";

export default function ChatPage() {

  const router = useRouter();

  useEffect(() => {

    const sessionId = getSessionId();

    router.replace(
      `/chat/${sessionId}`
    );

  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#050814] text-white">
      <p className="text-slate-400">
        Loading your chat...
      </p>
    </div>
  );
}