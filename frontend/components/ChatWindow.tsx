"use client";

import ChatBox from "@/app/chat/ChatBox";
import UploadPDF from "@/components/UploadPDF";

type Props = {
  sessionId: string;
};

export default function ChatWindow({
  sessionId,
}: Props) {

  return (
    <main className="flex h-full min-w-0 flex-1 flex-col overflow-hidden bg-[#050814]">

      <header className="shrink-0 border-b border-slate-800 bg-[#070b16] px-8 py-6">

        <h1 className="text-2xl font-bold text-white">
          RAG Chat
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Session: {sessionId}
        </p>

      </header>


      {/* PDF UPLOAD */}

      <div className="shrink-0 border-b border-slate-800 bg-[#070b16] px-8 py-5">

        <UploadPDF
          sessionId={sessionId}
        />

      </div>


      {/* CHAT */}

      <div className="min-h-0 flex-1 overflow-hidden">

        <ChatBox
          sessionId={sessionId}
        />

      </div>

    </main>
  );
}