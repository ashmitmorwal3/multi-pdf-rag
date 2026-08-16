import { redirect } from "next/navigation";

export default function ChatPage() {

  const sessionId = crypto.randomUUID();

  redirect(`/chat/${sessionId}`);

}