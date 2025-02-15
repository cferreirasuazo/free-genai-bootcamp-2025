import React from "react";
import { Typography } from "@/components/atoms/Typography";
import { Card } from "@/components/atoms/Card"
import { LastSession } from "@/components/organisms/LastSession"
import { StudyProgress } from "@/components/organisms/StudyProgress"

const Dashboard: React.FC = () => {
  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6">
          <h2 className="text-2xl font-semibold mb-4">Last Session</h2>
          <LastSession />
        </Card>

        <Card className="p-6">
          <h2 className="text-2xl font-semibold mb-4">Study Progress</h2>
          <StudyProgress />
        </Card>
      </div>
    </div>
  );
};

export default Dashboard; 