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
        <div className="flex items-center justify-center min-h-screen">
            <DonutChart
                sections={[
                    { value: 30, color: "#f6483bff" },
                    { value: 70, color: "#10b981" }
                ]}
                total={100}
                size={300}
                defaultText={"PTO Left"}
            />
            <Card className="w-full max-w-md shadow-lg">
                <CardHeader>
                    <CardTitle>Marcus App Template</CardTitle>
                </CardHeader>
                <CardContent>
                    <CardDescription>
                        This app is a starter template for SaaS applications. To use this template, simply fork the repository and install the app dependencies.
                    </CardDescription>
                </CardContent>
                <CardFooter>
                    <CardDescription>Copyright 2025 Fourier Gauss Labs</CardDescription>
                </CardFooter>
            </Card>
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
                ]}
                xKey="month"
                yKey="PTO"
                title="Line Chart - Linear"
                description="January - June 2024"
                footer={
                  <>
                    <div className="flex gap-2 leading-none font-medium">
                      Trending up by 5.2% this month <span><svg width="16" height="16"><path d="M2 10l4-4 4 4 4-4" stroke="#10b981" strokeWidth="2" fill="none"/></svg></span>
                    </div>
                    <div className="text-muted-foreground leading-none">
                      Showing total visitors for the last 6 months
                    </div>
                  </>
                }
            />
        </div>
    );
}
