type ConversationItemProps = {
    title: string;
  };
  
  export default function ConversationItem({
    title,
  }: ConversationItemProps) {
    return (
      <div className="mt-2 rounded-md p-2 hover:bg-gray-100">
        {title}
      </div>
    );
  }