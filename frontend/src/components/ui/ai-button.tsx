// src/components/ui/ai-button.tsx
import Link from 'next/link';
import { MessageCircle } from 'lucide-react'; // Example icon

export const AiButton = () => {
  return (
    <Link href="/ai-chat" passHref>
      <div
        className="flex items-center space-x-3 p-3 text-sm font-medium rounded-lg text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors cursor-pointer"
      >
        <MessageCircle className="w-5 h-5 text-blue-500" />
        <span>AI Assistant</span>
      </div>
    </Link>
  );
};