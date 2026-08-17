const SESSION_KEY = "multi-pdf-rag-session-id";

export function getSessionId(): string {
  let sessionId = localStorage.getItem(SESSION_KEY);

  if (!sessionId) {
    sessionId = crypto.randomUUID();

    localStorage.setItem(
      SESSION_KEY,
      sessionId
    );
  }

  return sessionId;
}