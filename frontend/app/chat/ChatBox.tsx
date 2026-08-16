"use client";

import { useEffect, useRef, useState } from "react";

import {
  askQuestion,
  getDocuments,
} from "@/lib/api";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

type Props = {
  sessionId?: string;
};

export default function ChatBox({
  sessionId = "frontend-test",
}: Props) {
  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);

  const [documents, setDocuments] =
    useState<string[]>([]);

  const [availableDocuments, setAvailableDocuments] =
    useState<string[]>([]);

  const [messages, setMessages] =
    useState<Message[]>([]);

  const messagesEndRef =
    useRef<HTMLDivElement | null>(null);

  // ==========================================
  // LOAD AVAILABLE DOCUMENTS
  // ==========================================

  useEffect(() => {
    async function loadDocuments() {
      try {
        const files = await getDocuments();

        setAvailableDocuments(files);
      } catch (error) {
        console.error(
          "Failed to load documents:",
          error
        );
      }
    }

    loadDocuments();
  }, []);

  // ==========================================
  // AUTO SCROLL TO LATEST MESSAGE
  // ==========================================

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  // ==========================================
  // SELECT / UNSELECT DOCUMENT
  // ==========================================

  function toggleDocument(
    filename: string
  ) {
    setDocuments((currentDocuments) => {
      if (
        currentDocuments.includes(filename)
      ) {
        return currentDocuments.filter(
          (document) =>
            document !== filename
        );
      }

      return [
        ...currentDocuments,
        filename,
      ];
    });
  }

  // ==========================================
  // SEND QUESTION
  // ==========================================

  async function handleSend() {
    const trimmedQuestion =
      question.trim();

    if (!trimmedQuestion) {
      return;
    }

    if (documents.length === 0) {
      return;
    }

    // ========================================
    // ADD USER MESSAGE IMMEDIATELY
    // ========================================

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ]);

    // Clear input immediately
    setQuestion("");

    setLoading(true);

    try {
      console.log(
        "Session ID:",
        sessionId
      );

      console.log(
        "Question:",
        trimmedQuestion
      );

      console.log(
        "Selected documents:",
        documents
      );

      // ======================================
      // CALL BACKEND
      // ======================================

      const data = await askQuestion(
        sessionId,
        trimmedQuestion,
        documents
      );

      // ======================================
      // ADD AI RESPONSE
      // ======================================

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          data.answer ||
          "I couldn't generate an answer.",
      };

      setMessages((currentMessages) => [
        ...currentMessages,
        assistantMessage,
      ]);
    } catch (error) {
      console.error(
        "Chat error:",
        error
      );

      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          "Sorry, something went wrong while processing your question.",
      };

      setMessages((currentMessages) => [
        ...currentMessages,
        errorMessage,
      ]);
    } finally {
      setLoading(false);
    }
  }

  // ==========================================
  // ENTER KEY
  // ==========================================

  function handleKeyDown(
    event: React.KeyboardEvent<HTMLInputElement>
  ) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      handleSend();
    }
  }

  // ==========================================
  // RENDER
  // ==========================================

  return (
    <div className="flex h-full min-h-0 flex-col bg-[#050814] text-white">

      {/* =====================================
          DOCUMENT SELECTOR
      ====================================== */}

      <section className="shrink-0 border-b border-slate-800 bg-[#070b16] px-10 py-6">

        <div className="flex items-center justify-between">

          <div>
            <h2 className="text-base font-semibold text-white">
              Select documents
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Choose one or more PDFs to ask questions about.
            </p>
          </div>

          {documents.length > 0 && (
            <div className="rounded-full border border-purple-500/40 bg-purple-500/10 px-4 py-2 text-xs font-medium text-purple-300">
              {documents.length} selected
            </div>
          )}

        </div>

        {/* DOCUMENT BUTTONS */}

        <div className="mt-5 flex flex-wrap gap-3">

          {availableDocuments.length === 0 ? (

            <p className="text-sm text-slate-500">
              No PDFs uploaded yet.
            </p>

          ) : (

            availableDocuments.map(
              (filename) => {

                const selected =
                  documents.includes(
                    filename
                  );

                return (
                  <button
                    key={filename}
                    type="button"
                    onClick={() =>
                      toggleDocument(
                        filename
                      )
                    }
                    className={`flex items-center gap-3 rounded-xl border px-4 py-3 text-sm transition ${
                      selected
                        ? "border-purple-500 bg-purple-500/10 text-purple-200 shadow-[0_0_20px_rgba(168,85,247,0.08)]"
                        : "border-slate-700 bg-[#0d1424] text-slate-400 hover:border-slate-500 hover:text-slate-200"
                    }`}
                  >

                    {/* CHECKBOX */}

                    <span
                      className={`flex h-5 w-5 items-center justify-center rounded-md border text-xs ${
                        selected
                          ? "border-purple-400 bg-purple-500 text-white"
                          : "border-slate-600 bg-transparent"
                      }`}
                    >
                      {selected
                        ? "✓"
                        : ""}
                    </span>

                    {/* FILE NAME */}

                    <span>
                      {filename}
                    </span>

                  </button>
                );
              }
            )
          )}

        </div>

      </section>

      {/* =====================================
          CHAT MESSAGES
      ====================================== */}

      <div className="min-h-0 flex-1 overflow-y-auto px-6 py-8">

        {/* EMPTY STATE */}

        {messages.length === 0 &&
          !loading && (
            <div className="flex h-full items-center justify-center">

              <div className="text-center">

                <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl border border-slate-800 bg-[#0b1120] text-4xl shadow-xl">
                  🤖
                </div>

                <h2 className="mt-6 text-2xl font-bold text-white">
                  Ask your documents
                </h2>

                <p className="mt-2 text-sm text-slate-500">
                  Select a PDF and ask anything about it.
                </p>

              </div>

            </div>
          )}

        {/* MESSAGE LIST */}

        <div className="mx-auto flex w-full max-w-4xl flex-col gap-7">

          {messages.map(
            (message) => {

              const isUser =
                message.role ===
                "user";

              return (
                <div
                  key={message.id}
                  className={`flex w-full gap-4 ${
                    isUser
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >

                  {/* AI AVATAR */}

                  {!isUser && (
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-slate-700 bg-[#0d1424] text-xl">
                      🤖
                    </div>
                  )}

                  {/* MESSAGE */}

                  <div
                    className={`max-w-[78%] ${
                      isUser
                        ? "items-end"
                        : "items-start"
                    }`}
                  >

                    <div
                      className={`mb-2 text-xs font-medium ${
                        isUser
                          ? "text-purple-400"
                          : "text-slate-500"
                      }`}
                    >
                      {isUser
                        ? "You"
                        : "AI"}
                    </div>

                    <div
                      className={`rounded-2xl px-5 py-4 text-sm leading-7 whitespace-pre-wrap ${
                        isUser
                          ? "rounded-br-md bg-purple-600 text-white shadow-lg shadow-purple-900/10"
                          : "rounded-bl-md border border-slate-800 bg-[#0d1424] text-slate-200"
                      }`}
                    >
                      {message.content}
                    </div>

                  </div>

                </div>
              );
            }
          )}

          {/* =================================
              LOADING MESSAGE
          ================================== */}

          {loading && (
            <div className="flex gap-4">

              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-slate-700 bg-[#0d1424] text-xl">
                🤖
              </div>

              <div>

                <div className="mb-2 text-xs font-medium text-slate-500">
                  AI
                </div>

                <div className="rounded-2xl rounded-bl-md border border-slate-800 bg-[#0d1424] px-5 py-4">

                  <div className="flex items-center gap-2">

                    <span className="h-2 w-2 animate-bounce rounded-full bg-slate-500 [animation-delay:-0.3s]" />

                    <span className="h-2 w-2 animate-bounce rounded-full bg-slate-500 [animation-delay:-0.15s]" />

                    <span className="h-2 w-2 animate-bounce rounded-full bg-slate-500" />

                  </div>

                </div>

              </div>

            </div>
          )}

          <div
            ref={messagesEndRef}
          />

        </div>

      </div>

      {/* =====================================
          INPUT AREA
      ====================================== */}

      <div className="shrink-0 border-t border-slate-800 bg-[#070b16] px-6 py-5">

        <div className="mx-auto flex w-full max-w-4xl items-center gap-3">

          <input
            type="text"
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }
            onKeyDown={handleKeyDown}
            disabled={loading}
            placeholder={
              documents.length === 0
                ? "Select a PDF first..."
                : "Ask about your documents..."
            }
            className="h-14 min-w-0 flex-1 rounded-xl border border-slate-700 bg-[#0d1424] px-5 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/10 disabled:cursor-not-allowed disabled:opacity-60"
          />

          <button
            type="button"
            onClick={handleSend}
            disabled={
              loading ||
              !question.trim() ||
              documents.length === 0
            }
            className="h-14 rounded-xl bg-purple-600 px-7 text-sm font-semibold text-white transition hover:bg-purple-500 disabled:cursor-not-allowed disabled:bg-slate-800 disabled:text-slate-500"
          >
            {loading
              ? "Thinking..."
              : "Send"}
          </button>

        </div>

        <p className="mt-3 text-center text-xs text-slate-600">
          AI responses are generated from your selected documents.
        </p>

      </div>

    </div>
  );
}