"use client";

import { Bars3Icon } from "@heroicons/react/24/outline";

const Image = ({ src, alt, width, height, className }: { src: string, alt: string, width: number, height: number, className?: string }) => <img src={src} alt={alt} width={width} height={height} className={className} />;

interface TopBannerProps {
  isSidePanelOpen: boolean;
  toggleSidePanel: () => void;
}

export default function TopBanner({ isSidePanelOpen, toggleSidePanel }: TopBannerProps) {
  return (
    <header
      className={`
        fixed top-0 right-0 h-20
        backdrop-blur-md
        p-4 flex items-center justify-between z-40
        transition-all duration-300 ease-in-out
        ${isSidePanelOpen ? "left-64" : "left-20"}
      `}
    >
      <div className="flex items-center space-x-4">
        <h1 className="text-xl font-bold text-gray-900">{isSidePanelOpen ? "" : "Dashboard"}</h1>
      </div>
      <Image
          src="https://placehold.co/40x40/0d9488/ffffff?text=⚡"
          alt="Logo"
          width={40}
          height={40}
          className="rounded-full hidden sm:block"
        />
    </header>
  );
}
