"use client";

import {
  HomeIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  PlusIcon,
  ArrowLeftCircleIcon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/react/24/outline";

interface SidePanelProps {
  isOpen: boolean;
  toggle: () => void;
}

export default function SidePanel({ isOpen, toggle }: SidePanelProps) {
  const menuItems = [
    { name: "New Chat", href: "/new-chat", icon: PlusIcon, isPrimary: true },
    { name: "Dashboard", href: "/home", icon: HomeIcon, isPrimary: false },
    { name: "Chats", href: "/home/chats", icon: ChatBubbleLeftRightIcon, isPrimary: false },
    { name: "Analytics", href: "/home/analytics", icon: ChartBarIcon, isPrimary: false },
  ];

  const primaryItem = menuItems.find((item) => item.isPrimary);
  const navigationItems = menuItems.filter((item) => !item.isPrimary);

  return (
    <aside
      className={`
        flex flex-col h-screen fixed top-0 left-0 z-50
        bg-gradient-to-b from-gray-900 via-gray-950 to-gray-900
        text-gray-200 border-r border-gray-800
        transition-all duration-500 ease-in-out
        ${isOpen ? "w-64" : "w-20"}
      `}
    >
      {/* Top Section */}
      <div
        onClick={toggle}
        className={`
          flex items-center cursor-pointer h-16 px-4 mb-4
          transition-all duration-300
          ${isOpen ? "justify-start" : "justify-center"}
        `}
      >
        {isOpen ? (
          <h2 className="text-lg font-bold tracking-tight text-white">
            ChatGPT Clone
          </h2>
        ) : (
          <span className="text-2xl text-teal-400 animate-pulse">⚡</span>
        )}
      </div>

      {/* Middle Section */}
      <div className="flex-1 overflow-y-hidden px-2">
        {primaryItem && (
          <a
            href={primaryItem.href}
            className={`
              flex items-center w-full mb-4 py-3 px-3 rounded-lg font-semibold
              bg-teal-600 text-white hover:bg-teal-500 hover:scale-105 transform transition-all
              ${isOpen ? "justify-start" : "justify-center"}
            `}
          >
            <primaryItem.icon className={`h-5 w-5 ${isOpen ? "mr-3" : ""}`} />
            <span
              className={`
                overflow-hidden whitespace-nowrap transition-all duration-300
                ${isOpen ? "max-w-full opacity-100" : "max-w-0 opacity-0"}
              `}
            >
              {primaryItem.name}
            </span>
          </a>
        )}

        <nav className="flex flex-col space-y-1">
          {navigationItems.map((item) => (
            <a
              key={item.name}
              href={item.href}
              className={`
                relative flex items-center py-2 px-3 rounded-lg text-sm
                hover:bg-gray-700/70 hover:text-white hover:scale-105 transform transition-all
                group
                ${isOpen ? "justify-start" : "justify-center"}
              `}
            >
              <item.icon className={`h-5 w-5 ${isOpen ? "mr-3" : ""}`} />
              <span
                className={`
                  overflow-hidden whitespace-nowrap transition-all duration-300
                  ${isOpen ? "max-w-full opacity-100" : "max-w-0 opacity-0"}
                `}
              >
                {item.name}
              </span>

              {!isOpen && (
                <span
                  className="
                    absolute left-full ml-2 bg-gray-900 text-white text-xs px-2 py-1
                    rounded shadow-lg opacity-0 group-hover:opacity-100 whitespace-nowrap
                    pointer-events-none transition-opacity
                  "
                >
                  {item.name}
                </span>
              )}
            </a>
          ))}
        </nav>
      </div>

      {/* Footer */}
      <div className="p-3 border-t border-gray-800">
        <a
          href="/home/settings"
          className={`
            flex items-center w-full py-2 px-3 rounded-lg text-sm text-gray-300
            hover:bg-gray-700/70 hover:text-white hover:scale-105 transform transition-all
            ${isOpen ? "justify-start" : "justify-center"}
          `}
        >
          <Cog6ToothIcon className={`h-5 w-5 ${isOpen ? "mr-3" : ""}`} />
          <span
            className={`
              overflow-hidden whitespace-nowrap transition-all duration-300
              ${isOpen ? "max-w-full opacity-100" : "max-w-0 opacity-0"}
            `}
          >
            Settings
          </span>
        </a>

        <a
          href="/logout"
          className={`
            flex items-center mt-2 w-full py-2 px-3 rounded-lg text-sm text-gray-300
            hover:bg-red-600 hover:text-white hover:scale-105 transform transition-all
            ${isOpen ? "justify-start" : "justify-center"}
          `}
        >
          <ArrowRightOnRectangleIcon className={`h-5 w-5 ${isOpen ? "mr-3" : ""}`} />
          <span
            className={`
              overflow-hidden whitespace-nowrap transition-all duration-300
              ${isOpen ? "max-w-full opacity-100" : "max-w-0 opacity-0"}
            `}
          >
            Logout
          </span>
        </a>

        <button
          onClick={toggle}
          className={`
            flex items-center mt-4 w-full py-2 px-3 rounded-lg text-sm text-gray-300
            hover:bg-gray-700/70 hover:text-white transform transition-all
            ${isOpen ? "justify-start" : "justify-center"}
          `}
        >
          <ArrowLeftCircleIcon
            className={`h-5 w-5 transition-transform duration-500 ${isOpen ? "" : "rotate-180"}`}
          />
          <span
            className={`
              overflow-hidden whitespace-nowrap transition-all duration-300
              ${isOpen ? "ml-2 max-w-full opacity-100" : "max-w-0 opacity-0"}
            `}
          >
            Collapse
          </span>
        </button>
      </div>
    </aside>
  );
}
