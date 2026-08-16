import ChatWindow from "@/components/ChatWindow";

type Props = {
  params: Promise<{
    sessionId: string;
  }>;
};

export default async function ChatSessionPage({
  params,
}: Props) {

  const { sessionId } = await params;

  return (
    <ChatWindow
      sessionId={sessionId}
    />
  );
}