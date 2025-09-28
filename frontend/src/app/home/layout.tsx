"use client";

import { ReactNode, useState } from "react";
import TopBanner from "@/components/topBanner";
import SidePanel from "@/components/sidePanel";

export default function HomeLayout({ children }: { children: ReactNode }) {
  const [isSidePanelOpen, setIsSidePanelOpen] = useState(true);

  const toggleSidePanel = () => setIsSidePanelOpen(prev => !prev);

  return (
    <div className="flex min-h-screen bg-gray-50">
      <SidePanel isOpen={isSidePanelOpen} toggle={toggleSidePanel} />

      <div className="flex flex-col flex-1 transition-all duration-300 ease-in-out">
        <TopBanner isSidePanelOpen={isSidePanelOpen} toggleSidePanel={toggleSidePanel} />

        <main
          className={`flex-1 p-6 transition-all duration-300 ease-in-out ${
            isSidePanelOpen ? "ml-64" : "ml-20"
          }`}
        >
          {children}
        </main>
      </div>
    </div>
  );
}
