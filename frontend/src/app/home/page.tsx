"use client";

import { useAuth } from "@/context/authContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from "@/components/ui/card";
import { DonutChart } from "@/components/ui/DonutChart";
import { ChartLineLinear } from "@/components/ui/chartLineLinear";

export default function HomePage() {
    const { user, loading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!loading && !user) {
            router.push("/"); // Redirect to landing page if not authenticated
        }
    }, [user, loading, router]);

    if (loading) {
        return <p>Loading...</p>; // Show a loading state while checking auth
    }

    return (
        <div className="flex flex-col px-6 justify-center min-h-screen gap-4">
            <div className="flex flex-row w-full max-w-4xl gap-4">
                {/* PTO Summary Section */}
                <Card className="w-[380px] h-[380px] flex flex-row items-center justify-between shadow">
                    <div className="flex flex-col justify-center h-full px-4 gap-6">
                        <div>
                            <span className="text-3xl font-bold text-green-600">70</span>
                            <span className="ml-2 text-green-600">hours left</span>
                        </div>
                        <div>
                            <span className="text-3xl font-bold text-red-600">30</span>
                            <span className="ml-2 text-red-600">hours used</span>
                        </div>
                    </div>
                    <div className="flex items-center justify-center h-full pr-4">
                        <DonutChart
                            sections={[
                                { value: 30, color: "#f6483bff" },
                                { value: 70, color: "#10b981" }
                            ]}
                            total={100}
                            size={140}
                            defaultText={"PTO Left"}
                        />
                    </div>
                </Card>

                {/* Line Chart Section */}            
                <div className="flex-1 h-auto flex items-stretch">
                    <ChartLineLinear
                        data={[
                            { month: "January", PTO: 186 },
                            { month: "February", PTO: 305 },
                            { month: "March", PTO: 237 },
                            { month: "April", PTO: 73 },
                            { month: "May", PTO: 209 },
                            { month: "June", PTO: 214 },
                            { month: "July", PTO: 305 },
                            { month: "August", PTO: 237 },
                            { month: "September", PTO: 186 },
                            { month: "October", PTO: 214 },
                            { month: "November", PTO: 73 },
                            { month: "December", PTO: 200 },
                        ]}
                        xKey="month"
                        yKey="PTO"
                        title="PTO Usage per Month"
                    />
                </div>
            </div>

            {/* History Section */}
            <Card className="w-full max-w-4xl shadow-lg">
                <CardHeader>
                    <CardTitle>History</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-col gap-4">
                        {[
                            { name: "PTO Request", date: "2025-09-01", status: "pending" },
                            { name: "Sick Leave", date: "2025-08-15", status: "accepted" },
                            { name: "WFH Request", date: "2025-07-22", status: "rejected" }
                        ].map((record, idx) => (
                            <button
                                key={idx}
                                className="flex items-center justify-between w-full px-6 py-4 rounded-lg shadow hover:bg-gray-100 transition cursor-pointer border border-gray-200"
                            >
                                <div className="flex flex-row items-center gap-4">
                                    <span className="font-semibold text-lg">{record.name}</span>
                                </div>
                                <div className="flex items-center gap-4">
                                    <span className="text-sm text-gray-400">{record.date}</span>
                                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                                        record.status === "pending" ? "bg-yellow-100 text-yellow-800" :
                                        record.status === "accepted" ? "bg-green-100 text-green-800" :
                                        "bg-red-100 text-red-800"
                                    }`}>
                                        {record.status.charAt(0).toUpperCase() + record.status.slice(1)}
                                    </span>
                                    <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-400">
                                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                                    </svg>
                                </div>
                            </button>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
